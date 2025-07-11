#!/bin/bash

echo "🚀 Setting up Binance Futures Trading Bot..."
echo "=============================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run this script as root"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt update -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget

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
    cat > .env << EOF
# Binance API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Trading Configuration
DEFAULT_SYMBOL=BTCUSDT
TEST_MODE=true
EOF
    echo "✅ .env file created! Please edit it with your API keys."
else
    echo "✅ .env file already exists."
fi

# Make main script executable
echo "🔧 Making scripts executable..."
chmod +x run_bot.sh
chmod +x stop_bot.sh

echo ""
echo "🎉 Setup completed successfully!"
echo "=============================================="
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: ./run_bot.sh"
echo "3. To stop: ./stop_bot.sh"
echo ""
echo "⚠️  IMPORTANT: Always test with TEST_MODE=true first!"
echo "=============================================="