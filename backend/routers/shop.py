from fastapi import APIRouter, HTTPException, Query
from web3 import Web3, exceptions
from .common import w3, SHOP_CONTRACT_ADDRESS, SHOP_ABI
from .loyalty_points import issue_points_endpoint, redeem_points_endpoint, get_points_balance, upload_to_ipfs
import json
count = 7
app = APIRouter()

@app.post("/add-product", tags=["Shop"])
def add_product(name: str, price: float):
    global count
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

        count += 1

        return {
            "status": "success",
            "transaction_hash": tx_receipt.transactionHash.hex(),
            "product_id": product_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# @app.post("/buy-product/{product_id}", tags=["Shop"])
# def buy_product(product_id: int, buyer_address: str = Query(...), use_points: bool = Query(False)):
#     print(f"Received request to buy product {product_id} by {buyer_address} using points: {use_points}")
#     try:
#         # Initialize contract
#         contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)
#
#         # Fetch product details
#         product = contract.functions.getProduct(product_id).call()
#         name = product[0]
#         price_in_wei = product[1]
#         total_price = price_in_wei
#
#         discount = 0
#         if use_points:
#             points_balance = get_points_balance(buyer_address)["points"]
#             print(f"User {buyer_address} has {points_balance} loyalty points.")
#             max_discount = total_price * 90 // 100  # Maximum discount is 90% of the total price
#             discount = min(points_balance, max_discount)  # Discount cannot exceed the max discount
#             total_price -= discount
#
#             # Burn used points
#             try:
#                 response = redeem_points_endpoint(buyer_address, discount)
#                 print(f"Redeem points response: {response}")
#                 if "status" not in response or response["status"] != "success":
#                     print(f"Failed to redeem points: {response}")
#                     raise HTTPException(status_code=500, detail=f"Failed to redeem points: {response.get('detail', 'Unknown error')}")
#                 print(f"Successfully redeemed {discount} points for {buyer_address}")
#             except Exception as e:
#                 print(f"Error redeeming points: {str(e)}")
#                 raise HTTPException(status_code=500, detail=f"Error redeeming points: {str(e)}")
#
#         # Execute buy transaction
#         try:
#             tx_hash = contract.functions.buyProduct(product_id, use_points).transact({
#                 'from': buyer_address,
#                 'value': total_price,
#                 'gas': 500000,
#                 'gasPrice': w3.to_wei('20', 'gwei')
#             })
#             tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#             if tx_receipt.status == 0:
#                 raise HTTPException(status_code=500, detail="Transaction failed to execute.")
#             print(f"Transaction successful: {tx_receipt.transactionHash.hex()}")
#         except Exception as e:
#             print(f"Transaction error: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")
#
#         # Calculate earned loyalty points on the original price (no discount)
#         loyalty_points_earned = (5 * price_in_wei) // 100  # 5% loyalty points in Wei
#         metadata = {"address": buyer_address, "points": loyalty_points_earned}
#         ipfs_hash = upload_to_ipfs(json.dumps(metadata))
#
#         # Issue earned points
#         try:
#             response = issue_points_endpoint(buyer_address, loyalty_points_earned)
#             print(f"Issue points response: {response}")
#             if "status" not in response or response["status"] != "success":
#                 print(f"Failed to issue points: {response}")
#                 raise HTTPException(status_code=500, detail=f"Failed to issue points: {response.get('detail', 'Unknown error')}")
#             print(f"Successfully issued {loyalty_points_earned} points to {buyer_address}")
#         except Exception as e:
#             print(f"Error issuing points: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Error issuing points: {str(e)}")
#
#         return {
#             "status": "success",
#             "transaction_hash": tx_receipt.transactionHash.hex(),
#             "discount_applied": discount,  # Return discount applied for clarity
#             "loyalty_points_earned": loyalty_points_earned  # Return earned points for clarity
#         }
#     except exceptions.ContractLogicError as e:
#         print(f"Contract logic error: {str(e)}")
#         raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
#     except Exception as e:
#         print(f"Server error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/buy-product/{product_id}", tags=["Shop"])
def buy_product(product_id: int, buyer_address: str = Query(...), use_points: bool = Query(False)):
    print(f"Received request to buy product {product_id} by {buyer_address} using points: {use_points}")
    try:
        # Initialize contract
        contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)

        # Fetch product details
        product = contract.functions.getProduct(product_id).call()
        name = product[0]
        price_in_wei = product[1]
        total_price = price_in_wei

        discount = 0
        if use_points:
            points_balance = get_points_balance(buyer_address)["points"]
            print(f"User {buyer_address} has {points_balance} loyalty points.")
            max_discount = total_price * 90 // 100  # Maximum discount is 90% of the total price
            discount = min(points_balance, max_discount)  # Discount cannot exceed the max discount
            total_price -= discount

            if points_balance > 0:
                # Burn used points
                try:
                    response = redeem_points_endpoint(buyer_address, discount)
                    print(f"Redeem points response: {response}")
                    if "status" not in response or response["status"] != "success":
                        print(f"Failed to redeem points: {response}")
                        raise HTTPException(status_code=500, detail=f"Failed to redeem points: {response.get('detail', 'Unknown error')}")
                    print(f"Successfully redeemed {discount} points for {buyer_address}")
                except Exception as e:
                    print(f"Error redeeming points: {str(e)}")
                    raise HTTPException(status_code=500, detail=f"Error redeeming points: {str(e)}")

        # Execute buy transaction
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

        # Calculate earned loyalty points on the original price (no discount)
        loyalty_points_earned = (5 * price_in_wei) // 100  # 5% loyalty points in Wei
        metadata = {"address": buyer_address, "points": loyalty_points_earned}
        ipfs_hash = upload_to_ipfs(json.dumps(metadata))

        # Issue earned points
        try:
            response = issue_points_endpoint(buyer_address, loyalty_points_earned)
            print(f"Issue points response: {response}")
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


@app.get("/get-products", tags=["Shop"])
def get_products():
    try:
        contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)
        product_count = 2
        products = []
        for product_id in range(count):
            name, price_in_wei = contract.functions.getProduct(product_id).call()
            price_in_eth = w3.from_wei(price_in_wei, 'ether')
            products.append({
                "product_id": product_id,
                "name": name,
                "price": price_in_eth
            })
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

SHOP_ROUTER = app
