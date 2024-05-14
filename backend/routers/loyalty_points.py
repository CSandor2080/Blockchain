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
print(w3.eth.accounts)
@app.post("/issue-points/{to_address}/{points}")
def issue_points(to_address: str, points: int):
    try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        tx_hash = contract.functions.issuePoints(to_address, points).transact({
            'from': w3.eth.accounts[0],  # Use the first account in Ganache
            'gas': 500000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")
        return {"status": "success", "transaction_receipt": str(tx_receipt)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


from web3.exceptions import TransactionNotFound, TimeExhausted

from fastapi import HTTPException
from web3 import Web3, exceptions

@app.post("/redeem-points/{to_address}/{points}")
async def redeem_points(to_address: str, points: int):
    try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        tx_hash = contract.functions.redeemPoints(to_address, points).transact({
            'from': w3.eth.accounts[0],
            'gas': 500000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # Ensure the transaction was successful before returning the receipt
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")

        # Convert transaction receipt to a JSON-friendly format
        receipt = {
            "transactionHash": tx_receipt.transactionHash.hex(),
            "blockHash": tx_receipt.blockHash.hex(),
            "blockNumber": tx_receipt.blockNumber,
            "cumulativeGasUsed": tx_receipt.cumulativeGasUsed,
            "gasUsed": tx_receipt.gasUsed,
            "status": tx_receipt.status,
        }
        return {"status": "success", "transaction_receipt": receipt}
    except exceptions.TransactionNotFound:
        raise HTTPException(status_code=404, detail="Transaction not found")
    except exceptions.TimeExhausted:
        raise HTTPException(status_code=408, detail="Transaction timeout")
    except exceptions.ContractLogicError as e:
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
