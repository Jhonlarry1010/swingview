#!/usr/bin/env python3
"""
Crypto Market Analyzer
Analyzes cryptocurrency market data and provides insights
"""

import json
from datetime import datetime
from statistics import mean, stdev
from typing import List, Dict, Any


class CryptoAnalyzer:
    """Analyzes cryptocurrency market data"""
    
    def __init__(self):
        self.coins_data = [
            {"name": "Bitcoin", "symbol": "BTC", "price": 42500, "change_24h": 2.5, "volume": 25000000000},
            {"name": "Ethereum", "symbol": "ETH", "price": 2250, "change_24h": 1.8, "volume": 12000000000},
            {"name": "Cardano", "symbol": "ADA", "price": 0.95, "change_24h": 3.2, "volume": 800000000},
            {"name": "Solana", "symbol": "SOL", "price": 150, "change_24h": 4.1, "volume": 2500000000},
            {"name": "Ripple", "symbol": "XRP", "price": 2.10, "change_24h": -1.2, "volume": 4200000000},
            {"name": "Polkadot", "symbol": "DOT", "price": 8.50, "change_24h": 2.9, "volume": 850000000},
        ]
    
    def get_top_gainers(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get top performing coins by 24h change"""
        sorted_coins = sorted(self.coins_data, key=lambda x: x['change_24h'], reverse=True)
        return sorted_coins[:limit]
    
    def get_top_losers(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get worst performing coins by 24h change"""
        sorted_coins = sorted(self.coins_data, key=lambda x: x['change_24h'])
        return sorted_coins[:limit]
    
    def calculate_market_stats(self) -> Dict[str, float]:
        """Calculate overall market statistics"""
        prices = [coin['price'] for coin in self.coins_data]
        changes = [coin['change_24h'] for coin in self.coins_data]
        volumes = [coin['volume'] for coin in self.coins_data]
        
        return {
            'avg_price': round(mean(prices), 2),
            'price_volatility': round(stdev(prices) if len(prices) > 1 else 0, 2),
            'avg_24h_change': round(mean(changes), 2),
            'total_volume': sum(volumes),
            'total_coins': len(self.coins_data)
        }
    
    def find_best_value(self) -> Dict[str, Any]:
        """Find coin with lowest price (best value)"""
        return min(self.coins_data, key=lambda x: x['price'])
    
    def analyze_volume(self) -> Dict[str, Any]:
        """Analyze trading volume distribution"""
        volumes = [coin['volume'] for coin in self.coins_data]
        high_volume = [c for c in self.coins_data if c['volume'] > mean(volumes)]
        low_volume = [c for c in self.coins_data if c['volume'] <= mean(volumes)]
        
        return {
            'avg_volume': round(mean(volumes), 0),
            'high_volume_coins': [c['symbol'] for c in high_volume],
            'low_volume_coins': [c['symbol'] for c in low_volume],
            'volume_range': {
                'min': min(volumes),
                'max': max(volumes)
            }
        }
    
    def generate_report(self) -> str:
        """Generate a comprehensive market report"""
        report = []
        report.append("=" * 60)
        report.append("CRYPTO MARKET ANALYSIS REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)
        report.append("")
        
        # Market Stats
        stats = self.calculate_market_stats()
        report.append("📊 MARKET STATISTICS")
        report.append(f"  • Total Coins Analyzed: {stats['total_coins']}")
        report.append(f"  • Average Price: ${stats['avg_price']}")
        report.append(f"  • Price Volatility: ${stats['price_volatility']}")
        report.append(f"  • Average 24h Change: {stats['avg_24h_change']}%")
        report.append(f"  • Total Trading Volume: ${stats['total_volume']:,.0f}")
        report.append("")
        
        # Top Gainers
        gainers = self.get_top_gainers(3)
        report.append("🚀 TOP GAINERS (24h)")
        for i, coin in enumerate(gainers, 1):
            report.append(f"  {i}. {coin['symbol']} - {coin['change_24h']:+.2f}% (${coin['price']})")
        report.append("")
        
        # Top Losers
        losers = self.get_top_losers(3)
        report.append("📉 TOP LOSERS (24h)")
        for i, coin in enumerate(losers, 1):
            report.append(f"  {i}. {coin['symbol']} - {coin['change_24h']:+.2f}% (${coin['price']})")
        report.append("")
        
        # Best Value
        best_value = self.find_best_value()
        report.append("💎 BEST VALUE COIN")
        report.append(f"  • {best_value['symbol']} - ${best_value['price']} ({best_value['change_24h']:+.2f}%)")
        report.append("")
        
        # Volume Analysis
        volume_analysis = self.analyze_volume()
        report.append("💰 VOLUME ANALYSIS")
        report.append(f"  • Average Volume: ${volume_analysis['avg_volume']:,.0f}")
        report.append(f"  • High Volume: {', '.join(volume_analysis['high_volume_coins'])}")
        report.append(f"  • Low Volume: {', '.join(volume_analysis['low_volume_coins'])}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """Main execution function"""
    analyzer = CryptoAnalyzer()
    
    # Print the comprehensive report
    print(analyzer.generate_report())
    
    # Additional insights
    print("\n📈 DETAILED COIN DATA:")
    print("-" * 60)
    for coin in analyzer.coins_data:
        print(f"{coin['symbol']:>5} | ${coin['price']:>10.2f} | {coin['change_24h']:>+6.2f}% | Vol: ${coin['volume']:>13,.0f}")


if __name__ == "__main__":
    main()
