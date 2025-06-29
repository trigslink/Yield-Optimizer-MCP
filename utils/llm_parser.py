import re

def parse_nlp_to_payload(user_input: str, openai_api_key: str = None, model: str = "gpt-4o") -> dict:
    """
    Parses natural language input like
    "Check yield for wallet 0xabc... on Ethereum"
    into {'wallet': ..., 'chain': ...}

    Args:
        user_input (str): Natural language input.
        openai_api_key (str): OpenAI key (not used in this regex-based parser).
        model (str): Model name (not used in this regex-based parser).

    Returns:
        dict: Extracted wallet and chain.
    """
    user_input = user_input.lower()

    # ✅ Find wallet (starts with 0x... for EVM)
    wallet_match = re.search(r"0x[a-fA-F0-9]{40}", user_input)
    wallet = wallet_match.group(0) if wallet_match else None

    # ✅ Find chain name
    chains = ["ethereum", "avalanche", "arbitrum", "optimism", "base", "solana"]
    chain = next((c for c in chains if c in user_input), None)

    if not wallet:
        raise ValueError("❌ Wallet address not found in input.")

    if not chain:
        raise ValueError("❌ Chain not found in input.")

    return {
        "wallet": wallet,
        "chain": chain,
    }