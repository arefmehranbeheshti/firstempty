interface BacktestConfigProps {
    coins: string[];
    timeframe: string;
    commission: number;
    startDate: string;
    endDate: string;
    initialBalance: number;
}

export class BacktestConfig {
    public readonly coins: string[];
    public readonly timeframe: string;
    public readonly commission: number;
    public readonly startDate: string;
    public readonly endDate: string;
    public readonly initialBalance: number;

    constructor(props?: Partial<BacktestConfigProps>) {
        this.coins = props?.coins ?? ["BTC/USDT", "ETH/USDT", "BNB/USDT"];
        this.timeframe = props?.timeframe ?? "1m";
        this.commission = props?.commission ?? 0.001;
        this.startDate = props?.startDate ?? "2023-01-01";
        this.endDate = props?.endDate ?? "2023-12-31";
        this.initialBalance = props?.initialBalance ?? 10000.0;
    }
}
