#!/usr/bin/env python3
"""
Phase 8: FastAPI REST API for BSC Wallet Operations
Run: uvicorn api:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wallet import generate_bsc_testnet_wallet
from transactions import send_bnb, transfer_token
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="BSC Testnet Wallet API")

class WalletRequest(BaseModel):
    pass

class BNBRequest(BaseModel):
    to_address: str
    amount: float

class TokenRequest(BaseModel):
    contract_address: str
    to_address: str
    amount: float

@app.get("/")
def root():
    return {"message": "🏦 BSC Testnet Wallet API", "status": "ready"}

@app.post("/generate_wallet")
def api_generate_wallet():
    """Generate BSC wallet"""
    wallet = generate_bsc_testnet_wallet()
    return {
        "success": True,
        "wallet": {
            "address": wallet["bsc_address"],
            "private_key": wallet["private_key"],
            "public_key": wallet["public_key"][:32] + "..."
        }
    }

@app.post("/send_bnb")
def api_send_bnb(req: BNBRequest):
    """Send BNB transaction"""
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    if not PRIVATE_KEY:
        raise HTTPException(400, "PRIVATE_KEY missing in .env")
    
    try:
        tx_hash = send_bnb(PRIVATE_KEY, req.to_address, req.amount)
        return {
            "success": True,
            "tx_hash": tx_hash,
            "explorer": f"https://testnet.bscscan.com/tx/{tx_hash}",
            "amount": req.amount
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/send_token")
def api_send_token(req: TokenRequest):
    """Send BEP-20 tokens"""
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    if not PRIVATE_KEY:
        raise HTTPException(400, "PRIVATE_KEY missing")
    
    try:
        tx_hash = transfer_token(PRIVATE_KEY, req.contract_address, req.to_address, req.amount)
        return {
            "success": True,
            "tx_hash": tx_hash,
            "explorer": f"https://testnet.bscscan.com/tx/{tx_hash}",
            "amount": req.amount
        }
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
