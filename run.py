import time
import os
from usdc_sender import send_all_usdc

# wallets file is stored inside polymarket/usdc/polymarket-deposit per project layout
WALLETS_PATH = os.path.join(os.path.dirname(__file__), "polymarket", "usdc", "polymarket-deposit", "wallets.txt")

def main():
    if not os.path.exists(WALLETS_PATH):
        print("Wallets file not found at:", WALLETS_PATH)
        return

    with open(WALLETS_PATH) as f:
        keys = [x.strip() for x in f if x.strip()]

    print(f"Total wallets loaded: {len(keys)}")

    for key in keys:
        send_all_usdc(key)
        time.sleep(1)

if __name__ == "__main__":
    main()
