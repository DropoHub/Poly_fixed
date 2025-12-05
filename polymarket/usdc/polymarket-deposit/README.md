# USDC Collector Bot (complete)

This repo contains scripts to sweep USDC from multiple wallets into a single cold wallet on Polygon.

IMPORTANT:
- Do NOT commit wallets.txt or any private keys to a public repo.
- Edit config.py to set RPC and COLD_WALLET if needed.

Quick start:
1. chmod +x install.sh
2. ./install.sh   (enter private key when prompted)
3. source venv/bin/activate
4. python3 run.py
