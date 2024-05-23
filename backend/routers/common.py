import os
import sys
import enum
import pathlib
from os.path import dirname, realpath

import uvicorn
from web3 import Web3
import json

class Tags(enum.Enum):
    LOYALTY_POINTS = "LoyaltyPoints"
    SHOP = "Shop"
    BALANCE = "Balance"
    IPFS= "IPFS"
# Contract Addresses (set these after you deploy your contracts)
LOYALTY_POINTS_CONTRACT_ADDRESS = '0xB016E4ddbb34a0492A7A8316a57305F35E81f05a'
SHOP_CONTRACT_ADDRESS = '0x152dCaDBe2c880E67066852b2Cc3D9F80F222346'

# Load contract ABIs
loyal_file_path = str(pathlib.Path(dirname(realpath(__file__)) + "/../../" +"build/contracts/LoyaltyPoints.json" ).resolve())
shop_file_path = str(pathlib.Path(dirname(realpath(__file__)) + "/../../" +"build/contracts/Shop.json").resolve())

# Load LoyaltyPoints contract ABI
with open(loyal_file_path) as file:
    loyalty_points_contract_json = json.load(file)
    LOYALTY_POINTS_ABI = loyalty_points_contract_json['abi']

# Load Shop contract ABI
with open(shop_file_path) as file:
    shop_contract_json = json.load(file)
    SHOP_ABI = shop_contract_json['abi']

WEB3_PROVIDER_URI = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum client")
else:
    print("Connected successfully...")

import ipfshttpclient

def upload_to_ipfs(data):
    client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')
    res = client.add_json(data)  # Using add_json to add data and return a dictionary
    return res

def get_from_ipfs(ipfs_hash):
    client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')
    return client.cat(ipfs_hash).decode('utf-8')
