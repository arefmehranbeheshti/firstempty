export interface OHLCV {
    timestamp: Date;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

export interface TradeEntry {
    type: 'BUY' | 'SELL';
    entryPrice: number;
    entryDate: Date;
    exitPrice: number;
    exitDate: Date;
    profit: number;
}

export interface DataSummary {
    startDate: Date;
    endDate: Date;
    totalCandles: number;
}

export interface TradeStats {
    trades: number;
    profit: number;
    profitPercentage: number;
    winRate: number;
    avgProfitPerTrade: number;
}

export interface Results {
    [key: string]: TradeStats | { totalProfit: number };
}