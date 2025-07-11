#!/bin/bash

echo "🔧 Setting up Auto-Restart System for VPS 1GB..."
echo "================================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run as root. Use regular user."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
sudo apt update
sudo apt install -y python3-psutil

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x run_bot_auto_restart.py
chmod +x run_bot_auto.sh

# Install systemd service
echo "🔧 Installing systemd service..."
sudo cp binance-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable binance-bot.service

echo "✅ Auto-restart system installed!"
echo ""
echo "📋 Available commands:"
echo "  Start bot: ./run_bot_auto.sh"
echo "  Start service: sudo systemctl start binance-bot"
echo "  Stop service: sudo systemctl stop binance-bot"
echo "  Check status: sudo systemctl status binance-bot"
echo "  View logs: sudo journalctl -u binance-bot -f"
echo ""
echo "🚀 Bot will now auto-start on VPS boot and auto-restart if crashed!"