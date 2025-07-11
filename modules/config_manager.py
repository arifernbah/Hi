#!/usr/bin/env python3
"""
Configuration Manager Module
Smart configuration untuk trading bot yang adaptif
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

class SmartConfig:
    """Konfigurasi pintar yang adaptif untuk modal kecil"""
    
    def __init__(self):
        # Mode trading (testnet/real)
        self.is_testnet = True
        
        # API credentials (akan diload dari environment atau file)
        self.api_key = ""
        self.api_secret = ""
        
        # Telegram settings
        self.telegram_token = ""
        self.telegram_chat_id = ""
        
        # Trading parameters (optimized untuk $5 modal)
        # Support multi-symbol list; keep backward-compat single symbol attr
        self.symbol = "BTCUSDT"             # primary / default symbol
        # Default top 10 large-cap futures pairs (relative safety vs. low-cap)
        self.symbols = [
            "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "SOLUSDT",
            "ADAUSDT", "AVAXUSDT", "MATICUSDT", "DOTUSDT", "LTCUSDT"
        ]
        self.timeframe = "5m"
        
        # Risk management (sangat konservatif)
        self.max_risk_per_trade = 0.02  # 2% per trade
        self.stop_loss_pct = 0.03       # 3% stop loss
        self.min_profit_target = 0.005  # 0.5% minimum profit
        self.leverage = 2               # Low leverage untuk safety
        
        # Position management
        self.max_open_positions = 1     # Hanya 1 posisi untuk modal kecil
        
        # Balance tracking
        self.initial_balance = 100.0    # Default initial balance untuk reference
        
        # Load existing config if available
        self.load_config()
    
    def load_config(self):
        """Load config dari file atau environment"""
        try:
            # Try environment variables first (support both API_KEY and BINANCE_API_KEY)
            self.api_key = os.getenv('BINANCE_API_KEY', os.getenv('API_KEY', ''))
            self.api_secret = os.getenv('BINANCE_API_SECRET', os.getenv('API_SECRET', ''))
            self.telegram_token = os.getenv('TELEGRAM_TOKEN', '')
            self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
            
            # Setelah membaca API key dan secret, set mode otomatis
            if self.api_key and self.api_secret:
                # Deteksi apakah ini API key testnet atau real
                if "testnet" in self.api_key.lower() or len(self.api_key) < 50:
                    self.is_testnet = True
                    print("[INFO] Detected Testnet API Key - Using Testnet Mode")
                else:
                    self.is_testnet = False
                    print("[INFO] Detected Real API Key - Using Real Trading Mode")
            else:
                self.is_testnet = True

            # Try loading from config file
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config_data = json.load(f)
                    
                for key, value in config_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                # Backward compatibility: if only 'symbol' provided, build symbols list
                if 'symbols' not in config_data and 'symbol' in config_data:
                    self.symbols = [config_data['symbol']]
                        
                logger.info("Configuration loaded successfully")
                
        except Exception as e:
            logger.warning(f"Could not load config: {e}")
    
    def save_config(self):
        """Save current config to file"""
        try:
            config_data = {
                'is_testnet': self.is_testnet,
                'symbol': self.symbol,
                'symbols': self.symbols,
                'timeframe': self.timeframe,
                'max_risk_per_trade': self.max_risk_per_trade,
                'stop_loss_pct': self.stop_loss_pct,
                'min_profit_target': self.min_profit_target,
                'leverage': self.leverage,
                'max_open_positions': self.max_open_positions
            }
            
            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
                
            logger.info("Configuration saved successfully")
            
        except Exception as e:
            logger.error(f"Could not save config: {e}")