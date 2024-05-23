from fastapi import APIRouter, HTTPException
from web3 import Web3, exceptions
from .common import w3, SHOP_CONTRACT_ADDRESS, SHOP_ABI
from .loyalty_points import issue_points_endpoint, redeem_points_endpoint, get_points_balance, upload_to_ipfs
import json

app = APIRouter()

@app.post("/add-product", tags=["Shop"])
def add_product(name: str, price: float):
    try:
        contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)
        price_in_wei = w3.to_wei(price, 'ether')
        tx_hash = contract.functions.addProduct(name, price_in_wei).transact({
            'from': w3.eth.accounts[0], 'gas': 500000, 'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")

        # Parse the event to get the product ID
        logs = contract.events.ProductAdded().get_logs(fromBlock=tx_receipt['blockNumber'], toBlock=tx_receipt['blockNumber'])
        if not logs:
            raise HTTPException(status_code=500, detail="ProductAdded event not found in transaction receipt.")

        product_id = logs[0]['args']['productId']

        return {
            "status": "success",
            "transaction_hash": tx_receipt.transactionHash.hex(),
            "product_id": product_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/buy-product/{product_id}", tags=["Shop"])
def buy_product(product_id: int, buyer_address: str, use_points: bool = False):
    try:
        # Inițializare contract
        contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)

        # Obținerea detaliilor produsului
        product = contract.functions.getProduct(product_id).call()
        name = product[0]
        price_in_wei = product[1]
        total_price = price_in_wei

        discount = 0
        if use_points:
            points_balance = get_points_balance(buyer_address)["points"]
            max_discount = total_price * 90 // 100  # Maximum discount is 90% of the total price
            discount = min(points_balance, max_discount)  # Discount cannot exceed the max discount
            total_price -= discount

            # Arderea punctelor folosite
            try:
                response = redeem_points_endpoint(buyer_address, discount)
                if "status" not in response or response["status"] != "success":
                    print(f"Failed to redeem points: {response}")
                    raise HTTPException(status_code=500, detail=f"Failed to redeem points: {response.get('detail', 'Unknown error')}")
                print(f"Successfully redeemed {discount} points for {buyer_address}")
            except Exception as e:
                print(f"Error redeeming points: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error redeeming points: {str(e)}")

        # Executarea tranzacției de cumpărare
        try:
            tx_hash = contract.functions.buyProduct(product_id, use_points).transact({
                'from': buyer_address,
                'value': total_price,
                'gas': 500000,
                'gasPrice': w3.to_wei('20', 'gwei')
            })
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            if tx_receipt.status == 0:
                raise HTTPException(status_code=500, detail="Transaction failed to execute.")
            print(f"Transaction successful: {tx_receipt.transactionHash.hex()}")
        except Exception as e:
            print(f"Transaction error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

        # Calcularea punctelor de loialitate câștigate la prețul original (fără discount)
        loyalty_points_earned = (5 * price_in_wei) // 100  # 5% loyalty points in Wei
        metadata = {"address": buyer_address, "points": loyalty_points_earned}
        ipfs_hash = upload_to_ipfs(json.dumps(metadata))

        # Emiterea punctelor câștigate
        try:
            response = issue_points_endpoint(buyer_address, loyalty_points_earned)
            if "status" not in response or response["status"] != "success":
                print(f"Failed to issue points: {response}")
                raise HTTPException(status_code=500, detail=f"Failed to issue points: {response.get('detail', 'Unknown error')}")
            print(f"Successfully issued {loyalty_points_earned} points to {buyer_address}")
        except Exception as e:
            print(f"Error issuing points: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error issuing points: {str(e)}")

        return {
            "status": "success",
            "transaction_hash": tx_receipt.transactionHash.hex(),
            "discount_applied": discount,  # Return discount applied for clarity
            "loyalty_points_earned": loyalty_points_earned  # Return earned points for clarity
        }
    except exceptions.ContractLogicError as e:
        print(f"Contract logic error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
        print(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/get-product/{product_id}", tags=["Shop"])
def get_product(product_id: int):
    try:
        contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)
        name, price_in_wei = contract.functions.getProduct(product_id).call()
        price_in_eth = w3.from_wei(price_in_wei, 'ether')
        return {
            "name": name,
            "price": price_in_eth
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

SHOP_ROUTER = app
