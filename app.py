from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from wallet_yield import get_wallet_yield
from utils.llm_parser import parse_nlp_to_payload
import os


app = FastAPI(
    title="Yield Optimizer MCP",
    description="Fetch DeFi yield for wallets on Ethereum, Avalanche, Arbitrum, Optimism, Base, Solana using Natural Language or Structured input.",
    version="6.0.0"
)

SUPPORTED_CHAINS = ["ethereum", "avalanche", "arbitrum", "optimism", "base", "solana"]


class WalletYieldRequest(BaseModel):
    wallet: str | None = None
    chain: str | None = None
    openai_api_key: str | None = None
    model: str | None = "gpt-4o"
    input: str | None = None


@app.get("/")
def home():
    return {
        "message": "✅ Yield Optimizer MCP is live!",
        "usage": "POST /wallet-yield with {'wallet':..., 'chain':..., 'openai_api_key':...} OR {'input': 'Natural language', openai_api_key}",
        "supported_chains": SUPPORTED_CHAINS
    }


@app.post("/wallet-yield/")
async def wallet_yield(request: Request):
    data = await request.json()

    wallet = data.get("wallet")
    chain = (data.get("chain") or "").lower()

    # ✅ Read API Key and Model from body or fallback to ENV
    openai_api_key = data.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    model = data.get("model") or os.getenv("MODEL", "gpt-4o")

    if not openai_api_key:
        raise HTTPException(
            status_code=400,
            detail="❌ 'openai_api_key' is required either in request body or set in .env (ENV variable)."
        )

    # ✅ If NLP input is provided, parse it
    if "input" in data and data["input"]:
        try:
            parsed = parse_nlp_to_payload(data["input"], openai_api_key, model)
            wallet = parsed.get("wallet", wallet)
            chain = parsed.get("chain", chain).lower()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"❌ NLP parsing failed: {str(e)}"
            )

    if not wallet or not chain:
        raise HTTPException(
            status_code=400,
            detail="❌ 'wallet' and 'chain' are required fields."
        )

    if chain not in SUPPORTED_CHAINS:
        raise HTTPException(
            status_code=400,
            detail=f"❌ Unsupported chain '{chain}'. Supported chains are: {SUPPORTED_CHAINS}"
        )

    # ✅ Fetch yield data
    try:
        result = get_wallet_yield(wallet, chain)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"❌ Internal error fetching yield: {str(e)}"
        )

    if not result:
        raise HTTPException(status_code=404, detail="❌ No data found for this wallet.")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {"output": result}


@app.get("/metadata")
def metadata():
    return {
        "mcp_id": "yield_optimizer_mcp",
        "service_name": "Yield Optimizer MCP",
        "description": """
        Fetch DeFi wallet holdings with best yield APY across Ethereum, Avalanche, Arbitrum, Optimism, Base, and Solana.
        Supports natural language input or structured JSON input.

        JSON keys:
        - 'wallet': Wallet address (optional if using 'input')
        - 'chain': Blockchain name like 'ethereum' (optional if using 'input')
        - 'openai_api_key': OpenAI API Key for NLP parsing (optional if set in ENV)
        - 'model': OpenAI model like 'gpt-4o' (optional if set in ENV, defaults to 'gpt-4o')
        - 'input': Natural language query like 'Check yield for wallet 0xabc on ethereum'
        """,
        "https_uri": "https://association-hayes-serves-enhancing.trycloudflare.com",
        "endpoint": "https://association-hayes-serves-enhancing.trycloudflare.com/wallet-yield/",
        "method": "POST",
        "input_format": {
            "input": "Optional. Natural language like 'Check yield for wallet 0xabc on ethereum'.",
            "wallet": "Wallet address (optional if using 'input')",
            "chain": f"Blockchain name (one of {SUPPORTED_CHAINS}, optional if using 'input')",
            "openai_api_key": "Required if not set in .env (OPENAI_API_KEY).",
            "model": "OpenAI model like 'gpt-4o' (optional if not set in .env, defaults to gpt-4o)"
        },
        "output": "Returns wallet holdings, USD value, best APY yield, protocol, and estimated yearly yield."
    }