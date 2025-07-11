#!/usr/bin/env python3
"""
Auto-Restart Bot Script - Optimized for VPS 1GB
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