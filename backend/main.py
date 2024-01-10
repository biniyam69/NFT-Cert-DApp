import os, sys
from fastapi import FastAPI



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
