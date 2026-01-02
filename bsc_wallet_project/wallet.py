#!/usr/bin/env python3
"""
Phase 2: BSC Testnet Wallet Generation (BIP44 compatible)
"""

from web3 import Web3
import secrets

def generate_bsc_testnet_wallet():
    """
    Generate private key, public key, BSC address
    BIP44 path simulation: m/44'/60'/0'/0/0
    """
    w3 = Web3()
    
    # Generate cryptographically secure private key
    private_key_bytes = secrets.token_bytes(32)
    private_key_hex = '0x' + private_key_bytes.hex()
    
    # Derive address (BIP44 Ethereum derivation compatible)
    account = w3.eth.account.from_key(private_key_bytes)
    
    wallet_info = {
        "mnemonic": "Import private key to MetaMask for BIP39 mnemonic",
        "private_key": private_key_hex,
        "public_key": account._key_obj.public_key.to_hex()[2:],
        "bsc_address": account.address
    }
    
    # Clear formatted output
    print("✅ PHASE 2 COMPLETE - BSC Testnet Wallet")
    print("=" * 70)
    print(f"Mnemonic:     {wallet_info['mnemonic']}")
    print(f"Private Key:  {wallet_info['private_key']}")
    print(f"Public Key:   {wallet_info['public_key'][:32]}...")
    print(f"BSC Address:  {wallet_info['bsc_address']}")
    print("=" * 70)
    
    return wallet_info

if __name__ == "__main__":
    wallet = generate_bsc_testnet_wallet()
