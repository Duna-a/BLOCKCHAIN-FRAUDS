#!/usr/bin/env python3


import requests
from typing import Dict, List, Optional
import time
import json
from datetime import datetime


class EnhancedTokenChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_match(self, token_name: str, search_term: str) -> bool:
        """Check if token name matches search term (exact or contains)"""
        if not token_name:
            return False
        token_lower = token_name.lower()
        search_lower = search_term.lower()
        # Exact match or contains the search term
        return search_lower in token_lower
        
    def search_dexscreener(self, token_name: str) -> List[Dict]:
        """Search DexScreener for token matches with enhanced metadata"""
        print(f"🔍 Searching DexScreener for '{token_name}'...")
        results = []
        
        try:
            url = f"https://api.dexscreener.com/latest/dex/search/?q={token_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                for pair in pairs[:10]:
                    base_token = pair.get('baseToken', {})
                    name = base_token.get('name')
                    symbol = base_token.get('symbol')
                    
                    # Only include if name or symbol matches
                    if self.is_match(name, token_name) or self.is_match(symbol, token_name):
                        token_info = {
                            'platform': 'DexScreener',
                            'name': name,
                            'symbol': symbol,
                            'address': base_token.get('address'),
                            'chain': pair.get('chainId'),
                            'dex': pair.get('dexId'),
                            'price_usd': pair.get('priceUsd'),
                            'price_change_24h': pair.get('priceChange', {}).get('h24'),
                            'liquidity_usd': pair.get('liquidity', {}).get('usd'),
                            'volume_24h': pair.get('volume', {}).get('h24'),
                            'fdv': pair.get('fdv'),
                            'market_cap': pair.get('marketCap'),
                            'pair_created_at': pair.get('pairCreatedAt'),
                            'url': pair.get('url'),
                            'listed_on': [pair.get('dexId')]
                        }
                        results.append(token_info)
                    
        except Exception as e:
            print(f"❌ DexScreener error: {str(e)}")
            
        return results
    
    def search_birdeye(self, token_name: str) -> List[Dict]:
        """Search Birdeye for Solana tokens with metadata"""
        print(f"🔍 Searching Birdeye for '{token_name}'...")
        results = []
        
        try:
            url = f"https://public-api.birdeye.so/public/tokenlist?keyword={token_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                tokens = data.get('data', {}).get('tokens', [])
                
                for token in tokens[:10]:
                    name = token.get('name')
                    symbol = token.get('symbol')
                    address = token.get('address')
                    
                    # Only include if name or symbol matches
                    if self.is_match(name, token_name) or self.is_match(symbol, token_name):
                        token_info = {
                            'platform': 'Birdeye',
                            'name': name,
                            'symbol': symbol,
                            'address': address,
                            'chain': 'Solana',
                            'decimals': token.get('decimals'),
                            'logo': token.get('logoURI'),
                            'url': f"https://birdeye.so/token/{address}"
                        }
                        
                        # Try to get additional metadata
                        try:
                            meta_url = f"https://public-api.birdeye.so/public/token_overview?address={address}"
                            meta_response = self.session.get(meta_url, timeout=5)
                            if meta_response.status_code == 200:
                                meta = meta_response.json().get('data', {})
                                token_info.update({
                                    'price_usd': meta.get('price'),
                                    'liquidity_usd': meta.get('liquidity'),
                                    'volume_24h': meta.get('v24hUSD'),
                                    'market_cap': meta.get('mc'),
                                    'holder_count': meta.get('holder'),
                                })
                        except:
                            pass
                        
                        results.append(token_info)
                    
        except Exception as e:
            print(f"❌ Birdeye error: {str(e)}")
            
        return results
    
    def search_coingecko(self, token_name: str) -> List[Dict]:
        """Search CoinGecko with detailed token information"""
        print(f"🔍 Searching CoinGecko for '{token_name}'...")
        results = []
        
        try:
            url = f"https://api.coingecko.com/api/v3/search?query={token_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                coins = data.get('coins', [])
                
                for coin in coins[:10]:
                    name = coin.get('name')
                    symbol = coin.get('symbol')
                    
                    # Only include if name or symbol matches
                    if self.is_match(name, token_name) or self.is_match(symbol, token_name):
                        coin_id = coin.get('id')
                        token_info = {
                            'platform': 'CoinGecko',
                            'name': name,
                            'symbol': symbol,
                            'coingecko_id': coin_id,
                            'market_cap_rank': coin.get('market_cap_rank'),
                            'url': f"https://www.coingecko.com/en/coins/{coin_id}"
                        }
                        
                        # Try to get detailed info
                        try:
                            detail_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
                            detail_response = self.session.get(detail_url, timeout=5)
                            if detail_response.status_code == 200:
                                detail = detail_response.json()
                                market_data = detail.get('market_data', {})
                                
                                token_info.update({
                                    'price_usd': market_data.get('current_price', {}).get('usd'),
                                    'market_cap': market_data.get('market_cap', {}).get('usd'),
                                    'volume_24h': market_data.get('total_volume', {}).get('usd'),
                                    'price_change_24h': market_data.get('price_change_percentage_24h'),
                                    'circulating_supply': market_data.get('circulating_supply'),
                                    'total_supply': market_data.get('total_supply'),
                                    'genesis_date': detail.get('genesis_date'),
                                    'listed_on': [ex.get('name') for ex in detail.get('tickers', [])[:5]],
                                    'contract_address': detail.get('contract_address'),
                                    'description': detail.get('description', {}).get('en', '')[:200] if detail.get('description', {}).get('en') else None
                                })
                        except:
                            pass
                        
                        results.append(token_info)
                    
        except Exception as e:
            print(f"❌ CoinGecko error: {str(e)}")
            
        return results
    
    def search_pumpfun(self, token_name: str) -> List[Dict]:
        """Search Pump.fun for Solana meme tokens with metadata"""
        print(f"🔍 Searching Pump.fun for '{token_name}'...")
        results = []
        
        try:
            url = f"https://frontend-api.pump.fun/coins?searchQuery={token_name}&limit=10"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for token in data:
                    name = token.get('name')
                    symbol = token.get('symbol')
                    
                    # Only include if name or symbol matches
                    if self.is_match(name, token_name) or self.is_match(symbol, token_name):
                        token_info = {
                            'platform': 'Pump.fun',
                            'name': name,
                            'symbol': symbol,
                            'address': token.get('mint'),
                            'chain': 'Solana',
                            'creator': token.get('creator'),
                            'market_cap': token.get('market_cap'),
                            'created_timestamp': token.get('created_timestamp'),
                            'description': token.get('description'),
                            'twitter': token.get('twitter'),
                            'telegram': token.get('telegram'),
                            'website': token.get('website'),
                            'url': f"https://pump.fun/{token.get('mint')}"
                        }
                        results.append(token_info)
                    
        except Exception as e:
            print(f"❌ Pump.fun error: {str(e)}")
            
        return results
    
    def search_mexc(self, token_name: str) -> List[Dict]:
        """Search MEXC exchange for token listings"""
        print(f"🔍 Searching MEXC for '{token_name}'...")
        results = []
        
        try:
            # MEXC API endpoint for symbols
            url = "https://api.mexc.com/api/v3/exchangeInfo"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                symbols = data.get('symbols', [])
                
                # Search for matching tokens - exact or contains
                for symbol in symbols:
                    base_asset = symbol.get('baseAsset', '')
                    if self.is_match(base_asset, token_name):
                        token_info = {
                            'platform': 'MEXC',
                            'symbol': base_asset,
                            'trading_pair': symbol.get('symbol'),
                            'quote_asset': symbol.get('quoteAsset'),
                            'status': symbol.get('status'),
                            'listed_on': ['MEXC'],
                            'url': f"https://www.mexc.com/exchange/{symbol.get('symbol')}"
                        }
                        
                        # Try to get price data
                        try:
                            price_url = f"https://api.mexc.com/api/v3/ticker/24hr?symbol={symbol.get('symbol')}"
                            price_response = self.session.get(price_url, timeout=5)
                            if price_response.status_code == 200:
                                price_data = price_response.json()
                                token_info.update({
                                    'price_usd': price_data.get('lastPrice'),
                                    'price_change_24h': price_data.get('priceChangePercent'),
                                    'volume_24h': price_data.get('quoteVolume'),
                                })
                        except:
                            pass
                        
                        results.append(token_info)
                        if len(results) >= 5:  # Limit to 5 results
                            break
                    
        except Exception as e:
            print(f"❌ MEXC error: {str(e)}")
            
        return results
    
    def search_coinmarketcap(self, token_name: str) -> List[Dict]:
        """Search CoinMarketCap with enhanced data"""
        print(f"🔍 Searching CoinMarketCap for '{token_name}'...")
        results = []
        
        try:
            url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=20&search={token_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get('data', {}).get('cryptoCurrencyList', []):
                    name = item.get('name')
                    symbol = item.get('symbol')
                    
                    # Only include if name or symbol matches
                    if self.is_match(name, token_name) or self.is_match(symbol, token_name):
                        quotes = item.get('quotes', [{}])[0]
                        
                        token_info = {
                            'platform': 'CoinMarketCap',
                            'name': name,
                            'symbol': symbol,
                            'cmc_rank': item.get('cmcRank'),
                            'price_usd': quotes.get('price'),
                            'market_cap': quotes.get('marketCap'),
                            'volume_24h': quotes.get('volume24h'),
                            'price_change_24h': quotes.get('percentChange24h'),
                            'circulating_supply': item.get('circulatingSupply'),
                            'total_supply': item.get('totalSupply'),
                            'max_supply': item.get('maxSupply'),
                            'url': f"https://coinmarketcap.com/currencies/{item.get('slug')}"
                        }
                        results.append(token_info)
                        if len(results) >= 5:  # Limit to 5 results
                            break
                    
        except Exception as e:
            print(f"❌ CoinMarketCap error: {str(e)}")
            
        return results
    
    def search_geckoterminal(self, token_name: str) -> List[Dict]:
        """Search GeckoTerminal for DEX data"""
        print(f"🔍 Searching GeckoTerminal for '{token_name}'...")
        results = []
        
        try:
            url = f"https://api.geckoterminal.com/api/v2/search/pools?query={token_name}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for pool in data.get('data', []):
                    attrs = pool.get('attributes', {})
                    pool_name = attrs.get('name', '')
                    
                    # Only include if pool name matches
                    if self.is_match(pool_name, token_name):
                        token_info = {
                            'platform': 'GeckoTerminal',
                            'name': pool_name,
                            'address': attrs.get('address'),
                            'chain': attrs.get('network', '').upper(),
                            'dex': attrs.get('dex_id'),
                            'price_usd': attrs.get('base_token_price_usd'),
                            'liquidity_usd': attrs.get('reserve_in_usd'),
                            'volume_24h': attrs.get('volume_usd', {}).get('h24'),
                            'price_change_24h': attrs.get('price_change_percentage', {}).get('h24'),
                            'pool_created_at': attrs.get('pool_created_at'),
                            'url': f"https://www.geckoterminal.com/{attrs.get('network')}/pools/{attrs.get('address')}"
                        }
                        results.append(token_info)
                        if len(results) >= 5:  # Limit to 5 results
                            break
                    
        except Exception as e:
            print(f"❌ GeckoTerminal error: {str(e)}")
            
        return results
    
    def search_all(self, token_name: str) -> Dict[str, List[Dict]]:
        """Search all platforms for the token"""
        print(f"\n{'='*60}")
        print(f"🚀 Searching for token: {token_name}")
        print(f"{'='*60}\n")
        
        all_results = {
            'dexscreener': [],
            'birdeye': [],
            'coingecko': [],
            'pumpfun': [],
            'mexc': [],
            'coinmarketcap': [],
            'geckoterminal': []
        }
        
        # Search each platform with delays to avoid rate limiting
        all_results['dexscreener'] = self.search_dexscreener(token_name)
        time.sleep(1)
        
        all_results['birdeye'] = self.search_birdeye(token_name)
        time.sleep(1)
        
        all_results['coingecko'] = self.search_coingecko(token_name)
        time.sleep(1)
        
        all_results['pumpfun'] = self.search_pumpfun(token_name)
        time.sleep(1)
        
        all_results['mexc'] = self.search_mexc(token_name)
        time.sleep(1)
        
        all_results['coinmarketcap'] = self.search_coinmarketcap(token_name)
        time.sleep(1)
        
        all_results['geckoterminal'] = self.search_geckoterminal(token_name)
        
        return all_results
    
    def display_results(self, results: Dict[str, List[Dict]]):
        """Display formatted results"""
        total_found = sum(len(v) for v in results.values())
        
        print(f"\n{'='*60}")
        print(f"📊 SEARCH RESULTS - Found {total_found} total matches")
        print(f"{'='*60}\n")
        
        if total_found == 0:
            print("❌ No tokens found matching your search.")
            print("\n💡 Try:")
            print("   • Different spelling or token symbol")
            print("   • Searching by contract address if you have it")
            print("   • Checking these explorers manually:")
            print("     - Etherscan: https://etherscan.io/tokens")
            print("     - BSCScan: https://bscscan.com/tokens")
            print("     - Solscan: https://solscan.io")
            print("     - OKLink: https://www.oklink.com")
            return
        
        for platform, tokens in results.items():
            if tokens:
                print(f"\n{'─'*60}")
                print(f"🔹 {platform.upper()} ({len(tokens)} results)")
                print(f"{'─'*60}")
                
                for i, token in enumerate(tokens, 1):
                    print(f"\n  #{i}")
                    for key, value in token.items():
                        if value is not None and key != 'description':
                            # Format large numbers
                            if isinstance(value, (int, float)) and value > 1000:
                                if key in ['liquidity_usd', 'volume_24h', 'market_cap', 'fdv']:
                                    value = f"${value:,.2f}"
                                elif key in ['supply', 'circulating_supply', 'total_supply', 'max_supply']:
                                    value = f"{value:,.0f}"
                                elif key == 'holder_count':
                                    value = f"{value:,}"
                            
                            # Format timestamps
                            if key in ['pair_created_at', 'pool_created_at', 'created_timestamp']:
                                try:
                                    if isinstance(value, (int, float)):
                                        dt = datetime.fromtimestamp(value / 1000 if value > 10000000000 else value)
                                        value = dt.strftime("%Y-%m-%d %H:%M:%S")
                                except:
                                    pass
                            
                            # Format lists
                            if isinstance(value, list):
                                value = ', '.join(str(v) for v in value if v)
                            
                            print(f"    {key.replace('_', ' ').title()}: {value}")
                    
                    # Show description if available
                    if token.get('description'):
                        desc = token['description']
                        if len(desc) > 150:
                            desc = desc[:150] + "..."
                        print(f"    Description: {desc}")
        
        # Add helpful links at the end
        print(f"\n{'='*60}")
        print("💡 TIP: For more detailed info, also check:")
        print("   • Etherscan (ETH): https://etherscan.io/tokens")
        print("   • BSCScan (BSC): https://bscscan.com/tokens") 
        print("   • Solscan (Solana): https://solscan.io")
        print("   • OKLink (Multi-chain): https://www.oklink.com")
        print(f"{'='*60}\n")
    
    def save_results(self, results: Dict[str, List[Dict]], filename: str = "token_results.json"):
        """Save results to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")


def main():
    """Main function to run the token checker"""
    checker = EnhancedTokenChecker()
    
    print("\n" + "="*60)
    print("🪙  ENHANCED BLOCKCHAIN TOKEN CHECKER")
    print("="*60)
    print("\nSearches across 7 platforms:")
    print("  • DexScreener (Multi-chain)")
    print("  • CoinGecko & CoinMarketCap (Market Data)")
    print("  • Birdeye (Solana)")
    print("  • Pump.fun (Solana Meme Tokens)")
    print("  • MEXC Exchange")
    print("  • GeckoTerminal (DEX Data)")

    print("="*60 + "\n")
    
    while True:
        token_name = input("Enter token name (or 'quit' to exit): ").strip()
        
        if token_name.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not token_name:
            print("⚠️  Please enter a token name.")
            continue
        
        # Search all platforms
        results = checker.search_all(token_name)
        
        # Display results
        checker.display_results(results)
        
        # Ask if user wants to save results
        save = input("\nSave results to JSON? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"{token_name.replace(' ', '_')}_results.json"
            checker.save_results(results, filename)
        
        print("\n" + "-"*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
