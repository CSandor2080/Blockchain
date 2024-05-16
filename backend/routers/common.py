import os
import sys
import pathlib
from os.path import dirname, realpath

import uvicorn

from web3 import Web3
import json
# Contract Addresses (set these after you deploy your contracts)
LOYALTY_POINTS_CONTRACT_ADDRESS = '0x659b5f31410FE75cCA404BF78F2B885900a3145a'


# Load contract ABIs
loyal_file_path = str(pathlib.Path(dirname(realpath(__file__)) + "/../../" +"build/contracts/LoyaltyPoints.json" ).resolve())


with open(loyal_file_path) as file:
    contract_json = json.load(file)
    LOYALTY_POINTS_ABI = contract_json['abi']


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
