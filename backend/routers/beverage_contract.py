from fastapi import APIRouter, HTTPException
from web3.exceptions import ContractLogicError, TransactionNotFound, TimeExhausted
from routers.common import (
    w3,
    LOYALTY_POINTS_CONTRACT_ADDRESS,
    BEVERAGE_CONTRACT_ADDRESS,
    LOYALTY_POINTS_ABI,
    BEVERAGE_ABI
)

app = APIRouter()

@app.post("/purchase-beverage/{customer_address}")
def purchase_beverage(customer_address: str):
    try:
        contract = w3.eth.contract(address=BEVERAGE_CONTRACT_ADDRESS, abi=BEVERAGE_ABI)
        tx_hash = contract.functions.purchase(customer_address).transact({
            'from': w3.eth.accounts[0],
            'gas': 500000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        # if tx_receipt.status == 0:
        #     raise HTTPException(status_code=500, detail="Transaction failed to execute.")
        return {"status": "success", "transaction_receipt": str(tx_receipt)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/redeem-beverage/{customer_address}/{points}")
def redeem_beverage(customer_address: str, points: int):
    try:
        contract = w3.eth.contract(address=BEVERAGE_CONTRACT_ADDRESS, abi=BEVERAGE_ABI)
        tx_hash = contract.functions.redeem(customer_address, points).transact({
            'from': w3.eth.accounts[0],
            'gas': 500000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")
        return {"status": "success", "transaction_receipt": str(tx_receipt)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

BEVERAGE_ROUTER = app
