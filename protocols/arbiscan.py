import requests
from utils.config import ARBISCAN_API_KEY


def get_arbitrum_balances(wallet: str, api_key: str = None):
    """
    Fetch token balances for an Arbitrum wallet using Arbiscan API.

    Args:
        wallet (str): Wallet address.
        api_key (str, optional): API key. Defaults to ARBISCAN_API_KEY.

    Returns:
        list: List of tokens with symbol, amount, and USD price (dummy 1.0 for now).
    """
    api_key = api_key or ARBISCAN_API_KEY  # ✅ Use passed key or fallback

    url = "https://api.arbiscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet,
        "page": 1,
        "offset": 100,
        "sort": "asc",
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Arbiscan API Error: {e}")
        return []

    try:
        data = response.json().get("result", [])
    except Exception as e:
        print(f"❌ Failed to parse JSON: {e}")
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

    token_prices = {symbol: 1.0 for symbol in token_balances}  # 🔗 Placeholder for price

    result = []
    for symbol, amount in token_balances.items():
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price_usd": token_prices.get(symbol, 1.0)
        })

    return result