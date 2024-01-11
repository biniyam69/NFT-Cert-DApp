from pydantic import BaseModel

class Transaction(BaseModel):
    sender_address: str
    reciever_address: str
    paraphrase: str
    amount: int
    note: str

class Asset(BaseModel):
    sender:str
    asset_name:str
    unit:str
    total:int
    default_frozen:bool
    decimals:int
    url:str
    manager:str
    reserve:str
    freeze:str
    clawback:str
    passphrase: str
