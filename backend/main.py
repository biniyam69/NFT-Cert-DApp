import os, sys
import base64
from algosdk.v2client import algod
from fastapi import FastAPI
from typing import Optional
from algosdk import account , encoding , mnemonic
from algosdk.transaction import PaymentTxn
from algosdk.transaction import AssetConfigTxn, AssetCreateTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.transaction import *
from algosdk.error import *
from algosdk.v2client import algod, indexer





sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

algod_client=algod.AlgodClient("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","http://localhost:4001") #Initializing the algod client
indexer_client=indexer.IndexerClient("","http://localhost:8980") #initializing the validator


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/account")
def create_account():
    private_key, address = account.generate_account()
    paraphrase = mnemonic.from_private_key(private_key)

    return {"address": address, "paraphrase": paraphrase}

@app.get("/account/{Address}")
def get_account_details(Address: str):
    info = algod_client.account_info(Address)
    return {"Address": info}

@app.post("/transaction")
def create_transaction(transacrion: Transaction):
    params = algod_client.suggested_params()


