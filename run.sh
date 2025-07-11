#!/bin/bash

echo "🤖 Starting Binance Futures Trading Bot..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment and run bot
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "🚀 Starting bot..."
echo "📊 Logs will appear below:"
echo "=============================================="

python3 binance_futures_bot.py