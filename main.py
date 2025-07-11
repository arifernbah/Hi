
from auto_config_loader import load_config_auto
from core.bot_runner import BinanceFuturesProBot
from dotenv import load_dotenv
import os
from binance.client import Client

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Real-time price fetch ===
def fetch_recent_prices(symbol: str, interval: str, limit: int = 60):
    """Fetch recent closing prices from Binance Futures public endpoint.

    Args:
        symbol (str): Trading pair symbol, e.g. "BTCUSDT".
        interval (str): Kline interval, e.g. "5m".
        limit (int): Number of klines to retrieve.

    Returns:
        list[float]: List of closing prices.
    """
    try:
        # Deteksi testnet atau real dari environment
        api_key = os.getenv("API_KEY", os.getenv("BINANCE_API_KEY", ""))
        is_testnet = "testnet" in api_key.lower() or len(api_key) < 50 if api_key else True
        
        client = Client(testnet=is_testnet)  # public endpoints do not require API keys
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
        return [float(kline[4]) for kline in klines]
    except Exception as e:
        print(f"[WARN] Failed to fetch prices from Binance Futures: {e}. Falling back to empty list.")
        return []

if __name__ == "__main__":
    config = load_config_auto(API_KEY, API_SECRET)

    # Inject Telegram config
    config['telegram'] = {
        'token': TELEGRAM_TOKEN,
        'chat_id': TELEGRAM_CHAT_ID
    }

    # === Kelly Sizing Activation ===
    if config["initial_balance"] >= 50:
        winrate = 0.75  # example fixed winrate
        tp = config["take_profit"]["tp_percent"]
        sl = config["stop_loss"]["sl_percent"]
        rr = tp / sl
        # Kelly fraction calculation moved to position_sizing module
        config["position_sizing"]["method"] = "kelly_partial"
        print(f"[DYNAMIC] Kelly sizing active for balance >= $50")

    # === Market Safety Check ===
    symbol = config["symbol"]
    print(f"[INFO] Starting bot with symbol: {symbol}")
    print(f"[INFO] Balance: ${config['initial_balance']:.2f}")
    print(f"[INFO] Max positions: {config['max_open_trades']}")
    print(f"[INFO] Confidence threshold: {config['confidence_threshold']}%")

    # Initialize and start the async trading bot
    import asyncio

    bot = BinanceFuturesProBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
