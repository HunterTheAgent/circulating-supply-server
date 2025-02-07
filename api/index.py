from flask import Flask, jsonify
import os
import asyncio
import aiohttp
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

# Conditionally load .env file for local development
if not os.getenv("VERCEL"):
    from dotenv import load_dotenv
    load_dotenv()

# Flask app
app = Flask(__name__)

# Load configuration from environment
TOTAL_SUPPLY = int(os.getenv("TOTAL_SUPPLY", 0))
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
LOCKED_ADDRESSES = os.getenv("LOCKED_ADDRESSES", "")
if LOCKED_ADDRESSES is not None:
    LOCKED_ADDRESSES = LOCKED_ADDRESSES.split(",")
else:
    LOCKED_ADDRESSES = []
TOKEN_DECIMALS = int(os.getenv("TOKEN_DECIMALS", 18))
API_VERSION = os.getenv("API_VERSION", "v1")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
CHAIN_IDS = [int(chain) for chain in os.getenv("CHAIN_IDS", "").split(",")]
CACHE_DURATION = int(os.getenv("CACHE_DURATION", 900))  # Default 15 minutes
RATE_LIMIT = os.getenv("RATE_LIMIT", "5 per minute")  # Default 5 requests per minute
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Configure Redis client
redis_client = Redis.from_url(REDIS_URL)

# Configure rate limiter with Redis backend
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri=REDIS_URL,
    default_limits=[RATE_LIMIT],
)

# Configure caching
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": CACHE_DURATION})

# Etherscan base URL
ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"

# Semaphore for rate limiting (5 calls per minute)
semaphore = asyncio.Semaphore(5)


async def fetch_balance(session, address, chain_id):
    """
    Fetch token balance for a given address and chain ID from Etherscan API.
    """
    async with semaphore:  # Ensure only 5 calls per minute
        params = {
            "chainid": chain_id,
            "module": "account",
            "action": "tokenbalance",
            "contractaddress": CONTRACT_ADDRESS,
            "address": address,
            "tag": "latest",
            "apikey": ETHERSCAN_API_KEY,
        }
        async with session.get(ETHERSCAN_BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("status") == "1":
                    return int(data.get("result", 0))  # Return balance as integer
                else:
                    app.logger.warning(f"Error for {address} on chain {chain_id}: {data.get('message', 'Unknown error')}")
                    return 0
            else:
                app.logger.warning(f"HTTP error for {address} on chain {chain_id}: {response.status}")
                return 0


async def fetch_all_balances(addresses, chains):
    """
    Fetch balances for all addresses across all chains.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for address in addresses:
            for chain_id in chains:
                tasks.append(fetch_balance(session, address, chain_id))
        return await asyncio.gather(*tasks)


def calculate_circulating_supply():
    """
    Calculate the circulating supply by aggregating locked supply.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    balances = loop.run_until_complete(fetch_all_balances(LOCKED_ADDRESSES, CHAIN_IDS))

    # Aggregate locked supply
    locked_supply = sum(balances)
    locked_supply /= 10 ** TOKEN_DECIMALS
    return TOTAL_SUPPLY - locked_supply

@cache.cached(timeout=CACHE_DURATION, key_prefix="result_circulating_supply")
@limiter.limit(RATE_LIMIT)
@app.route(f'/', methods=['GET'])
def get_simple_circulating_supply():
    """
    Minimal endpoint for circulating supply.
    """
    try:
        circulating_supply = calculate_circulating_supply()
        return jsonify({"result": circulating_supply, "locked_addresses": LOCKED_ADDRESSES, "locked_supply": TOTAL_SUPPLY - circulating_supply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
