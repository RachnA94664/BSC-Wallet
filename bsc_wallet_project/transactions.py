
#!/usr/bin/env python3
"""
Send BNB on BSC Testnet
"""
from web3 import Web3
from dotenv import load_dotenv
import os
import time

load_dotenv()

RPC_URL = "https://data-seed-prebsc-1-s1.binance.org:8545/"
CHAIN_ID = 97  # BSC Testnet

def get_web3():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    print(f"✅ Connected to BSC Testnet: {w3.is_connected()}")
    print(f"Latest block: {w3.eth.block_number}")
    return w3

def send_bnb(private_key: str, to_address: str, amount_bnb: float):
    """
    Send BNB transaction on BSC Testnet
    """
    w3 = get_web3()
    account = w3.eth.account.from_key(private_key)
    
    print(f"\n📤 Sending {amount_bnb} BNB")
    print(f"From: {account.address}")
    print(f"To:   {to_address}")
    
    # Convert BNB to wei
    value = w3.to_wei(amount_bnb, 'ether')
    
    # Get nonce & gas
    nonce = w3.eth.get_transaction_count(account.address)
    gas_price = w3.eth.gas_price
    
    # Build transaction
    tx = {
        'nonce': nonce,
        'to': Web3.to_checksum_address(to_address),
        'value': value,
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': CHAIN_ID
    }
    
    # Estimate gas
    gas_estimate = w3.eth.estimate_gas({
        'from': account.address,
        'to': to_address,
        'value': value
    })
    tx['gas'] = gas_estimate
    print(f"Gas estimate: {gas_estimate}")
    
    # Sign & send
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"✅ TX HASH: {tx_hash.hex()}")
    
    # Wait for receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    print(f"✅ Confirmed in block: {receipt.blockNumber}")
    print(f"Gas used: {receipt.gasUsed}")
    
    return tx_hash.hex()

# ERC20 / BEP20 ABI (minimal)
ERC20_ABI = [
    {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}
]

def transfer_token(private_key: str, token_contract: str, to_address: str, amount_tokens: float):
    """
    Send BEP-20 tokens on BSC Testnet
    """
    w3 = get_web3()
    account = w3.eth.account.from_key(private_key)
    
    contract = w3.eth.contract(address=Web3.to_checksum_address(token_contract), abi=ERC20_ABI)
    
    decimals = contract.functions.decimals().call()
    amount_raw = int(amount_tokens * (10 ** decimals))
    
    print(f"\n🎫 SENDING {amount_tokens} tokens")
    print(f"Token: {token_contract}")
    print(f"From: {account.address} → To: {to_address}")
    
    nonce = w3.eth.get_transaction_count(account.address)
    
    tx = contract.functions.transfer(
        Web3.to_checksum_address(to_address),
        amount_raw
    ).build_transaction({
        'chainId': CHAIN_ID,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    # Estimate gas
    gas_estimate = w3.eth.estimate_gas(tx)
    tx['gas'] = gas_estimate
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    print(f"📄 Token TX: https://testnet.bscscan.com/tx/{tx_hash.hex()}")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Token transfer confirmed! Gas: {receipt.gasUsed}")
    
    return tx_hash.hex()

if __name__ == "__main__":
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    if PRIVATE_KEY:
        print("💰 Current balance check...")
        w3 = get_web3()
        balance = w3.from_wei(w3.eth.get_balance(w3.eth.account.from_key(PRIVATE_KEY).address), 'ether')
        print(f"Balance: {float(balance):.6f} BNB")
        
        # Send 0.0001 BNB to self (super cheap test)
        # send_bnb(PRIVATE_KEY, '0xB49318939aBbe48A2DCBd10e289991324F5C4ba2', 0.0001)
        print("✅ Ready for send_bnb() test!")
    else:
        print("❌ PRIVATE_KEY missing")
