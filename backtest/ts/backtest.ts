import { CCXT } from 'ccxt';
import { DataFrame } from 'pandas-js';
import { BacktestConfig } from './config';
import { PriceActionStrategy } from './strategy';
import { 
    OHLCV, 
    TradeEntry, 
    DataSummary, 
    Results, 
    TradeStats 
} from './types';

export class Backtester {
    private readonly config: BacktestConfig;
    private readonly strategy: PriceActionStrategy;
    private readonly exchange: CCXT;
    private results: Results = {};
    private dataSummary: Record<string, DataSummary> = {};
    private tradeHistory: Record<string, TradeEntry[]> = {};

    constructor(config: BacktestConfig) {
        this.config = config;
        this.strategy = new PriceActionStrategy();
        this.exchange = new CCXT.binance();
    }

    private async fetchData(symbol: string): Promise<DataFrame> {
        const startTimestamp = this.exchange.parse8601(this.config.startDate);
        const endTimestamp = this.exchange.parse8601(this.config.endDate);
        
        const ohlcv = await this.exchange.fetchOHLCV(
            symbol,
            this.config.timeframe,
            startTimestamp,
            1000
        );
        
        const df = new DataFrame(ohlcv as OHLCV[]);
        
        this.dataSummary[symbol] = {
            startDate: df.get('timestamp').min(),
            endDate: df.get('timestamp').max(),
            totalCandles: df.length
        };
        
        return df;
    }

    public async run(): Promise<Results> {
        let totalProfit = 0;

        for (const coin of this.config.coins) {
            const df = await this.fetchData(coin);
            const signalDf = this.strategy.calculateSignals(df);
            
            let balance = this.config.initialBalance;
            let position = 0;
            let trades = 0;
            let winningTrades = 0;
            this.tradeHistory[coin] = [];
            
            for (let i = 1; i < signalDf.length; i++) {
                const row = signalDf.iloc(i);
                
                if (row.get('signal') === 1 && position === 0) {
                    const entryPrice = row.get('close');
                    position = balance / entryPrice;
                    balance -= balance * this.config.commission;
                    trades++;
                    
                    const tradeEntry: Partial<TradeEntry> = {
                        type: 'BUY',
                        entryPrice,
                        entryDate: row.get('timestamp')
                    };
                    
                    this.processTradeExit(
                        coin,
                        tradeEntry,
                        row,
                        position,
                        balance,
                        winningTrades
                    );
                }
            }
            
            this.calculateResults(
                coin,
                balance,
                trades,
                winningTrades,
                totalProfit
            );
        }
        
        this.results['total'] = { totalProfit };
        return this.results;
    }

    private processTradeExit(
        coin: string,
        tradeEntry: Partial<TradeEntry>,
        row: Series,
        position: number,
        balance: number,
        winningTrades: number
    ): void {
        const exitPrice = row.get('close');
        const newBalance = position * exitPrice;
        const tradeProfit = newBalance - balance;
        
        if (tradeProfit > 0) winningTrades++;
        
        this.tradeHistory[coin].push({
            ...tradeEntry as TradeEntry,
            exitPrice,
            exitDate: row.get('timestamp'),
            profit: tradeProfit
        });
    }

    private calculateResults(
        coin: string,
        balance: number,
        trades: number,
        winningTrades: number,
        totalProfit: number
    ): void {
        const profit = balance - this.config.initialBalance;
        const profitPercentage = (profit / this.config.initialBalance) * 100;
        const winRate = trades > 0 ? (winningTrades / trades) * 100 : 0;
        const avgProfit = trades > 0 ? profit / trades : 0;
        
        this.results[coin] = {
            trades,
            profit,
            profitPercentage,
            winRate,
            avgProfitPerTrade: avgProfit
        };
        
        totalProfit += profit;
    }
}