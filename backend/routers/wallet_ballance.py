from fastapi import APIRouter
from fastapi import HTTPException
from routers.common import (w3, LOYALTY_POINTS_CONTRACT_ADDRESS,
                  BEVERAGE_CONTRACT_ADDRESS, LOYALTY_POINTS_ABI,BEVERAGE_ABI)

app = APIRouter()

@app.get("/wallets")
def get_wallets():
    return {"accounts": w3.eth.accounts}

@app.get("/balance/{account_address}")
def get_balance(account_address: str):
    try:
        balance = w3.eth.get_balance(account_address)
        return {"balance": w3.from_wei(balance, 'ether')}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

WALLET_BALANCE_ROUTER = app