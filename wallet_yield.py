import os

from protocols.defillama import fetch_defillama_yields
from protocols.etherscan import get_token_balances as eth_balances
from protocols.snowtrace import get_avalanche_balances
from protocols.arbiscan import get_arbitrum_balances
from protocols.basescan import get_base_balances
from protocols.optimismscan import get_optimism_balances
from protocols.solscan import get_solana_balances


def get_wallet_yield(wallet: str, chain: str):
    chain = chain.lower()

    if chain == "ethereum":
        balances = eth_balances(wallet, os.getenv("ETHERSCAN_API_KEY"))
    elif chain == "avalanche":
        balances = get_avalanche_balances(wallet, os.getenv("SNOWTRACE_API_KEY"))
    elif chain == "arbitrum":
        balances = get_arbitrum_balances(wallet, os.getenv("ARBISCAN_API_KEY"))
    elif chain == "base":
        balances = get_base_balances(wallet, os.getenv("BASESCAN_API_KEY"))
    elif chain == "optimism":
        balances = get_optimism_balances(wallet, os.getenv("OPTIMISMSCAN_API_KEY"))
    elif chain == "solana":
        balances = get_solana_balances(wallet, os.getenv("HELIUS_API_KEY"))
    else:
        return {"error": f"❌ Unsupported chain '{chain}'"}

    if not balances:
        return {"error": "❌ No assets found for wallet"}

    yield_data = fetch_defillama_yields(chain)

    positions = []
    total_value = 0

    for token in balances:
        symbol = token['symbol']
        amount = token['amount']
        price = token['price_usd']
        token_value = amount * price

        # Find best APY
        yields = [y for y in yield_data if y['symbol'].lower() == symbol.lower()]
        best_yield = max(yields, key=lambda x: x.get('apy', 0), default=None)

        apy = best_yield['apy'] if best_yield else 0
        yearly_yield = token_value * (apy / 100)

        positions.append({
            "asset": symbol,
            "amount": amount,
            "value_usd": token_value,
            "apy": apy,
            "best_protocol": best_yield['protocol'] if best_yield else "N/A",
            "estimated_yield_per_year_usd": yearly_yield
        })

        total_value += token_value

    return {
        "wallet": wallet,
        "chain": chain,
        "total_value_usd": total_value,
        "positions": positions
    }