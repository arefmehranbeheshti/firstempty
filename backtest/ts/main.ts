import { BacktestConfig } from './config';
import { Backtester } from './backtest';
import { Results, TradeStats } from './types';

async function main(): Promise<void> {
    const config = new BacktestConfig();
    const backtester = new Backtester(config);
    const results = await backtester.run();
    
    console.log("\n=== Data Summary ===");
    for (const [coin, data] of Object.entries(backtester.dataSummary)) {
        console.log(`\n${coin}:`);
        console.log(`Start Date: ${data.startDate}`);
        console.log(`End Date: ${data.endDate}`);
        console.log(`Total Candles: ${data.totalCandles}`);
        console.log(`Timeframe: ${config.timeframe}`);
    }
    
    console.log("\n=== Trade History ===");
    for (const [coin, trades] of Object.entries(backtester.tradeHistory)) {
        console.log(`\n${coin} Trades:`);
        for (const trade of trades) {
            console.log(`Type: ${trade.type}`);
            console.log(`Entry Price: $${trade.entryPrice.toFixed(2)}`);
            console.log(`Entry Date: ${trade.entryDate}`);
            console.log(`Exit Price: $${trade.exitPrice.toFixed(2)}`);
            console.log(`Exit Date: ${trade.exitDate}`);
            console.log(`Profit: $${trade.profit.toFixed(2)}`);
            console.log("---");
        }
    }
    
    console.log("\n=== Backtesting Results ===");
    for (const [coin, stats] of Object.entries(results)) {
        if (coin !== 'total') {
            const tradeStats = stats as TradeStats;
            console.log(`\n${coin}:`);
            console.log(`Number of trades: ${tradeStats.trades}`);
            console.log(`Profit: $${tradeStats.profit.toFixed(2)}`);
            console.log(`Profit percentage: ${tradeStats.profitPercentage.toFixed(2)}%`);
            console.log(`Win Rate: ${tradeStats.winRate.toFixed(2)}%`);
            console.log(`Average Profit per Trade: $${tradeStats.avgProfitPerTrade.toFixed(2)}`);
        }
    }
    
    console.log(`\nTotal Profit: $${(results.total as { totalProfit: number }).totalProfit.toFixed(2)}`);
}

if (require.main === module) {
    main().catch(console.error);
}