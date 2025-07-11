#!/bin/bash

echo "🤖 BINANCE FUTURES BOT - FULLY AUTOMATED SETUP"
echo "=============================================="
echo "🎯 Tujuan: Bot jalan otomatis, Anda tinggal lihat hasil"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Don't run as root. Use regular user."
    exit 1
fi

# Step 1: System Update & Dependencies
print_header "Step 1: Installing system dependencies..."
sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv git curl wget htop

# Step 2: Create project directory
print_header "Step 2: Setting up project directory..."
if [ ! -d "/workspace" ]; then
    sudo mkdir -p /workspace
    sudo chown $USER:$USER /workspace
fi

cd /workspace

# Step 3: Create virtual environment
print_header "Step 3: Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 4: Install Python dependencies
print_header "Step 4: Installing Python packages..."
pip install --upgrade pip
pip install python-binance python-telegram-bot python-dotenv numpy pandas psutil

# Step 5: Create .env template
print_header "Step 5: Creating environment configuration..."
cat > .env.template << 'EOF'
# Binance API Configuration
API_KEY=your_binance_api_key_here
API_SECRET=your_binance_api_secret_here

# Telegram Bot Configuration  
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Bot Configuration
BINANCE_USE_TESTNET=true  # Set to false for real trading
ALLOW_AUTO_REBOOT=false   # Set to true to allow auto-reboot on memory issues

# Optional: Performance tracking
ENABLE_PERFORMANCE_TRACKING=true
AUTO_UPGRADE_ENABLED=true
EOF

# Step 6: Create auto-restart script
print_header "Step 6: Creating auto-restart system..."
cat > run_bot_auto_restart.py << 'EOF'
#!/usr/bin/env python3
"""
Auto-Restart Bot Script - Fully Automated for VPS 1GB
Monitors bot process and restarts automatically if crashed
"""

import subprocess
import time
import psutil
import os
import signal
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_restart.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoRestartBot:
    def __init__(self):
        self.bot_process = None
        self.restart_count = 0
        self.max_restarts_per_hour = 5
        self.restart_times = []
        self.is_running = True
        
        # Memory limits for VPS 1GB
        self.memory_warning_threshold = 600  # MB
        self.memory_critical_threshold = 750  # MB
        self.max_memory_usage = 800  # MB
        
        # Bot script path
        self.bot_script = "main.py"
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.is_running = False
        if self.bot_process:
            self.terminate_bot()
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            return memory_mb
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return 0
    
    def check_system_memory(self):
        """Check system memory and log warnings"""
        try:
            memory = psutil.virtual_memory()
            memory_mb = memory.used / 1024 / 1024
            memory_percent = memory.percent
            
            if memory_percent > 90:
                logger.warning(f"⚠️ System memory critical: {memory_percent:.1f}% ({memory_mb:.1f}MB)")
                return False
            elif memory_percent > 80:
                logger.warning(f"⚠️ System memory high: {memory_percent:.1f}% ({memory_mb:.1f}MB)")
            elif memory_percent > 70:
                logger.info(f"ℹ️ System memory moderate: {memory_percent:.1f}% ({memory_mb:.1f}MB)")
            
            return True
        except Exception as e:
            logger.error(f"Error checking system memory: {e}")
            return True
    
    def cleanup_old_logs(self):
        """Clean up old log files to save space"""
        try:
            log_files = ['bot.log', 'auto_restart.log']
            for log_file in log_files:
                if os.path.exists(log_file):
                    # Check file size
                    size_mb = os.path.getsize(log_file) / 1024 / 1024
                    if size_mb > 10:  # If log file > 10MB
                        # Truncate to last 1000 lines
                        with open(log_file, 'r') as f:
                            lines = f.readlines()
                        with open(log_file, 'w') as f:
                            f.writelines(lines[-1000:])
                        logger.info(f"Cleaned up {log_file} (was {size_mb:.1f}MB)")
        except Exception as e:
            logger.error(f"Error cleaning up logs: {e}")
    
    def start_bot(self):
        """Start the bot process"""
        try:
            # Check if bot script exists
            if not os.path.exists(self.bot_script):
                logger.error(f"Bot script {self.bot_script} not found!")
                return False
            
            # Check system memory before starting
            if not self.check_system_memory():
                logger.error("System memory too low, waiting 5 minutes...")
                time.sleep(300)
                return False
            
            # Clean up old logs
            self.cleanup_old_logs()
            
            # Start bot process
            logger.info(f"🚀 Starting bot: {self.bot_script}")
            self.bot_process = subprocess.Popen(
                ['python3', self.bot_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit to see if it starts successfully
            time.sleep(10)
            
            if self.bot_process.poll() is None:
                logger.info(f"✅ Bot started successfully (PID: {self.bot_process.pid})")
                return True
            else:
                stdout, stderr = self.bot_process.communicate()
                logger.error(f"❌ Bot failed to start: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            return False
    
    def terminate_bot(self):
        """Terminate bot process gracefully"""
        if self.bot_process and self.bot_process.poll() is None:
            try:
                logger.info("🛑 Terminating bot gracefully...")
                self.bot_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.bot_process.wait(timeout=30)
                    logger.info("✅ Bot terminated gracefully")
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️ Bot didn't terminate gracefully, forcing kill...")
                    self.bot_process.kill()
                    self.bot_process.wait()
                    logger.info("✅ Bot killed forcefully")
                    
            except Exception as e:
                logger.error(f"Error terminating bot: {e}")
    
    def check_restart_limit(self):
        """Check if we've restarted too many times recently"""
        current_time = time.time()
        # Remove restart times older than 1 hour
        self.restart_times = [t for t in self.restart_times if current_time - t < 3600]
        
        if len(self.restart_times) >= self.max_restarts_per_hour:
            logger.error(f"🚨 Too many restarts ({len(self.restart_times)}) in the last hour. Waiting 30 minutes...")
            time.sleep(1800)  # Wait 30 minutes
            self.restart_times.clear()
            return False
        
        return True
    
    def monitor_bot(self):
        """Main monitoring loop"""
        logger.info("🤖 Auto-restart bot started. Monitoring main bot...")
        
        while self.is_running:
            try:
                # Check if bot is still running
                if self.bot_process and self.bot_process.poll() is None:
                    # Bot is running, check memory usage
                    memory_mb = self.get_memory_usage()
                    
                    if memory_mb > self.memory_critical_threshold:
                        logger.warning(f"🚨 Bot memory critical: {memory_mb:.1f}MB > {self.memory_critical_threshold}MB")
                        self.terminate_bot()
                        time.sleep(5)
                        continue
                    elif memory_mb > self.memory_warning_threshold:
                        logger.warning(f"⚠️ Bot memory high: {memory_mb:.1f}MB > {self.memory_warning_threshold}MB")
                    
                    # Check system memory
                    self.check_system_memory()
                    
                    # Sleep for monitoring interval
                    time.sleep(30)
                    
                else:
                    # Bot has crashed or stopped
                    if self.bot_process:
                        stdout, stderr = self.bot_process.communicate()
                        logger.error(f"❌ Bot crashed or stopped unexpectedly")
                        if stderr:
                            logger.error(f"Error output: {stderr}")
                    
                    # Check restart limit
                    if not self.check_restart_limit():
                        continue
                    
                    # Record restart time
                    self.restart_times.append(time.time())
                    self.restart_count += 1
                    
                    logger.info(f"🔄 Restarting bot (attempt #{self.restart_count})...")
                    
                    # Wait before restart
                    time.sleep(10)
                    
                    # Start bot
                    if self.start_bot():
                        logger.info(f"✅ Bot restarted successfully")
                    else:
                        logger.error(f"❌ Failed to restart bot")
                        time.sleep(60)  # Wait longer before next attempt
                
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
        
        # Cleanup
        if self.bot_process:
            self.terminate_bot()
        logger.info("👋 Auto-restart bot stopped")

if __name__ == "__main__":
    auto_restart = AutoRestartBot()
    auto_restart.monitor_bot()
EOF

# Step 7: Create systemd service
print_header "Step 7: Creating systemd service..."
cat > binance-bot.service << 'EOF'
[Unit]
Description=Binance Futures Trading Bot
After=network.target
Wants=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/workspace
Environment=PATH=/workspace/venv/bin
ExecStart=/workspace/venv/bin/python3 /workspace/run_bot_auto_restart.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Memory limits for VPS 1GB
MemoryMax=800M
MemorySwapMax=0

# Process limits
LimitNOFILE=65536
LimitNPROC=4096

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/workspace

[Install]
WantedBy=multi-user.target
EOF

# Step 8: Create monitoring script
print_header "Step 8: Creating monitoring tools..."
cat > monitor_bot.sh << 'EOF'
#!/bin/bash

echo "📊 BINANCE BOT MONITORING"
echo "========================="

# Check bot status
echo "🤖 Bot Status:"
if systemctl is-active --quiet binance-bot; then
    echo -e "  ✅ Bot is RUNNING"
else
    echo -e "  ❌ Bot is STOPPED"
fi

# Check memory usage
echo ""
echo "💾 Memory Usage:"
total_mem=$(free -m | awk 'NR==2{printf "%.0f", $2}')
used_mem=$(free -m | awk 'NR==2{printf "%.0f", $3}')
mem_percent=$((used_mem * 100 / total_mem))

echo "  Total: ${total_mem}MB"
echo "  Used: ${used_mem}MB (${mem_percent}%)"

if [ $mem_percent -gt 85 ]; then
    echo -e "  ⚠️  High memory usage!"
elif [ $mem_percent -gt 70 ]; then
    echo -e "  ⚠️  Moderate memory usage"
else
    echo -e "  ✅ Normal memory usage"
fi

# Check disk usage
echo ""
echo "💿 Disk Usage:"
df -h /workspace | tail -1 | awk '{print "  Used: " $3 " / " $2 " (" $5 ")"}'

# Show recent logs
echo ""
echo "📋 Recent Bot Logs:"
journalctl -u binance-bot --no-pager -n 10

echo ""
echo "🔧 Commands:"
echo "  View live logs: sudo journalctl -u binance-bot -f"
echo "  Restart bot: sudo systemctl restart binance-bot"
echo "  Stop bot: sudo systemctl stop binance-bot"
echo "  Check status: sudo systemctl status binance-bot"
EOF

# Step 9: Create performance dashboard
print_header "Step 9: Creating performance dashboard..."
cat > dashboard.py << 'EOF'
#!/usr/bin/env python3
"""
Performance Dashboard - View trading results easily
"""

import json
import os
from datetime import datetime, timedelta
import requests

def get_bot_status():
    """Get bot status from systemd"""
    try:
        result = os.popen('systemctl is-active binance-bot').read().strip()
        return "🟢 RUNNING" if result == "active" else "🔴 STOPPED"
    except:
        return "❓ UNKNOWN"

def get_memory_usage():
    """Get memory usage"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            total = int(lines[0].split()[1]) // 1024
            available = int(lines[2].split()[1]) // 1024
            used = total - available
            percent = (used / total) * 100
            return f"{used}MB / {total}MB ({percent:.1f}%)"
    except:
        return "N/A"

def get_recent_trades():
    """Get recent trades from log"""
    try:
        # This would parse actual trade data from logs
        return "Check Telegram for trade notifications"
    except:
        return "No trade data available"

def main():
    print("🤖 BINANCE FUTURES BOT - PERFORMANCE DASHBOARD")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🤖 Status: {get_bot_status()}")
    print(f"💾 Memory: {get_memory_usage()}")
    print(f"📊 Recent Trades: {get_recent_trades()}")
    print("")
    print("📱 Check Telegram for live trading updates!")
    print("🔧 Use ./monitor_bot.sh for detailed monitoring")

if __name__ == "__main__":
    main()
EOF

# Step 10: Install systemd service
print_header "Step 10: Installing systemd service..."
sudo cp binance-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable binance-bot.service

# Make scripts executable
chmod +x run_bot_auto_restart.py
chmod +x monitor_bot.sh
chmod +x dashboard.py

# Step 11: Create final setup instructions
print_header "Step 11: Setup complete!"
echo ""
echo "🎉 SETUP COMPLETE! Your bot is ready for fully automated trading."
echo ""
echo "📋 NEXT STEPS:"
echo "1. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. Start the bot:"
echo "   sudo systemctl start binance-bot"
echo ""
echo "3. Monitor performance:"
echo "   ./monitor_bot.sh"
echo "   ./dashboard.py"
echo ""
echo "📱 TELEGRAM COMMANDS:"
echo "  /start - Start bot"
echo "  /status - Check status"
echo "  /balance - Check balance"
echo "  /performance - View performance"
echo "  /stop - Stop bot"
echo ""
echo "🔧 USEFUL COMMANDS:"
echo "  View logs: sudo journalctl -u binance-bot -f"
echo "  Restart: sudo systemctl restart binance-bot"
echo "  Stop: sudo systemctl stop binance-bot"
echo "  Status: sudo systemctl status binance-bot"
echo ""
echo "🚀 Bot will auto-start on VPS boot and auto-restart if crashed!"
echo "📊 You can now focus on analyzing trading results!"