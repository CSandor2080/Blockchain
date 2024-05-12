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

@app.post("/issue-points/{to_address}/{points}")
def issue_points(to_address: str, points: int):
    try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        tx_hash = contract.functions.issuePoints(to_address, points).transact({'from': BEVERAGE_CONTRACT_ADDRESS})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return {"status": "success", "transaction_receipt": tx_receipt}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/redeem-points/{to_address}/{points}")
def redeem_points(to_address: str, points: int):
    try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        tx_hash = contract.functions.redeemPoints(to_address, points).transact({'from': BEVERAGE_CONTRACT_ADDRESS})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return {"status": "success", "transaction_receipt": tx_receipt}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/points-balance/{account_address}")
def get_points_balance(account_address: str):
    try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        balance = contract.functions.getPointsBalance(account_address).call()
        return {"points_balance": balance}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


LOYALTY_POINTS_ROUTER = app
