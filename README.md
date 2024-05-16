### Loyalty rewards application

The application aims to provide a solution for rewarding customers based on frequent acquisitions in a decentralized 
manner.

##### Features
- Issue points for a user
- Redeem points



##### Getting started

The application is in the development stage, at the moment, to run the application docker containers are necessary.
- `docker run -p 8545:8545 trufflesuite/ganache`
- `docker run -d --name ipfs_host -p 5001:5001 ipfs/go-ipfs:v0.6.0`
- `npm install` - Installing npm dependencies
- `nom install -g truffle`
- `truffle migrate --network development` (Move the Loyalty contract address in backend/routers/common in LOYALTY_POINTS_CONTRACT_ADDRESS)
- `cd ./backend`
- `pip install -r requirements.txt`
- `python/python3 main.py`

Contract testing is done in js and is handled by truffle:
- `truffle test`

##### Repository content
- **backend**: Provides backend functionalities. It is written in python fastapi.
- **frontend**: Provides frontend functionalities. It is written in HTML, CSS, plain js.
- **contracts**: Provides the implementation for contracts. It is written in solidity.
- **migrations**: Provides the script/s for moving the contracts to a network.
- **test**: Provides suite of tests for contract functionalities. It is written in plain js.


