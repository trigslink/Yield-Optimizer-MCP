import requests

def fetch_defillama_yields(chain: str):
    url = "https://yields.llama.fi/pools"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    pools = response.json().get("data", [])
    filtered = [
        {
            "protocol": pool['project'],
            "apy": pool.get('apy', 0),
            "symbol": pool['symbol'],
            "chain": pool['chain'],
            "tvlUsd": pool.get('tvlUsd', 0),
            "url": pool.get('url', '')
        }
        for pool in pools if pool['chain'].lower() == chain.lower()
    ]
    return filtered