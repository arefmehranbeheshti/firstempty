import requests
import pandas as pd
import time
from datetime import datetime

def fetch_and_save_data(symbol):
    url = f"https://chart.nobitex.ir/market/udf/history"
    params = {
        "symbol": symbol,
        "resolution": "1",
        "from": "0000",
        "to": "1737951001"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['s'] == 'ok':
            df = pd.DataFrame({
                'timestamp': data['t'],
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            filename = f"data_{symbol}.csv"
            df.to_csv(filename, index=False)
            print(f"Successfully saved data for {symbol}")
            
        else:
            print(f"Error fetching data for {symbol}: {data['s']}")
            
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")
    
    time.sleep(1)

symbols = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "XRPUSDT", "BCHUSDT", "BNBUSDT", "EOSUSDT", 
           "XLMUSDT", "ETCUSDT", "TRXUSDT", "PMNUSDT", "DOGEUSDT", "UNIUSDT", "DAIUSDT", 
           "LINKUSDT", "DOTUSDT", "AAVEUSDT", "ADAUSDT", "SHIBUSDT", "FTMUSDT", "MATICUSDT", 
           "AXSUSDT", "MANAUSDT", "SANDUSDT", "AVAXUSDT", "MKRUSDT", "GMTUSDT", "USDCUSDT", 
           "BANDUSDT", "COMPUSDT", "HBARUSDT", "WBTCUSDT", "GLMUSDT", "ATOMUSDT", "AEVOUSDT", 
           "RSRUSDT", "API3USDT", "ENSUSDT", "MAGICUSDT", "ONEUSDT", "EGALAUSDT", "XTZUSDT", 
           "FLOWUSDT", "GALUSDT", "CVCUSDT", "NMRUSDT", "BATUSDT", "TRBUSDT", "RDNTUSDT", 
           "YFIUSDT", "TUSDT", "QNTUSDT", "IMXUSDT", "GMXUSDT", "ETHFIUSDT", "GRTUSDT", 
           "WLDUSDT", "NOTUSDT", "MEMEUSDT", "SOLUSDT", "BALUSDT", "DAOUSDT", "TONUSDT", 
           "1INCHUSDT", "OMUSDT", "SLPUSDT", "SSVUSDT", "RNDRUSDT", "NEARUSDT", "WOOUSDT", 
           "CRVUSDT", "MDTUSDT", "EGLDUSDT", "LPTUSDT", "BICOUSDT", "ANTUSDT", "APEUSDT", 
           "LRCUSDT", "WUSDT", "BLURUSDT", "CELRUSDT", "CVXUSDT", "100K_FLOKIUSDT", "JSTUSDT", 
           "ZROUSDT", "ARBUSDT", "1M_NFTUSDT", "UMAUSDT", "SKLUSDT", "ZRXUSDT", "AGLDUSDT", 
           "APTUSDT", "SUSHIUSDT", "FETUSDT", "ALGOUSDT", "1M_PEPEUSDT", "1B_BABYDOGEUSDT", 
           "MASKUSDT", "1M_BTTUSDT", "STORJUSDT", "XMRUSDT", "SNTUSDT", "FILUSDT", "ENJUSDT", 
           "OMGUSDT", "CHZUSDT", "DYDXUSDT", "AGIXUSDT", "LDOUSDT", "SNXUSDT"]


for symbol in symbols:
    fetch_and_save_data(symbol)
