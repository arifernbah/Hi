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
        self.symbol = "DOGEUSDT"             # primary / default symbol
        # Default top 10 large-cap futures pairs (relative safety vs. low-cap)
        self.symbols = [
            "DOGEUSDT", "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", 
            "SOLUSDT", "MATICUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT"
        ]
        self.timeframe = "5m"
        
        # Risk management (sangat konservatif)
        self.max_risk_per_trade = 0.02  # 2% per trade
        self.stop_loss_pct = 0.03       # 3% stop loss
        self.min_profit_target = 0.005  # 0.5% minimum profit
        self.leverage = 2               # Low leverage untuk safety
        
        # Position management - MODERATE MODE
        self.max_open_positions = 2     # 2 posisi untuk moderate growth
        
        # Balance tracking
        self.initial_balance = 100.0    # Default initial balance untuk reference
        
        # Entry confidence threshold - MODERATE MODE
        self.confidence_threshold = 70  # Normal confidence untuk entry (70%)
        self.high_confidence_threshold = 80  # High confidence untuk 2nd position
        self.max_high_confidence_positions = 1  # Max high confidence positions
        self.different_symbols_only = True  # Force different symbols
        self.portfolio_heat_limit = 10  # Portfolio heat limit (%)
        
        # Additional config attributes for compatibility
        self.exchange = "binance_futures"
        self.strategy = "hybrid"
        self.risk_level = "conservative"
        self.max_open_trades = 1  # Alias for max_open_positions
        self.vps = "1GB"
        
        # Position sizing config
        self.position_sizing_method = "kelly_partial"
        self.position_sizing_fraction = 0.5
        
        # Safety orders config
        self.safety_orders_enabled = False
        self.max_safety_orders = 0
        self.martingale_volume_coefficient = 1.0
        self.martingale_step_coefficient = 1.0
        
        # Take profit config
        self.take_profit_enabled = True
        self.tp_percent = 1.0
        
        # Stop loss config
        self.stop_loss_enabled = True
        self.sl_percent = 3.0
        
        # Trailing config
        self.trailing_enabled = True
        self.trailing_percent = 0.2
        
        # Session config
        self.session_active_hours_only = True
        self.session_hours = "07:00-21:00"
        
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
                'max_open_positions': self.max_open_positions,
                'confidence_threshold': self.confidence_threshold,
                'high_confidence_threshold': self.high_confidence_threshold,
                'max_high_confidence_positions': self.max_high_confidence_positions,
                'different_symbols_only': self.different_symbols_only,
                'portfolio_heat_limit': self.portfolio_heat_limit,
                'exchange': self.exchange,
                'strategy': self.strategy,
                'risk_level': self.risk_level,
                'max_open_trades': self.max_open_trades,
                'vps': self.vps,
                'position_sizing_method': self.position_sizing_method,
                'position_sizing_fraction': self.position_sizing_fraction,
                'safety_orders_enabled': self.safety_orders_enabled,
                'max_safety_orders': self.max_safety_orders,
                'martingale_volume_coefficient': self.martingale_volume_coefficient,
                'martingale_step_coefficient': self.martingale_step_coefficient,
                'take_profit_enabled': self.take_profit_enabled,
                'tp_percent': self.tp_percent,
                'stop_loss_enabled': self.stop_loss_enabled,
                'sl_percent': self.sl_percent,
                'trailing_enabled': self.trailing_enabled,
                'trailing_percent': self.trailing_percent,
                'session_active_hours_only': self.session_active_hours_only,
                'session_hours': self.session_hours
            }
            
            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
                
            logger.info("Configuration saved successfully")
            
        except Exception as e:
            logger.error(f"Could not save config: {e}")