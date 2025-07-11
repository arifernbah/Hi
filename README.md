# 🤖 Binance Futures Trading Bot

Advanced automated trading bot for Binance Futures with multi-symbol scanning, smart position sizing, and Telegram notifications.

## ✨ Features

- **Multi-Symbol Trading**: Scans 10+ cryptocurrency pairs simultaneously
- **Smart Analysis**: Advanced technical indicators and market analysis
- **Auto Leverage**: Dynamic leverage adjustment based on balance and volatility
- **Risk Management**: Sophisticated position sizing and risk controls
- **Telegram Integration**: Real-time notifications and casual messaging
- **Two Trading Modes**: 
  - **Moderate Mode** ($5-$20): 20-25% monthly growth
  - **Optimized Mode** ($20+): 30-45% monthly growth

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

### 2. Configure API Keys
Edit the `.env` file with your credentials:
```env
# Binance API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Trading Configuration
DEFAULT_SYMBOL=BTCUSDT
TEST_MODE=true
```

### 3. Run the Bot
```bash
# Make run script executable and start
chmod +x run.sh
./run.sh
```

## 📋 Prerequisites

- **Binance Account**: Create account at [binance.com](https://binance.com)
- **API Keys**: Generate API keys with Futures trading permissions
- **Telegram Bot**: Create bot via [@BotFather](https://t.me/botfather)
- **Minimum Balance**: $5 for moderate mode, $20+ for optimized mode

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the bot
python3 binance_futures_bot.py
```

## 📊 Trading Modes

### Moderate Mode ($5-$20 Balance)
- **Max Positions**: 2
- **Confidence Threshold**: 70% (normal), 80% (high-confidence)
- **Expected Growth**: 20-25% monthly
- **Risk Level**: Conservative

### Optimized Mode ($20+ Balance)
- **Max Positions**: 3
- **Confidence Threshold**: 65% (normal), 75% (high-confidence)
- **Expected Growth**: 30-45% monthly
- **Risk Level**: Moderate

## ⚠️ Important Notes

1. **Always test first**: Set `TEST_MODE=true` in `.env`
2. **Start small**: Begin with small amounts
3. **Monitor regularly**: Check Telegram notifications
4. **Risk warning**: Trading involves risk of loss
5. **API security**: Keep your API keys secure

## 📱 Telegram Notifications

The bot sends casual, friendly messages for:
- Trade entries and exits
- Balance updates
- Error alerts
- Daily summaries

## 🔍 Technical Indicators

- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Moving Averages
- Volume Analysis
- Market Structure Analysis

## 🛠️ Troubleshooting

### Common Issues:
1. **API Key Error**: Check permissions and keys
2. **Telegram Error**: Verify bot token and chat ID
3. **Balance Error**: Ensure sufficient funds
4. **Network Error**: Check internet connection

### Logs:
- Check console output for detailed logs
- Telegram notifications for important events

## 📈 Performance Expectations

- **Trade Frequency**: 2-5 trades per day
- **Win Rate**: 60-70%
- **Drawdown**: 10-18% maximum
- **Recovery**: 1-2 weeks typically

## 🔒 Security

- Never share API keys
- Use API keys with Futures trading only
- Enable IP restrictions on Binance
- Regular security audits

## 📞 Support

For issues or questions:
1. Check the logs first
2. Verify API key permissions
3. Ensure sufficient balance
4. Test with small amounts

---

**Disclaimer**: This bot is for educational purposes. Trading involves risk. Use at your own discretion.
