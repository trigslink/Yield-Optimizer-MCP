import requests
from utils.config import ETHERSCAN_API_KEY


def get_token_balances(wallet: str, api_key: str = None):
    """
    Fetch ERC-20 token balances for an Ethereum wallet using Etherscan API.

    Args:
        wallet (str): Ethereum wallet address.
        api_key (str, optional): API key for Etherscan. Defaults to env variable.

    Returns:
        list: List of tokens with symbol, amount, contract address, and price (placeholder).
    """
    api_key = api_key or ETHERSCAN_API_KEY  # ✅ Use provided API key or fallback

    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet,
        "page": 1,
        "offset": 10000,  # Fetch full transaction history
        "sort": "asc",
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Etherscan API Error: {e}")
        return []

    data = response.json().get("result", [])
    if not isinstance(data, list):
        print(f"❌ Unexpected API response: {data}")
        return []

    token_balances = {}
    wallet_lower = wallet.lower()

    for tx in data:
        try:
            symbol = tx.get('tokenSymbol', 'UNKNOWN')
            contract = tx.get('contractAddress')
            decimals = int(tx.get('tokenDecimal') or 18)
            value = int(tx.get('value') or 0)

            to_address = tx.get('to', '').lower()
            from_address = tx.get('from', '').lower()

            token_balances.setdefault(contract, {
                'symbol': symbol,
                'balance': 0,
                'decimals': decimals
            })

            if to_address == wallet_lower:
                token_balances[contract]['balance'] += value
            if from_address == wallet_lower:
                token_balances[contract]['balance'] -= value

        except Exception as e:
            print(f"⚠️ Error processing transaction: {e}")
            continue

    result = []
    for contract, data in token_balances.items():
        balance = data['balance'] / (10 ** data['decimals'])
        if balance > 0:
            result.append({
                "symbol": data['symbol'],
                "contract_address": contract,
                "amount": balance,
                "price_usd": 1.0  # ✅ Placeholder, can integrate price feed later
            })

    return result