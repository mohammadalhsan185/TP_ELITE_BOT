import time, datetime, logging, requests, csv
from decimal import Decimal

TOKEN = "ضع توكن البوت هنا"
CHAT_ID = "ضع معرف التليجرام هنا"

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
TIMEFRAMES = ["1m", "1h"]

def now_iraq():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def fetch_klines(symbol, tf, limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": tf, "limit": limit}
    res = requests.get(url, params=params)
    return [
        {"close": Decimal(k[4])}
        for k in res.json()
    ]

def analyze(symbol, tf):
    candles = fetch_klines(symbol, tf)
    closes = [c["close"] for c in candles]
    price = closes[-1]
    msg = f"""
📡 تحليل {symbol} ({tf})
📉 السعر الحالي: {price} USDT
🕓 {now_iraq()}
"""
    send_telegram(msg)

def run_all():
    for sym in SYMBOLS:
        for tf in TIMEFRAMES:
            analyze(sym, tf)
            time.sleep(1)

if __name__ == "__main__":
    run_all()
