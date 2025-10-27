# 🧠 Blockchain Transaction Scanners

A lightweight pair of Python scripts to analyze recent **on-chain transactions** for Ethereum and BNB Smart Chain (BSC).  
You can search by **block number**, **amount range**, and **time window**, then automatically export results to CSV.

---

## 🚀 Features

✅ Connects to any Ethereum or BSC RPC (Alchemy, QuickNode, Ankr, or public nodes)  
✅ Scans a given number of blocks before a target block  
✅ Filters by **exact value range** (min/max ETH or BNB)  
✅ Displays **transaction details + real-world time window**  
✅ Optional CSV export for results  
✅ Lightweight & fast — no dependencies beyond `web3.py`

---

## 📁 Files

| File | Description |
|------|--------------|
| `eth_tx_scanner.py` | Scans Ethereum mainnet for ETH transfers |
| `bsc_tx_scanner.py` | Scans BSC mainnet for BNB transfers |
| `.gitignore` | Common ignored files |
| `README.md` | Project documentation |

---

## ⚙️ Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/blockchain-tx-scanners.git
cd blockchain-tx-scanners
