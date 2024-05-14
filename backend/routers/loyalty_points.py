import json
from fastapi import APIRouter, HTTPException
from web3.exceptions import ContractLogicError, TransactionNotFound, TimeExhausted
from web3 import Web3, exceptions
from routers.common import (
    w3,
    LOYALTY_POINTS_CONTRACT_ADDRESS,
    LOYALTY_POINTS_ABI,
    upload_to_ipfs,
    get_from_ipfs
)
import  ipfshttpclient
app = APIRouter()
def upload_to_ipfs(data):
    client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')
    res = client.add_str(data)
    print(f"######################IPFS add_json response: {res}")
    return res

def get_from_ipfs(ipfs_hash):
    client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')
    return client.cat(ipfs_hash).decode('utf-8')

@app.post("/issue-points/{to_address}/{points}")
def issue_points_endpoint(to_address: str, points: int):
    #try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        current_points, _ = contract.functions.getPointsBalance(to_address).call()
        new_points = current_points + points
        metadata = {"address": to_address, "points": new_points}

        ipfs_hash = upload_to_ipfs(json.dumps(metadata))
        tx_hash = contract.functions.issuePoints(to_address, points, ipfs_hash).transact({
            'from': w3.eth.accounts[0], 'gas': 500000, 'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")
        return {"status": "success", "ipfs_hash": ipfs_hash}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/redeem-points/{to_address}/{points}")
async def redeem_points_endpoint(to_address: str, points: int):
    try:
        contract = w3.eth.contract(address=LOYALTY_POINTS_CONTRACT_ADDRESS, abi=LOYALTY_POINTS_ABI)
        current_points, _ = contract.functions.getPointsBalance(to_address).call()
        if current_points < points:
            raise HTTPException(status_code=400, detail="Insufficient points")
        new_points = current_points - points
        metadata = {"address": to_address, "points": new_points}

        ipfs_hash = upload_to_ipfs(json.dumps(metadata))
        tx_hash = contract.functions.redeemPoints(to_address, points, ipfs_hash).transact({
            'from': w3.eth.accounts[0], 'gas': 500000, 'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            raise HTTPException(status_code=500, detail="Transaction failed to execute.")
        receipt = {
            "transactionHash": tx_receipt.transactionHash.hex(),
            "blockHash": tx_receipt.blockHash.hex(),
            "blockNumber": tx_receipt.blockNumber,
            "cumulativeGasUsed": tx_receipt.cumulativeGasUsed,
            "gasUsed": tx_receipt.gasUsed,
            "status": tx_receipt.status,
        }
        return {"status": "success", "transaction_receipt": receipt, "ipfs_hash": ipfs_hash}
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
        points, ipfs_hash = contract.functions.getPointsBalance(account_address).call()
        if not ipfs_hash:
            raise HTTPException(status_code=404, detail="IPFS hash not found")
        metadata = get_from_ipfs(ipfs_hash)
        return {"points": points, "ipfs_hash": ipfs_hash, "metadata": json.loads(metadata)}
    except exceptions.ContractLogicError as e:
        raise HTTPException(status_code=400, detail=f"Contract error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/upload-data-ipfs")
def upload_data_to_ipfs(data: str):
    try:
        ipfs_hash = upload_to_ipfs(data)
        return {"ipfs_hash": ipfs_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS upload error: {str(e)}")

@app.get("/get-data-ipfs/{ipfs_hash}")
def get_data_from_ipfs(ipfs_hash: str):
    try:
        data = get_from_ipfs(ipfs_hash)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPFS retrieval error: {str(e)}")

LOYALTY_POINTS_ROUTER =app