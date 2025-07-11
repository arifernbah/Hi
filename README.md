# ARIFBOT - Binance Futures Trading Bot

🤖 **Professional Binance Futures Trading Bot** dengan arsitektur modular dan intelligence 10-year pro trader.

## ⚡ Fitur Utama

- **📊 Binance Futures Trading** (bukan Spot)
- **🧠 Professional Trading Intelligence**
- **🛡️ Risk Management Hedge Fund Grade**
- **📱 Telegram Integration**
- **⚙️ Modular Architecture**
- **🎯 Multi-Symbol Support** (Top 10 pairs)
- **🔄 Auto Testnet/Real Detection**

## 🚀 Quick Start

### 1. Setup Otomatis
```bash
bash setup_and_run.sh
```

### 2. Manual Setup
```bash
# Install dependencies
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements_pro_trader.txt

# Setup environment
cp .env.template .env
# Edit .env dengan API key Anda
```

### 3. Konfigurasi .env
```env
API_KEY=your_binance_futures_api_key
API_SECRET=your_binance_futures_secret
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

## 📋 Requirements

- Python 3.10+
- Binance Futures API Key
- Telegram Bot Token
- VPS dengan akses internet stabil

## 🔧 Konfigurasi

### API Key Setup
1. **Untuk Real Trading:**
   - Buat API key di [Binance Futures](https://www.binance.com/en/futures-activity/leaderboard)
   - Aktifkan Futures permissions
   - Pastikan IP VPS sudah di-whitelist

2. **Untuk Testing:**
   - Buat API key di [Binance Testnet](https://testnet.binance.vision/)
   - Bot otomatis detect testnet/real

### Telegram Setup
1. Buat bot di [@BotFather](https://t.me/botfather)
2. Dapatkan chat ID dengan [@userinfobot](https://t.me/userinfobot)
3. Isi di file `.env`

## 📊 Trading Pairs

Bot mendukung top 10 large-cap futures pairs:
- BTCUSDT, ETHUSDT, BNBUSDT
- XRPUSDT, SOLUSDT, ADAUSDT
- AVAXUSDT, MATICUSDT, DOTUSDT, LTCUSDT

## 🛡️ Risk Management

- **Position Sizing:** Kelly Criterion
- **Stop Loss:** Dynamic berdasarkan volatility
- **Take Profit:** Multi-level
- **Max Risk:** 2% per trade
- **Leverage:** Conservative (2x default)

## 📱 Telegram Commands

- `/start` - Welcome message
- `/status` - Bot status & positions
- `/balance` - Account balance
- `/performance` - Trading stats
- `/mode` - Current mode (testnet/real)
- `/testnet` - Switch to testnet
- `/real` - Switch to real trading
- `/stop` - Stop bot
- `/help` - Show help

## 🏗️ Architecture

```
├── core/
│   └── bot_runner.py          # Main bot logic
├── modules/
│   ├── config_manager.py      # Configuration
│   ├── smart_trading.py       # Trading strategies
│   ├── telegram_handler.py    # Telegram integration
│   └── ...                    # Other modules
├── main.py                    # Entry point
├── setup_and_run.sh          # Auto setup script
└── requirements_pro_trader.txt # Dependencies
```

## ⚠️ Disclaimer

- **Trading involves risk**
- **Test thoroughly before real trading**
- **Use testnet for initial testing**
- **Monitor bot performance regularly**

## 📞 Support

Untuk bantuan dan support, silakan buat issue di repository ini.

---

**🚀 Ready untuk professional futures trading!**
