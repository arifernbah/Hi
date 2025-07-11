#!/bin/bash

echo "🚀 Setting up Binance Futures Trading Bot..."
echo "=============================================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt update -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file template..."
    cat > .env << 'EOF'
# ========================================
# 🤖 BINANCE FUTURES TRADING BOT CONFIG
# ========================================

# 🔑 BINANCE API CONFIGURATION
# Get from: https://www.binance.com/en/my/settings/api-management
# Enable: Futures Trading, Spot & Margin Trading
API_KEY=your_binance_api_key_here
API_SECRET=your_binance_secret_key_here

# Alternative format (also supported):
# BINANCE_API_KEY=your_binance_api_key_here
# BINANCE_SECRET_KEY=your_binance_secret_key_here

# 📱 TELEGRAM CONFIGURATION
# Bot Token: Get from @BotFather on Telegram
# Chat ID: Get from @userinfobot on Telegram
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Alternative format (also supported):
# TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# ⚙️ TRADING CONFIGURATION
DEFAULT_SYMBOL=BTCUSDT
TEST_MODE=false

# 🎯 TRADING MODES
# TEST_MODE=true  = Testnet (paper trading)
# TEST_MODE=false = Real trading (LIVE MONEY)

# 📊 OPTIONAL SETTINGS
# MAX_POSITIONS=3
# CONFIDENCE_THRESHOLD=70
# LEVERAGE=5
EOF
    echo "✅ .env file created! Please edit it with your API keys."
    echo "⚠️  IMPORTANT: Set TEST_MODE=false for real trading!"
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "=============================================="
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: source venv/bin/activate && python3 binance_futures_bot.py"
echo ""
echo "⚠️  IMPORTANT: Set TEST_MODE=false for real trading!"
echo "=============================================="