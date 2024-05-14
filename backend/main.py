import os
import sys
import pathlib
from os.path import dirname, realpath

import uvicorn

sys.path.append(
    str(pathlib.Path(dirname(realpath(__file__)) + "/../..").resolve())
)


from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, Path

#from routers.beverage_contract import BEVERAGE_ROUTER
from routers.loyalty_points import LOYALTY_POINTS_ROUTER
from routers.wallet_ballance import WALLET_BALANCE_ROUTER
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# List of allowed origins; '*' allows all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Set up Web3



@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse("/docs")


app.include_router(WALLET_BALANCE_ROUTER)
app.include_router(LOYALTY_POINTS_ROUTER)
#app.include_router(BEVERAGE_ROUTER)


if __name__ == "__main__":
    uvicorn.run(
        host='127.0.0.1',
        port=8080,
        app="main:app",
        reload=True
    )