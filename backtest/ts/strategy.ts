import { DataFrame, Series } from 'pandas-js';

export class PriceActionStrategy {
    public calculateSignals(df: DataFrame): DataFrame {
        // Calculate technical indicators
        df.set('sma20', this.calculateSMA(df.get('close'), 20));
        df.set('sma50', this.calculateSMA(df.get('close'), 50));
        df.set('rsi', this.calculateRSI(df.get('close'), 14));
        df.set('atr', this.calculateATR(df, 14));
        
        // Generate signals
        df.set('signal', 0);
        
        // Buy conditions
        const buyCondition = df.get('sma20')
            .gt(df.get('sma50'))
            .and(df.get('rsi').lt(70))
            .and(df.get('close').gt(df.get('sma20')));
            
        // Sell conditions
        const sellCondition = df.get('sma20')
            .lt(df.get('sma50'))
            .and(df.get('rsi').gt(30))
            .and(df.get('close').lt(df.get('sma20')));
            
        df.loc[buyCondition].set('signal', 1);
        df.loc[sellCondition].set('signal', -1);
        
        return df;
    }

    private calculateSMA(series: Series, period: number): Series {
        return series.rolling(period).mean();
    }

    private calculateRSI(prices: Series, period: number): Series {
        const delta = prices.diff();
        const gain = delta.where(delta.gt(0), 0).rolling(period).mean();
        const loss = delta.where(delta.lt(0), 0).abs().rolling(period).mean();
        const rs = gain.div(loss);
        return new Series(100 - (100 / (1 + rs.values)));
    }

    private calculateATR(df: DataFrame, period: number): Series {
        const highLow = df.get('high').sub(df.get('low'));
        const highClose = df.get('high').sub(df.get('close').shift(1)).abs();
        const lowClose = df.get('low').sub(df.get('close').shift(1)).abs();
        
        const trueRange = highLow
            .max(highClose)
            .max(lowClose);
            
        return trueRange.rolling(period).mean();
    }
}