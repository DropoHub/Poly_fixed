# USDC Collector Bot (complete)

This repo contains scripts to sweep USDC from multiple wallets into a single polybridge contract address on Polygon.

IMPORTANT:
- Do NOT commit wallets.txt or any private keys to a public repo.
- Edit `polymarket/usdc/polymarket-deposit/config.py` to set RPC, `POLYMARKET_BRIDGE_CONTRACT` and `USDC_CONTRACT` if needed.

Project layout:
- `install.sh` and `run.py` remain in repository root.
- All runtime files (config.py, wallets.txt, usdc_sender.py, debug_balance.py, dry_build.py, README.md) are inside `polymarket/usdc/polymarket-deposit`.

Quick start:
1. chmod +x install.sh
2. ./install.sh   (enter private key when prompted — this will be saved to polymarket/usdc/polymarket-deposit/wallets.txt)
3. source venv/bin/activate
4. python3 run.py
