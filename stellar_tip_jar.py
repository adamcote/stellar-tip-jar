# Import the necessary modules from the stellar-sdk package
from stellar_sdk import Keypair, Server, TransactionBuilder, Network, Account
import requests

# 1. Generate a new Stellar keypair (public/private keys)
#    The public key is your "tip jar" address. The secret key is like your password—keep it safe!
keypair = Keypair.random()
public_key = keypair.public_key
secret_key = keypair.secret

print("Welcome to the Stellar Tip Jar!")
print("Your public address (share this to receive tips):")
print(public_key)
print("\nYour secret key (DO NOT share this!):")
print(secret_key)

# 2. Fund your account on the Stellar testnet using Friendbot (for demo/testing)
#    On mainnet, someone would need to send you at least 1 XLM to activate your account.
print("\nFunding your account on the Stellar testnet...")
response = requests.get(f"https://friendbot.stellar.org/?addr={public_key}")
if response.status_code == 200:
    print("Account funded successfully!")
else:
    print("Error funding account. Try again later.")
    exit(1)

# 3. Connect to the Stellar testnet server
server = Server("https://horizon-testnet.stellar.org")

# 4. Check your tip jar balance
def check_balance():
    # Fetch account details from the Stellar blockchain
    account = server.accounts().account_id(public_key).call()
    # The 'balances' field contains all assets (XLM and tokens) held by the account
    for balance in account['balances']:
        if balance['asset_type'] == 'native':
            print(f"\nYour tip jar balance: {balance['balance']} XLM")

check_balance()

# 5. (Optional) Show how to send a thank-you memo when someone tips
#    For demo, we'll send a small tip to ourselves with a memo.
def send_tip_with_memo(amount, memo_text):
    # Load the account from the blockchain
    account = server.load_account(public_key)
    # Build a transaction to send XLM to yourself with a memo
    transaction = (
        TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100
        )
        .add_text_memo(memo_text)  # Add a memo (thank you message)
        .append_payment_op(destination=public_key, amount=str(amount), asset_code="XLM")
        .build()
    )
    # Sign the transaction with your secret key
    transaction.sign(keypair)
    # Submit the transaction to the Stellar network
    response = server.submit_transaction(transaction)
    print(f"\nSent {amount} XLM with memo: '{memo_text}'")
    print("Transaction hash:", response['hash'])

# Uncomment the next line to send a thank-you tip to yourself
# send_tip_with_memo(0.00001, "Thank you for the tip!")

print("\nShare your public address to receive tips on the Stellar testnet!")
print("To check your balance again, just run this script.")

# END OF SCRIPT