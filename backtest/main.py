from typing import Dict
from config import BacktestConfig
from backtest import Backtester
from datetime import datetime

def main() -> None:
    config = BacktestConfig()
    backtester = Backtester(config)
    results = backtester.run()
    
    print("\n=== Data Summary ===")
    for coin, data in backtester.data_summary.items():
        print(f"\n{coin}:")
        print(f"Start Date: {data['start_date']}")
        print(f"End Date: {data['end_date']}")
        print(f"Total Candles: {data['total_candles']}")
        print(f"Timeframe: {config.timeframe}")
        
    print("\n=== Trade History ===")
    for coin, trades in backtester.trade_history.items():
        print(f"\n{coin} Trades:")
        for trade in trades:
            print(f"Type: {trade['type']}")
            print(f"Entry Price: ${trade['entry_price']:.2f}")
            print(f"Exit Price: ${trade['exit_price']:.2f}")
            print(f"Profit: ${trade['profit']:.2f}")
            print(f"Date: {trade['date']}")
            print("---")
    
    print("\n=== Backtesting Results ===")
    for coin, stats in results.items():
        if coin != 'total':
            print(f"\n{coin}:")
            print(f"Number of trades: {stats['trades']}")
            print(f"Profit: ${stats['profit']:.2f}")
            print(f"Profit percentage: {stats['profit_percentage']:.2f}%")
            print(f"Win Rate: {stats['win_rate']:.2f}%")
            print(f"Average Profit per Trade: ${stats['avg_profit_per_trade']:.2f}")
    
    print(f"\nTotal Profit: ${results['total']['total_profit']:.2f}")

if __name__ == "__main__":
    main()
