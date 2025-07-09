import time
import datetime
import requests
from decimal import Decimal, getcontext

# دقّة الأرقام العشرية
getcontext().prec = 8

# ضع هنا التوكن والمعرّف (أضفتهم كـ Secrets في GitHub Actions)
TOKEN = "8055534376:AAH5MnespXGMHATDljNfEwbLbBrLccf5gG4"
CHAT_ID = "1014050409"

# قائمة الرموز والفريمات
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
TIMEFRAMES = ["1m", "1h", "4h", "1d"]

def now_iraq():
    """التاريخ والوقت حسب توقيت العراق"""
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=3))\
           .strftime("%Y-%m-%d %H:%M:%S")

def send_telegram(msg: str):
    """إرسال رسالة إلى تيليجرام عبر البوت"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def fetch_klines(symbol: str, tf: str, limit: int = 100):
    """جلب بيانات الشموع والاحتفاظ بإغلاق كل شمعة بعد التحقق من اكتمالها"""
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": tf, "limit": limit}
    res = requests.get(url, params=params).json()
    return [
        {"close": Decimal(k[4])}
        for k in res
        if isinstance(k, list) and len(k) >= 5
    ]

def analyze(symbol: str, tf: str):
    """بناء رسالة التحليل وإرسالها"""
    candles = fetch_klines(symbol, tf)
    if not candles:
        print(f"No data for {symbol} {tf}")
        return

    price = candles[-1]["close"]
    msg = f"""
📡 تحليل {symbol} ({tf})
📉 السعر اللحظي: {price} USDT
🕓 {now_iraq()}
"""
    send_telegram(msg)

def run_all():
    """تشغيل التحليل لكل رمز ولكل فريم"""
    for sym in SYMBOLS:
        for tf in TIMEFRAMES:
            analyze(sym, tf)
            time.sleep(1)

if __name__ == "__main__":
    run_all()
