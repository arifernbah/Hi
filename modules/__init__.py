"""
Professional Trading Bot Modules - Lightweight & Modular
Optimized untuk VPS 1GB RAM dengan intelligence 10-year pro trader
"""

# Version info
__version__ = "1.0.0"
__author__ = "Pro Trader Bot"

# Import all modules
from .config_manager import SmartConfig
from .indicators import SmartIndicators
from .market_analysis import MarketRegimeDetector, LiquidityZoneDetector, MarketStructureAnalyzer
from .position_sizing import KellyCriterionCalculator
from .session_timing import TradingSessionAnalyzer
from .smart_trading import SmartEntry, SmartExit
from .telegram_handler import TelegramNotifier
from .performance_monitor import PerformanceMonitor

__all__ = [
    'SmartConfig',
    'SmartIndicators', 
    'MarketRegimeDetector',
    'LiquidityZoneDetector',
    'MarketStructureAnalyzer',
    'KellyCriterionCalculator',
    'TradingSessionAnalyzer',
    'SmartEntry',
    'SmartExit',
    'TelegramNotifier',
    'PerformanceMonitor'
]
