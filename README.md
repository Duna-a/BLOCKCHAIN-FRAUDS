# 🪙 Blockchain Token Checker

A powerful Python tool to search for cryptocurrency tokens across **major blockchain platforms** with detailed metadata including liquidity, holders, creation date, and exchange listings.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

### 🎯 Smart Filtering
- **Exact Match Search** - Only shows tokens that contain your search term in name or symbol
- **No False Positives** - Filters out unrelated results automatically
- **Multi-Platform** - Searches 7+ platforms simultaneously

### 📊 Comprehensive Token Data
- ✅ **Token Metadata** - Name, symbol, contract address, decimals
- ✅ **Market Data** - Price, market cap, volume, FDV
- ✅ **Liquidity Information** - Total liquidity in USD across DEXs
- ✅ **Holder Count** - Number of token holders
- ✅ **Creation Date** - When token/pair was created
- ✅ **Exchange Listings** - Where the token is listed
- ✅ **Supply Data** - Circulating, total, and max supply
- ✅ **Social Links** - Twitter, Telegram, Website (when available)
- ✅ **Price Changes** - 24h price change percentage

### 🌐 Supported Platforms

| Platform | Type | Networks | Data Provided |
|----------|------|----------|---------------|
| **DexScreener** | DEX Aggregator | Multi-chain | Price, Liquidity, Volume, Creation Date |
| **CoinGecko** | Market Tracker | Multi-chain | Market Cap, Supply, Genesis Date, Listings |
| **CoinMarketCap** | Market Tracker | Multi-chain | Rank, Price, Supply, Volume |
| **Birdeye** | Analytics | Solana | Holders, Liquidity, Price, Volume |
| **Pump.fun** | Meme Launchpad | Solana | Creator, Social Links, Description |
| **MEXC** | CEX | Multi-chain | Trading Pairs, Price, Volume |
| **GeckoTerminal** | DEX Tracker | Multi-chain | Pool Data, Liquidity, Creation Date |

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip or pip3

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/blockchain-token-checker.git
cd blockchain-token-checker
```

2. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

Or use the automated setup:
```bash
chmod +x run.sh
./run.sh
```

### Usage

**Run the script:**
```bash
python3 token_checker.py
```

**Or use the run script:**
```bash
./run.sh
```




## 📊 Sample Output Data

### Token Information Fields

| Field | Description | Example |
|-------|-------------|---------|
| **name** | Full token name | "Bonk" |
| **symbol** | Token ticker | "BONK" |
| **address** | Contract/mint address | "DezXAZ8z..." |
| **chain** | Blockchain network | "Solana", "Ethereum" |
| **price_usd** | Current USD price | 0.0000234 |
| **market_cap** | Total market cap | $1,234,567,890 |
| **liquidity_usd** | Total liquidity | $12,456,789 |
| **volume_24h** | 24h trading volume | $8,234,567 |
| **holder_count** | Number of holders | 456,789 |
| **genesis_date** | Launch date | "2022-12-25" |
| **listed_on** | Exchanges/DEXs | ["Raydium", "Orca"] |

## 💾 Data Export

Results can be saved to JSON format for programmatic use:

```json
{
  "dexscreener": [
    {
      "platform": "DexScreener",
      "name": "Bonk",
      "symbol": "BONK",
      "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
      "chain": "solana",
      "price_usd": "0.0000234",
      "liquidity_usd": 12456789.00,
      "volume_24h": 8234567.00,
      "holder_count": 456789
    }
  ],
  "coingecko": [...],
  "birdeye": [...]
}
```



## 🔍 Search Tips

**For best results:**
- ✅ Try both full name and symbol (e.g., "Bitcoin" and "BTC")
- ✅ Use exact spelling when possible
- ✅ Search by contract address for precise results
- ✅ Be aware that newly launched tokens may not appear on all platforms
- ✅ Case doesn't matter - searches are case-insensitive


## 📝 Requirements

```
requests>=2.31.0
```

All dependencies are listed in `requirements.txt`




