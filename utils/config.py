from dotenv import load_dotenv
import os

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
SNOWTRACE_API_KEY = os.getenv("SNOWTRACE_API_KEY")
ARBISCAN_API_KEY = os.getenv("ARBISCAN_API_KEY")
BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
OPTIMISMSCAN_API_KEY = os.getenv("OPTIMISMSCAN_API_KEY")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")


REQUIRED_KEYS = {
    "ETHERSCAN_API_KEY": ETHERSCAN_API_KEY,
    "SNOWTRACE_API_KEY": SNOWTRACE_API_KEY,
    "ARBISCAN_API_KEY": ARBISCAN_API_KEY,
    "BASESCAN_API_KEY": BASESCAN_API_KEY,
    "OPTIMISMSCAN_API_KEY": OPTIMISMSCAN_API_KEY,
    "HELIUS_API_KEY": HELIUS_API_KEY,
}

missing = [key for key, value in REQUIRED_KEYS.items() if not value]
if missing:
    print(f"⚠️ Warning: Missing API keys for {', '.join(missing)}")