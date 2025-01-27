from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import numpy as np

@dataclass
class PriceActionStrategy:
    def calculate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        # Calculate technical indicators
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['rsi'] = self._calculate_rsi(df['close'], 14)
        df['atr'] = self._calculate_atr(df, 14)
        
        # Generate signals based on price action
        df['signal'] = 0
        df.loc[(df['sma_20'] > df['sma_50']) & 
               (df['rsi'] < 70) & 
               (df['close'] > df['sma_20']), 'signal'] = 1  # Buy
        
        df.loc[(df['sma_20'] < df['sma_50']) & 
               (df['rsi'] > 30) & 
               (df['close'] < df['sma_20']), 'signal'] = -1  # Sell
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _calculate_atr(self, df: pd.DataFrame, period: int) -> pd.Series:
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        return true_range.rolling(period).mean()