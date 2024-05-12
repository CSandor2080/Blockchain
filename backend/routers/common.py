import os
import sys
import pathlib
from os.path import dirname, realpath

import uvicorn

from web3 import Web3
import json
# Contract Addresses (set these after you deploy your contracts)
LOYALTY_POINTS_CONTRACT_ADDRESS = '0xa881c83a92968FCe612f68A7334BC068c945eA2b'
BEVERAGE_CONTRACT_ADDRESS = '0xd52bE6158f6122C7116cdC23a7ccf71570B8f750'

# Load contract ABIs
loyal_file_path = str(pathlib.Path(dirname(realpath(__file__)) + "/../../" +"build/contracts/LoyaltyPoints.json" ).resolve())
bvg_file_path=  str(pathlib.Path(dirname(realpath(__file__)) + "/../../" +"build/contracts/BeverageContract.json" ).resolve())


with open(loyal_file_path) as file:
    contract_json = json.load(file)
    LOYALTY_POINTS_ABI = contract_json['abi']

with open(bvg_file_path) as file:
    contract_json = json.load(file)
    BEVERAGE_ABI = contract_json['abi']

WEB3_PROVIDER_URI = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum client")
else:
    print("Connected successfully...")

