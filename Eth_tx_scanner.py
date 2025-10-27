from web3 import Web3
from datetime import datetime
import argparse
import os
import sys
import csv

RPC_URL = os.getenv("ETH_RPC") or "https://eth-mainnet.g.alchemy.com/v2/your api key here"

print(f"🔌 Connecting to Ethereum node: {RPC_URL}")
try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Could not connect to Ethereum node. Check your RPC URL or internet.")
        sys.exit(1)
except Exception as e:
    print(f"⚠️ Error connecting to RPC: {e}")
    sys.exit(1)


parser = argparse.ArgumentParser(
    description="Scan Ethereum blocks before a given block for ETH transfers in a specific amount range."
)
parser.add_argument("--block", type=int, required=True, help="Anchor block number (e.g. 23654513)")
parser.add_argument("--min", type=float, required=True, help="Minimum ETH amount to match (e.g. 0.1587)")
parser.add_argument("--max", type=float, required=True, help="Maximum ETH amount to match (e.g. 0.165)")
parser.add_argument("--window", type=int, default=25, help="How many blocks before the target block to scan (default: 25)")
parser.add_argument("--save", action="store_true", help="Save results to matches.csv")
args = parser.parse_args()


target_block = args.block
blocks_before = args.window

start_block = max(0, target_block - blocks_before)
end_block = target_block

print(f"\n🔍 Scanning blocks {start_block} → {end_block} (only before target)")
print(f"🎯 ETH Range: {args.min} → {args.max} ETH\n")


matches = []

for blk_num in range(start_block, end_block + 1):
    try:
        block = w3.eth.get_block(blk_num, full_transactions=True)
        blk_time = datetime.utcfromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"⚠️ Error fetching block {blk_num}: {e}")
        continue

    for tx in block.transactions:
        eth_value = tx.value / 1e18
        if args.min <= eth_value <= args.max:
            matches.append({
                "block": blk_num,
                "time": blk_time,
                "eth": round(eth_value, 9),
                "from": tx["from"],
                "to": tx.to,
                "hash": tx.hash.hex()
            })


if not matches:
    print("⚠️ No transactions found in that block range.")
else:
    print(f"✅ Found {len(matches)} matching transactions:\n")
    for m in matches:
        print(f"[{m['time']}] Block {m['block']} — {m['eth']} ETH")
        print(f"   From: {m['from']}")
        print(f"   To:   {m['to']}")
        print(f"   Tx:   {m['hash']}\n")

    if args.save:
        with open("matches.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=matches[0].keys())
            writer.writeheader()
            writer.writerows(matches)
        print("📁 Results saved to matches.csv")

print("\n✅ Scan complete.")


## how to run
#python eth_tx_scanner.py --block 23654513 --min 0.15869697 --max 0.165 --window 25
#block number ---- amount with range --- window for how many blocks before the target block to scan