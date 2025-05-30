import yfinance as yf
import pandas as pd
import ta
import time
from datetime import datetime

def fetch_data(symbol):
    df = yf.download(tickers=symbol, interval='1m', period='1d', progress=False)
    df.dropna(inplace=True)
    return df

def generate_signal(df):
    df['ema5'] = ta.trend.ema_indicator(df['Close'], window=5)
    df['ema13'] = ta.trend.ema_indicator(df['Close'], window=13)
    df['ema50'] = ta.trend.ema_indicator(df['Close'], window=50)
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    bb = ta.volatility.BollingerBands(df['Close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    last = df.iloc[-1]

    if (
        last['ema5'] > last['ema13'] > last['ema50'] and
        last['rsi'] > 55 and
        last['Close'] < last['bb_upper']
    ):
        return 'CALL'
    elif (
        last['ema5'] < last['ema13'] < last['ema50'] and
        last['rsi'] < 45 and
        last['Close'] > last['bb_lower']
    ):
        return 'PUT'
    else:
        return 'NO SIGNAL'

def run_signal_bot():
    assets = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "XAUUSD": "XAUUSD=X"
    }

    while True:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking signals...")
        for name, symbol in assets.items():
            df = fetch_data(symbol)
            signal = generate_signal(df)
            price = df['Close'].iloc[-1]
            print(f"{name} | Signal: {signal} | Price: {price}")
        time.sleep(60)

if __name__ == "__main__":
    run_signal_bot()

