#!/usr/bin/env python3
"""
Technical Indicators Module
Lightweight indicators untuk professional analysis
"""

import logging
from typing import List, Union

logger = logging.getLogger(__name__)

class SmartIndicators:
    """Technical indicators yang ringan dan efisien"""
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> Union[float, List[float]]:
        """Calculate RSI indicator"""
        try:
            if len(prices) < period + 1:
                return 50.0  # Neutral RSI if insufficient data
            
            # Calculate price changes
            deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
            
            # Separate gains and losses
            gains = [delta if delta > 0 else 0 for delta in deltas]
            losses = [-delta if delta < 0 else 0 for delta in deltas]
            
            # Calculate first average gain and loss
            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period
            
            # Calculate subsequent values using Wilder's smoothing
            for i in range(period, len(gains)):
                avg_gain = (avg_gain * (period - 1) + gains[i]) / period
                avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            # Calculate RSI
            if avg_loss == 0:
                return 100.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50.0
    
    @staticmethod
    def sma(prices: List[float], period: int = 20) -> float:
        """Simple Moving Average"""
        try:
            if len(prices) < period:
                return prices[-1] if prices else 0.0
            
            return sum(prices[-period:]) / period
            
        except Exception as e:
            logger.error(f"Error calculating SMA: {e}")
            return prices[-1] if prices else 0.0
    
    @staticmethod
    def ema(prices: List[float], period: int = 20) -> float:
        """Exponential Moving Average"""
        try:
            if len(prices) < period:
                return SmartIndicators.sma(prices, len(prices))
            
            multiplier = 2 / (period + 1)
            ema_val = prices[0]
            
            for price in prices[1:]:
                ema_val = (price * multiplier) + (ema_val * (1 - multiplier))
            
            return ema_val
            
        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return prices[-1] if prices else 0.0
    
    @staticmethod
    def bb_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> dict:
        """Bollinger Bands"""
        try:
            if len(prices) < period:
                mid = prices[-1] if prices else 0.0
                return {"upper": mid, "middle": mid, "lower": mid}
            
            # Calculate middle band (SMA)
            middle = SmartIndicators.sma(prices, period)
            
            # Calculate standard deviation
            variance = sum([(price - middle) ** 2 for price in prices[-period:]]) / period
            std = variance ** 0.5
            
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)
            
            return {
                "upper": upper,
                "middle": middle,
                "lower": lower
            }
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            mid = prices[-1] if prices else 0.0
            return {"upper": mid, "middle": mid, "lower": mid}
    
    @staticmethod
    def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
        """MACD indicator"""
        try:
            if len(prices) < slow:
                return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
            
            # Calculate EMAs
            ema_fast = SmartIndicators.ema(prices, fast)
            ema_slow = SmartIndicators.ema(prices, slow)
            
            # MACD line
            macd_line = ema_fast - ema_slow
            
            # Signal line (EMA of MACD) - simplified
            signal_line = macd_line * 0.1  # Simplified signal
            
            # Histogram
            histogram = macd_line - signal_line
            
            return {
                "macd": macd_line,
                "signal": signal_line,
                "histogram": histogram
            }
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
    
    @staticmethod
    def support_resistance(prices: List[float], window: int = 10) -> dict:
        """Simple Support and Resistance levels"""
        try:
            if len(prices) < window * 2:
                current = prices[-1] if prices else 0.0
                return {"support": current * 0.98, "resistance": current * 1.02}
            
            # Find recent highs and lows
            recent_highs = []
            recent_lows = []
            
            for i in range(window, len(prices) - window):
                is_high = all(prices[i] >= prices[j] for j in range(i-window, i+window+1))
                is_low = all(prices[i] <= prices[j] for j in range(i-window, i+window+1))
                
                if is_high:
                    recent_highs.append(prices[i])
                if is_low:
                    recent_lows.append(prices[i])
            
            # Calculate support and resistance
            resistance = max(recent_highs[-3:]) if len(recent_highs) >= 3 else max(prices[-20:])
            support = min(recent_lows[-3:]) if len(recent_lows) >= 3 else min(prices[-20:])
            
            return {
                "support": support,
                "resistance": resistance
            }
            
        except Exception as e:
            logger.error(f"Error calculating S/R: {e}")
            current = prices[-1] if prices else 0.0
            return {"support": current * 0.98, "resistance": current * 1.02}