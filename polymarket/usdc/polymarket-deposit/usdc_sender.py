from web3 import Web3
from eth_account import Account
from config import POLYMARKET_BRIDGE_CONTRACT, RPC, USDC_CONTRACT

USDC_ABI = [
    {"constant": False,
     "inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
     "name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
    {"constant": True,
     "inputs":[{"name":"_owner","type":"address"}],
     "name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}
]

w3 = Web3(Web3.HTTPProvider(RPC))
token = w3.eth.contract(address=w3.to_checksum_address(USDC_CONTRACT), abi=USDC_ABI)

def send_all_usdc(private_key):
    try:
        acct = Account.from_key(private_key)
        sender = acct.address

        bal = token.functions.balanceOf(sender).call()
        if bal == 0:
            print(f"[SKIP] {sender} → No USDC")
            return

        cold = w3.to_checksum_address(POLYMARKET_BRIDGE_CONTRACT)
        print(f"[SEND] {sender} → {cold} | USDC: {bal/1e6}")

        nonce = w3.eth.get_transaction_count(sender)
        try:
            gas_est = token.functions.transfer(cold, bal).estimate_gas({"from": sender})
        except Exception:
            gas_est = 100000

        tx = token.functions.transfer(cold, bal).build_transaction({
            "from": sender,
            "nonce": nonce,
            "gas": int(gas_est * 1.2),
            "gasPrice": w3.eth.gas_price
        })

        # SIGN TX (robust)
        signed = w3.eth.account.sign_transaction(tx, private_key)

        raw_tx = None

        # various possible raw tx fields
        for attr in ("rawTransaction", "raw_transaction", "raw"):
            raw_tx = getattr(signed, attr, None)
            if raw_tx:
                break

        if raw_tx is None and isinstance(signed, dict):
            raw_tx = signed.get("rawTransaction") or signed.get("raw_transaction") or signed.get("raw") or signed.get("rawTx")

        # hex → bytes
        if isinstance(raw_tx, str):
            try:
                raw_tx = bytes.fromhex(raw_tx.replace("0x", ""))
            except Exception as e:
                print("[ERROR] Failed to decode raw tx hex:", e)
                return

        if raw_tx is None:
            print("[ERROR] Unable to extract raw transaction bytes from:", signed)
            return

        # SEND TX
        try:
            tx_hash = w3.eth.send_raw_transaction(raw_tx)
        except Exception as e:
            print("[ERROR] send_raw_transaction failed:", e)
            return

        # PRINT TX HASH
        try:
            print("TX HASH:", w3.to_hex(tx_hash))
        except:
            print("TX HASH (fallback):", tx_hash.hex() if hasattr(tx_hash, "hex") else str(tx_hash))

    except Exception as e:
        print("[ERROR]", e)
