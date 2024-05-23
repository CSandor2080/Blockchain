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
def buy_product(product_id: int, buyer_address: str, quantity: int = 1, use_points: bool = False):
    try:
        contract = w3.eth.contract(address=SHOP_CONTRACT_ADDRESS, abi=SHOP_ABI)

        # Fetch the product details
        name, price_in_wei = contract.functions.getProduct(product_id).call()
        total_price = price_in_wei * quantity

        if use_points:
            points_balance = get_points_balance(buyer_address)["points"]
            discount = min(points_balance, total_price)
            total_price -= discount
            redeem_points_endpoint(buyer_address, discount)

        tx_hash = contract.functions.buyProduct(product_id, use_points).transact({
            'from': buyer_address,
            'value': total_price,
            'gas': 500000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })

        if not use_points:
            loyalty_points_earned = (5 * total_price) // 100  # 5% loyalty points in Wei
            metadata = {"address": buyer_address, "points": loyalty_points_earned}
            ipfs_hash = upload_to_ipfs(json.dumps(metadata))
            issue_points_endpoint(buyer_address, loyalty_points_earned)

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")

        return {
            "status": "success",
            "transaction_hash": tx_receipt.transactionHash.hex()
        }
    except exceptions.ContractLogicError as e:
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
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
