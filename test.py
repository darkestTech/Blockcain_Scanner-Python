from web3 import Web3

RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/api key here "

print("🔌 Connecting to:", RPC_URL)
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    print("✅ Connected to Ethereum successfully!")
    print("Latest block number:", w3.eth.block_number)
else:
    print("❌ Failed to connect.")


#use this simple code to test connection to ethereum node if it works fine you can run the main scanner scripts