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
from schemes import AssetCreation, Transaction



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

@app.post("/nft_transfer")
def nft_transfer(transaction: Transaction):
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "your-api-key"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    try:
        private_key = encoding.mnemonic_to_private_key(transaction.passphrase)
        sender_address = account.address_from_private_key(private_key)

        params = algod_client.suggested_params()
        unsigned_txn = transaction.AssetTransferTxn(
            sender = sender_address,
            first=params["lastRound"],
            last=params["lastRound"] + 1000,
            note =transaction.note.encode(),
            asset=transaction.asset_id,
            to=transaction.reciever_address,
            amount=transaction.amount,
            genesis_hash=algod_client.genesis().hash,
        )

        #sign the transaction
        signed_txn = unsigned_txn.sign(private_key)
        
        #submit the transaction to the algorand network

        tx_id = algod_client.send_transaction(signed_txn)
        return {"Transaction ID": tx_id}
    
    except WrongChecksumError:
        return {"passphrase": "Checksum Error"}
    
    except ValueError:
        return {"passphrase": "Unknown value in the passphrase"}
    
    except WrongMnemonicLengthError:
        return {"passphrase": "Incorrect lengthof the passphrase"}
    





@app.post("/create_asset")
def create_asset(asset_creation: AssetCreation, transaction: Transaction):
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "your-api-key"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    try:
        # Recover account from passphrase
        private_key = encoding.mnemonic_to_private_key(asset_creation.passphrase)
        creator_address = account.address_from_private_key(private_key)

        # Create the asset creation transaction
        params = algod_client.suggested_params()
        unsigned_txn = transaction.AssetConfigTxn(
            sender=creator_address,
            fee=1000,
            first=params["lastRound"],
            last=params["lastRound"] + 1000,
            gh=params["genesisID"],
            receiver=creator_address,
            asset_name=asset_creation.asset_name,
            unit_name=asset_creation.unit_name,
            total=asset_creation.total,
            decimals=asset_creation.decimals,
            default_frozen=asset_creation.default_frozen,
            url=asset_creation.url,
            manager=asset_creation.manager,
            reserve=asset_creation.reserve,
            freeze=asset_creation.freeze,
            clawback=asset_creation.clawback,
        )

        #sign the transaction
        signed_txn = unsigned_txn.sign(private_key)

        #ssubmit the transaction to algorand network
        tx_id = algod_client.send_transaction(signed_txn)
        return {"Asset Creation Transaction ID": tx_id}

    except WrongChecksumError:
        return {"passphrase": "Checksum error"}

    except ValueError:
        return {"passphrase": "unknown word in the passphrase"}

    except WrongMnemonicLengthError:
        return {"passphrase": "Incorrect size of the passphrase"}


@app.get("/assets")
def get_nfts():
    '''
    Endpoint to view all the available assets

    '''
    return indexer_client.search_assets()

@app.get("/transaction/{account}")
def get_transactions(account: str):
    '''
    Endpoint to geet all the transactions for an account
    '''

    return indexer_client.search_transactions_by_address(account)


@app.get("/transaction/{transaction_ID}")
def get_txn_info(transaction_ID: str):
    '''
    Get an info on a transaction by the txn ID
    '''

    return indexer_client.transaction(transaction_ID)



