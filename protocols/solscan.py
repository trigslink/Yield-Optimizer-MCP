import requests
from utils.config import HELIUS_API_KEY


def get_solana_balances(wallet: str, api_key: str = None):
    """
    Fetch token balances for a Solana wallet using the Helius API.

    Args:
        wallet (str): Wallet address.
        api_key (str, optional): Helius API key. Defaults to env key.

    Returns:
        list: List of tokens with symbol, amount, and USD price (placeholder).
    """
    api_key = api_key or HELIUS_API_KEY  # ✅ Use passed key or fallback

    url = f"https://api.helius.xyz/v0/addresses/{wallet}/balances?api-key={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Helius API Error: {e}")
        return []

    try:
        data = response.json()
    except Exception as e:
        print(f"❌ Invalid JSON response: {e} | {response.text}")
        return []

    tokens = data.get("tokens", [])
    if not tokens:
        print("⚠️ No tokens found for this wallet.")
        return []

    token_balances = {}
    for token in tokens:
        try:
            symbol = token.get("tokenSymbol", "UNKNOWN").upper()
            amount = float(token.get("amount", 0))
            token_balances[symbol] = token_balances.get(symbol, 0) + amount
        except Exception as e:
            print(f"⚠️ Error parsing amount for {symbol}: {e}")
            continue

    token_prices = {symbol: 1.0 for symbol in token_balances}  # 🔥 Placeholder prices

    result = []
    for symbol, amount in token_balances.items():
        result.append({
            "symbol": symbol,
            "amount": amount,
            "price_usd": token_prices.get(symbol, 1.0)
        })

    return result