from typing import Dict, List
import ccxt
import pandas as pd
from datetime import datetime
from config import BacktestConfig
from strategy import PriceActionStrategy

class Backtester:
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.strategy = PriceActionStrategy()
        self.exchange = ccxt.binance()
        self.results: Dict[str, Dict] = {}
        self.data_summary: Dict[str, Dict] = {}
        self.trade_history: Dict[str, List] = {}
        
    def fetch_data(self, symbol: str) -> pd.DataFrame:
        start_timestamp = self.exchange.parse8601(self.config.start_date)
        end_timestamp = self.exchange.parse8601(self.config.end_date)
        
        ohlcv = self.exchange.fetch_ohlcv(
            symbol,
            timeframe=self.config.timeframe,
            since=start_timestamp,
            limit=1000
        )
        
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Store data summary
        self.data_summary[symbol] = {
            'start_date': df['timestamp'].min(),
            'end_date': df['timestamp'].max(),
            'total_candles': len(df),
        }
        
        return df.set_index('timestamp')
    
    def run(self) -> Dict[str, Dict]:
        total_profit = 0
        
        for coin in self.config.coins:
            df = self.fetch_data(coin)
            df = self.strategy.calculate_signals(df)
            
            balance = self.config.initial_balance
            position = 0
            trades = 0
            winning_trades = 0
            self.trade_history[coin] = []
            
            for i in range(1, len(df)):
                if df['signal'].iloc[i] == 1 and position == 0:  # Buy
                    entry_price = df['close'].iloc[i]
                    position = balance / entry_price
                    balance -= balance * self.config.commission
                    trades += 1
                    trade_entry = {
                        'type': 'BUY',
                        'entry_price': entry_price,
                        'entry_date': df.index[i],
                    }
                    
                elif df['signal'].iloc[i] == -1 and position > 0:  # Sell
                    exit_price = df['close'].iloc[i]
                    new_balance = position * exit_price
                    trade_profit = new_balance - balance
                    balance = new_balance - (new_balance * self.config.commission)
                    
                    if trade_profit > 0:
                        winning_trades += 1
                    
                    self.trade_history[coin].append({
                        **trade_entry,
                        'exit_price': exit_price,
                        'exit_date': df.index[i],
                        'profit': trade_profit,
                    })
                    
                    position = 0
            
            # Close any remaining position
            if position > 0:
                exit_price = df['close'].iloc[-1]
                new_balance = position * exit_price
                trade_profit = new_balance - balance
                balance = new_balance - (new_balance * self.config.commission)
                
                self.trade_history[coin].append({
                    **trade_entry,
                    'exit_price': exit_price,
                    'profit': trade_profit,
                    'date': df.index[-1]
                })
            
            profit = balance - self.config.initial_balance
            profit_percentage = (profit / self.config.initial_balance) * 100
            win_rate = (winning_trades / trades * 100) if trades > 0 else 0
            avg_profit = profit / trades if trades > 0 else 0
            
            self.results[coin] = {
                'trades': trades,
                'profit': profit,
                'profit_percentage': profit_percentage,
                'win_rate': win_rate,
                'avg_profit_per_trade': avg_profit
            }
            
            total_profit += profit
        
        self.results['total'] = {'total_profit': total_profit}
        return self.results
