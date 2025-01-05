# Circulating Supply API

A public API for calculating the circulating supply of a token by aggregating balances locked in specific addresses across multiple chains. This project uses Flask, asyncio, and Etherscan's API for efficient and scalable computation.

---

## Features

- **Endpoints**:
  - `/`: Returns the circulating supply (`result`), the list of locked addresses and the locked supply.
- **Asynchronous Fetching**:
  - Uses `asyncio` and `aiohttp` for concurrent API requests.
- **Rate Limiting**:
  - Prevents abuse using Redis-backed rate limiting with `Flask-Limiter`.
- **Caching**:
  - Reduces redundant calculations with a configurable caching duration.
- **Configurable**:
  - Fully customizable through environment variables.
- **Production-Ready**:
  - Integrated with Redis for distributed caching and rate limiting.

---

## API Endpoints

### `GET /`
Minimal endpoint for circulating supply.

#### Response
```json
{
    "result": 750000.0,
    "locked_addresses": [
        "0xe04f27eb70e025b78871a2ad7eabe85e61212761",
        "0xAnotherLockedAddress"
    ],
    "locked_supply": 10000
}

## Configuration

```
# Token Configuration
TOTAL_SUPPLY=1000000
CONTRACT_ADDRESS=0xYourTokenContractAddress
LOCKED_ADDRESSES=0xe04f27eb70e025b78871a2ad7eabe85e61212761,0xAnotherLockedAddress
TOKEN_DECIMALS=18

# API Configuration
API_VERSION=v1
ETHERSCAN_API_KEY=YourEtherscanAPIKey
CHAIN_IDS=8453  # Comma-separated chain IDs (e.g., 8453 for Base Mainnet)

# Caching and Rate Limiting
CACHE_DURATION=900  # Cache duration in seconds (default: 15 minutes)
RATE_LIMIT=5 per minute  # Requests allowed per minute

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/circulating-supply-api.git
   cd circulating-supply-api
   ```
2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Set up environment variables:

Create a .env file in the root directory and configure it based on the example below:

```bash
TOTAL_SUPPLY=1000000
CONTRACT_ADDRESS=0xYourTokenContractAddress
LOCKED_ADDRESSES=0xe04f27eb70e025b78871a2ad7eabe85e61212761,0xAnotherLockedAddress
TOKEN_DECIMALS=18
API_VERSION=v1
ETHERSCAN_API_KEY=YourEtherscanAPIKey
CHAIN_IDS=8453
CACHE_DURATION=900
RATE_LIMIT=5 per minute
REDIS_URL=redis://localhost:6379/0
```

4. Run Redis:

Make sure a Redis instance is running locally or use a cloud-hosted Redis.

5. Start the Flask app:

```bash
export FLASK_APP=api/index.py
flash run
```

6. Access the API:

- Open your browser or use a tool like curl or Postman to query the API.
- Example: http://localhost:5000/

## Deployment

### Deploying with Vercel

1. Install the Vercel CLI:

```bash
npm install -g vercel
```

2. Link your project:

```
vercel link
```

3. Add environment variables: Use the following command for each variable in the .env file:

```bash
vercel env add TOTAL_SUPPLY
vercel env add CONTRACT_ADDRESS
vercel env add LOCKED_ADDRESSES
vercel env add TOKEN_DECIMALS
vercel env add API_VERSION
vercel env add ETHERSCAN_API_KEY
vercel env add CHAIN_IDS
vercel env add CACHE_DURATION
vercel env add RATE_LIMIT
vercel env add REDIS_URL
```

Deploy the application:

```bash
vercel # for prod
vercel dev # for dev
```

## Contributing

Contributions are welcome!

## License

This project is licensed under the [GNU General Public License v3 (GPL v3)](https://www.gnu.org/licenses/gpl-3.0.html).

### Key Terms:
1. You may copy, distribute, and modify the software as long as you track changes/dates in source files.
2. Any modifications to this project must also be distributed under the GPL v3 license.
3. You must disclose source code when distributing the software, even in modified forms.

See the [LICENSE](LICENSE) file for full terms and conditions.
