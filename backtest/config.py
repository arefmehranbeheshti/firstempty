from dataclasses import dataclass
from typing import List

@dataclass
class BacktestConfig:
    coins: List[str] = ("BTC/USDT", "ETH/USDT", "BNB/USDT")
    timeframe: str = "1m"
    commission: float = 0.001  # 0.1%
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"
    initial_balance: float = 10000.0