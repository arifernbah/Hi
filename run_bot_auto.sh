#!/bin/bash

echo "🤖 Starting Binance Futures Trading Bot with Auto-Restart..."
echo "=========================================================="

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

# Check if auto-restart script exists
if [ ! -f "run_bot_auto_restart.py" ]; then
    echo "❌ Auto-restart script not found!"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check system memory
echo "💾 Checking system memory..."
total_mem=$(free -m | awk 'NR==2{printf "%.0f", $2}')
used_mem=$(free -m | awk 'NR==2{printf "%.0f", $3}')
mem_percent=$((used_mem * 100 / total_mem))

echo "📊 Memory Usage: ${used_mem}MB / ${total_mem}MB (${mem_percent}%)"

if [ $mem_percent -gt 85 ]; then
    echo "⚠️ Warning: High memory usage (${mem_percent}%). Consider restarting VPS."
fi

# Start the auto-restart bot
echo "🚀 Starting bot with auto-restart protection..."
echo "📊 Logs will appear below:"
echo "=========================================================="

# Run the auto-restart bot
python3 run_bot_auto_restart.py

# If we reach here, something went wrong
echo ""
echo "🤖 Auto-restart bot stopped."
echo "To restart, run: ./run_bot_auto.sh"