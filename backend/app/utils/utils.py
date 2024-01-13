import os, sys
import base64
from algosdk.v2client import algod
from fastapi import FastAPI, HTTPException, status
from typing import Optional
from algosdk import account , encoding , mnemonic
from algosdk.transaction import PaymentTxn
from algosdk.transaction import AssetConfigTxn, AssetCreateTxn, AssetTransferTxn, AssetFreezeTxn, AssetOptInTxn
from algosdk.transaction import *
from algosdk.error import *
from algosdk.v2client import algod, indexer


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

algod_client=algod.AlgodClient("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","http://localhost:4001") #Initializing the algod client
indexer_client=indexer.IndexerClient("","http://localhost:8980") #initializing the validator




class Helpers:
    def __init__(self):
        pass

    def opt_in_to_nft(self, asset_id, public_key):
        try:
            sender_address = encoding.encode_address(public_key)
            params = algod_client.suggested_params()
                    
            note = "Opt-in to NFT certificate".encode()

            opt_in_txn = AssetTransferTxn(
                sender=sender_address,
                sp=params,
                index=asset_id,
                target=sender_address,
                amt=0,  # 0 Algos to opt-in
                close_remainder_to=sender_address,
                note=note,
            )

            signed_txn = opt_in_txn.sign("")

            # Submit the transaction to the Algorand network
            tx_id = algod_client.send_transaction(signed_txn)

            return {"status": "success", "transaction_id": tx_id}
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    # Define approved_transfers outside of the method
    approved_transfers = set()

    def approve_nft_transfer(self, public_key: str):
        if public_key not in self.approved_transfers:
            self.approved_transfers.add(public_key)
            return {"status": "success", "message": "NFT transfer approved for trainee"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transfer already approved")

    def check_transfer_status(self, public_key: str):
        # Simulate the status check logic
        if public_key in self.approved_transfers:
            return {"status": "approved", "message": "Your NFT transfer request has been approved"}
        else:
            return {"status": "pending", "message": "Your NFT transfer request is still pending approval"}
