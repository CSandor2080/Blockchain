from fastapi import APIRouter, HTTPException
from web3.exceptions import ContractLogicError
from routers.common import (
    w3,
    LOYALTY_POINTS_CONTRACT_ADDRESS,
    BEVERAGE_CONTRACT_ADDRESS,
    LOYALTY_POINTS_ABI,
    BEVERAGE_ABI
)

app = APIRouter()

def execute_transaction(contract, function, *args):
    try:
        tx_hash = function(*args).transact({'from': BEVERAGE_CONTRACT_ADDRESS})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return {"status": "success", "transaction_receipt": tx_receipt}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/purchase-beverage/{customer_address}")
def purchase_beverage(customer_address: str):
    try:
        contract = w3.eth.contract(address=BEVERAGE_CONTRACT_ADDRESS, abi=BEVERAGE_ABI)
        return execute_transaction(contract, contract.functions.purchase, customer_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/redeem-beverage/{customer_address}/{points}")
def redeem_beverage(customer_address: str, points: int):
    try:
        contract = w3.eth.contract(address=BEVERAGE_CONTRACT_ADDRESS, abi=BEVERAGE_ABI)
        return execute_transaction(contract, contract.functions.redeem, customer_address, points)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

BEVERAGE_ROUTER = app
