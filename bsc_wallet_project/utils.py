#!/usr/bin/env python3
"""
Balance utilities
"""
from web3 import Web3
from transactions import ERC20_ABI, get_web3

def get_bnb_balance(address: str):
    """Get BNB balance in human format"""
    w3 = get_web3()
    balance_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
    balance_bnb = w3.from_wei(balance_wei, 'ether')
    print(f"💰 BNB Balance [{address}]: {float(balance_bnb):.6f} BNB")
    return float(balance_bnb)

def get_token_balance(address: str, contract_address: str):
    """Get BEP20 token balance"""
    w3 = get_web3()
    contract = w3.eth.contract(Web3.to_checksum_address(contract_address), abi=ERC20_ABI)
    
    decimals = contract.functions.decimals().call()
    raw_balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
    balance = raw_balance / (10 ** decimals)
    
    print(f"🎫 Token [{contract_address}]: {float(balance):.2f}")
    return float(balance)

if __name__ == "__main__":
    print("=== Balance Utils ===")
    get_bnb_balance("0xB49318939aBbe48A2DCBd10e289991324F5C4ba2")
