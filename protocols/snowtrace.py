import requests
from utils.config import SNOWTRACE_API_KEY


def get_avalanche_balances(wallet: str, api_key: str = None):
    """
    Fetch token balances for an Avalanche wallet using Snowtrace API.

    Args:
        wallet (str): Wallet address.
        api_key (str, optional): API key. Defaults to SNOWTRACE_API_KEY.

    Returns:
        list: List of tokens with symbol, amount, and USD price (dummy 1.0 for now).
    """
    api_key = api_key or SNOWTRACE_API_KEY  # ✅ Use passed API key or fallback

    url = "https://api.snowtrace.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet,
        "page": 1,
        "offset": 10000,  # ⬆️ Increased to fetch all txns
        "sort": "asc",
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Snowtrace API Error: {e}")
        return []

    try:
        response_json = response.json()
    except Exception as e:
        print(f"❌ Invalid JSON response: {e} | {response.text}")
        return []

    if response_json.get('status') != '1':
        print(f"❌ API Error: {response_json.get('message')} | Details: {response_json.get('result')}")
        return []

    data = response_json.get("result", [])
    if not isinstance(data, list):
        print(f"❌ Unexpected response format: {data}")
        return []

    token_balances = {}
    for tx in data:
        try:
            symbol = tx.get('tokenSymbol', '').upper()
            decimal = int(tx.get('tokenDecimal') or 18)
            value = int(tx.get('value', '0')) / (10 ** decimal)

            token_balances[symbol] = token_balances.get(symbol, 0) + value
        except Exception as e:
            print(f"⚠️ Error processing {symbol}: {e}")
            continue

    token_prices = {symbol: 1.0 for symbol in token_balances}  # 🔗 Placeholder for price feed

    result = []
    for symbol, amount in token_balances.items():
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price_usd": token_prices.get(symbol, 1.0)
        })

    return result