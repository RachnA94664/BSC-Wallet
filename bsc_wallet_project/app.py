#!/usr/bin/env python3
"""
BSC Testnet Wallet - Streamlit UI (ERROR-FREE)
Run: streamlit run app.py
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Local imports (fixed path)
from wallet import generate_bsc_testnet_wallet
from transactions import send_bnb, transfer_token, get_web3
from utils import get_bnb_balance
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="🏦 BSC Wallet", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
.main-header {font-size: 3rem; color: #1f77b4;}
.metric-card {background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🏦 BSC Testnet Wallet Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Navigation
st.sidebar.title("📱 Navigation")
page = st.sidebar.selectbox("Choose Action:", 
    ["🔑 Generate Wallet", "💰 Check Balance", "📤 Send BNB", "🎫 Send Token"])

PRIVATE_KEY = os.getenv('PRIVATE_KEY', "")
WALLET_ADDR = "0xB49318939aBbe48A2DCBd10e289991324F5C4ba2"

# Page 1: Generate Wallet
if page == "🔑 Generate Wallet":
    st.header("🎲 Generate New BSC Testnet Wallet")
    col1, col2 = st.columns([1,3])
    
    with col1:
        if st.button("🔥 GENERATE WALLET", type="primary", use_container_width=True):
            with st.spinner("🧠 Generating BIP44 wallet..."):
                wallet = generate_bsc_testnet_wallet()
                st.session_state.wallet = wallet
                st.success("✅ Wallet Generated Successfully!")
                st.balloons()
    
    if 'wallet' in st.session_state:
        with col2:
            st.markdown("**📋 Wallet Details:**")
            st.code(f"""
🆔 Address: {st.session_state.wallet['bsc_address']}
🔑 Private Key: {st.session_state.wallet['private_key']}
📝 Mnemonic: {st.session_state.wallet['mnemonic']}
🔓 Public Key: {st.session_state.wallet['public_key'][:32]}...
            """)
            st.warning("⚠️ **SAVE PRIVATE KEY SECURELY - Cannot recover!**")

# Page 2: Check Balance
elif page == "💰 Check Balance":
    st.header("💎 Check Wallet Balances")
    col1, col2 = st.columns(2)
    
    with col1:
        address = st.text_input("Wallet Address", value=WALLET_ADDR, help="Enter BSC Testnet address")
        if st.button("🔍 Check BNB Balance", type="primary"):
            with st.spinner("Fetching from BSC Testnet..."):
                try:
                    balance = get_bnb_balance(address)
                    st.metric("BNB Balance", f"{balance:.8f} BNB", delta=None)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with col2:
        st.info("💡 **Faucet**: [Get Test BNB](https://testnet.bnbchain.org/faucet-smart)")

# Page 3: Send BNB
elif page == "📤 Send BNB":
    st.header("🚀 Send Native BNB")
    
    if not PRIVATE_KEY:
        st.error("❌ **PRIVATE_KEY missing!** Add to `.env` file")
        st.info("`PRIVATE_KEY=0xyourprivatekeyhere`")
    else:
        col1, col2 = st.columns(2)
        with col1:
            to_address = st.text_input("Recipient Address", help="BSC Testnet address")
        with col2:
            amount = st.number_input("Amount (BNB)", min_value=0.00001, value=0.001, step=0.0001)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 SEND BNB", type="primary", use_container_width=True):
                if not to_address:
                    st.warning("⚠️ Enter recipient address")
                else:
                    with st.spinner("📡 Broadcasting transaction..."):
                        try:
                            tx_hash = send_bnb(PRIVATE_KEY, to_address, amount)
                            st.success("✅ **BNB SENT SUCCESSFULLY!**")
                            st.balloons()
                            st.markdown(f"🔗 [View Transaction](https://testnet.bscscan.com/tx/{tx_hash})")
                            st.code(tx_hash)
                        except Exception as e:
                            st.error(f"❌ Transaction failed: {str(e)}")

# Page 4: Send Token
elif page == "🎫 Send Token":
    st.header("🔄 Send BEP-20 Token")
    
    if not PRIVATE_KEY:
        st.error("❌ **PRIVATE_KEY missing!** Add to `.env`")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            token_contract = st.text_input("Token Contract Address", 
                placeholder="0x...", help="BEP-20 contract address")
        with col2:
            to_address = st.text_input("Recipient Address")
        with col3:
            amount = st.number_input("Token Amount", min_value=0.01, value=1.0, step=0.01)
        
        if st.button("🔄 SEND TOKEN", type="primary", use_container_width=True):
            if not all([token_contract, to_address]):
                st.warning("⚠️ Fill all fields")
            else:
                with st.spinner("📡 Sending tokens..."):
                    try:
                        tx_hash = transfer_token(PRIVATE_KEY, token_contract, to_address, amount)
                        st.success("✅ **TOKEN TRANSFER SUCCESS!**")
                        st.balloons()
                        st.markdown(f"🔗 [View on BscScan](https://testnet.bscscan.com/tx/{tx_hash})")
                        st.code(tx_hash)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("[**Faucet**](https://testnet.bnbchain.org/faucet-smart)")
with col2:
    st.markdown("[**Explorer**](https://testnet.bscscan.com)")
with col3:
    st.markdown("**RPC:** data-seed-prebsc-1-s1.binance.org:8545")

st.markdown("***Built with Streamlit + Web3.py | BSC Testnet Assignment***")

