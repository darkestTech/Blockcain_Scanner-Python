from web3 import Web3
from datetime import datetime
import argparse
import os
import sys
import csv

RPC_URL = "https://bnb-mainnet.g.alchemy.com/v2/apikey here"


print(f"🔌 Connecting to BSC node: {RPC_URL}")
try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("❌ Could not connect to BSC node. Check your RPC URL or internet.")
        sys.exit(1)
except Exception as e:
    print(f"⚠️ Error connecting to RPC: {e}")
    sys.exit(1)

parser = argparse.ArgumentParser(
    description="Scan BSC blocks before a given block for BNB transfers in a specific amount range."
)
parser.add_argument("--block", type=int, required=True, help="Anchor block number (e.g. 39876543)")
parser.add_argument("--min", type=float, required=True, help="Minimum BNB amount to match (e.g. 0.1587)")
parser.add_argument("--max", type=float, required=True, help="Maximum BNB amount to match (e.g. 0.165)")
parser.add_argument("--window", type=int, default=25, help="How many blocks before the target block to scan (default: 25)")
parser.add_argument("--save", action="store_true", help="Save results to matches_bsc.csv")
args = parser.parse_args()


target_block = args.block
blocks_before = args.window

start_block = max(0, target_block - blocks_before)
end_block = target_block

print(f"\n🔍 Scanning BSC blocks {start_block} → {end_block} (only before target)")
print(f"🎯 BNB Range: {args.min} → {args.max} BNB\n")


matches = []
timestamps = []

for blk_num in range(start_block, end_block + 1):
    try:
        block = w3.eth.get_block(blk_num, full_transactions=True)
        blk_time = datetime.utcfromtimestamp(block.timestamp)
        timestamps.append(blk_time)
        blk_time_str = blk_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"⚠️ Error fetching block {blk_num}: {e}")
        continue

    for tx in block.transactions:
        bnb_value = tx.value / 1e18
        if args.min <= bnb_value <= args.max:
            matches.append({
                "block": blk_num,
                "time": blk_time_str,
                "bnb": round(bnb_value, 9),
                "from": tx["from"],
                "to": tx.to,
                "hash": tx.hash.hex()
            })


if timestamps:
    first_time = timestamps[0]
    last_time = timestamps[-1]
    time_diff = (last_time - first_time).total_seconds()
    mins, secs = divmod(time_diff, 60)
    print(f"🕒 Time range covered: {int(mins)} min {int(secs)} sec "
          f"({first_time.strftime('%Y-%m-%d %H:%M:%S')} → {last_time.strftime('%Y-%m-%d %H:%M:%S')})\n")
else:
    print("⚠️ No blocks fetched successfully.\n")


if not matches:
    print("⚠️ No transactions found in that block range.")
else:
    print(f"✅ Found {len(matches)} matching transactions:\n")
    for m in matches:
        print(f"[{m['time']}] Block {m['block']} — {m['bnb']} BNB")
        print(f"   From: {m['from']}")
        print(f"   To:   {m['to']}")
        print(f"   Tx:   {m['hash']}\n")

    if args.save:
        with open("matches_bsc.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=matches[0].keys())
            writer.writeheader()
            writer.writerows(matches)
        print("📁 Results saved to matches_bsc.csv")

print("\n✅ BSC scan complete.")


#how to run:# python bsctx.py --block 39876543 --min 0.1587 --max 0.165 --window 25 --save(csvfileifneeded )