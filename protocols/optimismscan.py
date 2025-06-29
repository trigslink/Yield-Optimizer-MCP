import requests
from utils.config import OPTIMISMSCAN_API_KEY


def get_optimism_balances(wallet: str, api_key: str = None):
    """
    Fetch ERC-20 token balances for an Optimism wallet using Optimism Etherscan API.

    Args:
        wallet (str): Optimism wallet address.
        api_key (str, optional): API key for OptimismScan. Defaults to env variable.

    Returns:
        list: List of tokens with symbol, amount, and placeholder price.
    """
    api_key = api_key or OPTIMISMSCAN_API_KEY  # ✅ Use provided API key or fallback

    url = "https://api-optimistic.etherscan.io/api"
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
        print(f"❌ HTTP Error: {e}")
        return []

    try:
        response_json = response.json()
    except Exception as e:
        print("❌ Invalid JSON response:", response.text)
        return []

    if response_json.get('status') != '1':
        print(f"❌ API Error: {response_json.get('message')} | Details: {response_json.get('result')}")
        return []

    data = response_json.get('result', [])
    if not isinstance(data, list):
        print("❌ Unexpected response format:", data)
        return []

    token_balances = {}
    for tx in data:
        symbol = tx.get('tokenSymbol', '').upper()
        decimal = int(tx.get('tokenDecimal', '18') or 18)

        try:
            value = int(tx.get('value', '0')) / (10 ** decimal)
        except Exception as e:
            print(f"⚠️ Error parsing value for {symbol}: {e}")
            continue

        token_balances[symbol] = token_balances.get(symbol, 0) + value

    token_prices = {symbol: 1.0 for symbol in token_balances}  # 🔗 Add price fetch later

    result = []
    for symbol, amount in token_balances.items():
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price_usd": token_prices.get(symbol, 1.0)
        })

    return result