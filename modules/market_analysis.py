#!/usr/bin/env python3
"""
Market Analysis Module - Professional Grade
Contains: Market Regime Detection, Liquidity Zones, Market Structure Analysis
"""

import numpy as np
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class MarketRegimeDetector:
    """Deteksi regime market seperti pro trader institutional"""
    
    def __init__(self):
        self.regime_cache = {}
        self.volatility_cache = {}
    
    def detect_market_regime(self, prices: List[float], volumes: List[float]) -> Dict[str, Any]:
        """Deteksi regime market: Trending/Ranging/Volatile"""
        if len(prices) < 50:
            return {"regime": "insufficient_data", "confidence": 0}
        
        # Calculate key metrics
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns) * np.sqrt(288)  # Annualized for 5min bars
        
        # Trend strength (ADX-like calculation)
        highs = [max(prices[i-5:i+1]) for i in range(5, len(prices))]
        lows = [min(prices[i-5:i+1]) for i in range(5, len(prices))]
        
        plus_dm = np.maximum(np.diff(highs), 0)
        minus_dm = np.maximum(-np.diff(lows), 0)
        tr = np.maximum(np.diff(highs), np.maximum(np.abs(np.diff(prices[-len(plus_dm):])), np.abs(np.diff(lows))))
        
        plus_di = 100 * (plus_dm / tr)
        minus_di = 100 * (minus_dm / tr)
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
        adx = np.mean(dx[-14:])  # 14-period ADX
        
        # Volume analysis
        volume_sma = np.mean(volumes[-20:])
        current_volume = volumes[-1]
        volume_ratio = current_volume / volume_sma
        
        # Regime classification
        if adx > 25 and volatility < np.percentile([np.std(np.diff(prices[i:i+20])) for i in range(len(prices)-20)], 70):
            regime = "trending_strong"
            confidence = min(adx / 50 * 100, 95)
        elif adx > 15:
            regime = "trending_weak"  
            confidence = min(adx / 30 * 100, 85)
        elif volatility > np.percentile([np.std(np.diff(prices[i:i+20])) for i in range(len(prices)-20)], 80):
            regime = "volatile"
            confidence = min(volatility * 1000, 90)
        else:
            regime = "ranging"
            confidence = 100 - adx * 2
        
        return {
            "regime": regime,
            "confidence": confidence,
            "adx": adx,
            "volatility": volatility,
            "volume_ratio": volume_ratio,
            "trend_strength": adx,
            "market_bias": "bullish" if plus_di > minus_di else "bearish"
        }

class LiquidityZoneDetector:
    """Deteksi liquidity zones seperti ICT/Smart Money concepts"""
    
    def detect_liquidity_zones(self, prices: List[float]) -> Dict[str, Any]:
        """Deteksi zone dimana institutional traders biasanya masuk"""
        if len(prices) < 100:
            return {"zones": [], "current_bias": "neutral"}
        
        # Previous day high/low (PDH/PDL)
        daily_high = max(prices[-288:])  # 288 = 24 hours of 5min bars
        daily_low = min(prices[-288:])
        
        # Fair Value Gaps detection
        fvgs = self._detect_fair_value_gaps(prices)
        
        # Current price relative to levels
        current_price = prices[-1]
        
        # Bias determination
        if current_price > (daily_high + daily_low) / 2:
            bias = "bullish"
            key_level = daily_low
        else:
            bias = "bearish" 
            key_level = daily_high
        
        return {
            "daily_high": daily_high,
            "daily_low": daily_low,
            "fair_value_gaps": fvgs,
            "current_bias": bias,
            "key_level": key_level,
            "distance_to_key": abs(current_price - key_level) / current_price * 100
        }
    
    def _detect_fair_value_gaps(self, prices: List[float]) -> List[Dict]:
        """Deteksi Fair Value Gaps - area dimana price akan kembali"""
        fvgs = []
        
        for i in range(2, len(prices)-1):
            if i < len(prices)-1 and prices[i+1] > prices[i-1]:
                gap_size = (prices[i+1] - prices[i-1]) / prices[i] * 100
                if gap_size > 0.1:
                    fvgs.append({
                        "type": "bullish",
                        "top": prices[i+1],
                        "bottom": prices[i-1],
                        "index": i,
                        "size_pct": gap_size
                    })
            elif i < len(prices)-1 and prices[i+1] < prices[i-1]:
                gap_size = (prices[i-1] - prices[i+1]) / prices[i] * 100
                if gap_size > 0.1:
                    fvgs.append({
                        "type": "bearish",
                        "top": prices[i-1],
                        "bottom": prices[i+1],
                        "index": i,
                        "size_pct": gap_size
                    })
        
        # Return only recent and significant FVGs
        recent_fvgs = [fvg for fvg in fvgs if len(prices) - fvg["index"] < 50]
        return sorted(recent_fvgs, key=lambda x: x["size_pct"], reverse=True)[:3]

class MarketStructureAnalyzer:
    """Analisis struktur market seperti pro trader"""
    
    def analyze_market_structure(self, prices: List[float]) -> Dict[str, Any]:
        """Analisis Higher Highs, Higher Lows, Lower Highs, Lower Lows"""
        if len(prices) < 30:
            return {"structure": "insufficient_data", "bias": "neutral"}
        
        # Find swing points
        swing_highs = []
        swing_lows = []
        
        for i in range(5, len(prices)-5):
            if all(prices[i] > prices[j] for j in range(i-5, i)) and \
               all(prices[i] > prices[j] for j in range(i+1, i+6)):
                swing_highs.append((i, prices[i]))
            
            if all(prices[i] < prices[j] for j in range(i-5, i)) and \
               all(prices[i] < prices[j] for j in range(i+1, i+6)):
                swing_lows.append((i, prices[i]))
        
        # Analyze structure
        structure = self._determine_structure(swing_highs[-3:], swing_lows[-3:])
        
        # Market bias
        if structure in ["higher_highs_higher_lows", "higher_highs"]:
            bias = "bullish"
        elif structure in ["lower_highs_lower_lows", "lower_lows"]:
            bias = "bearish"
        else:
            bias = "ranging"
        
        return {
            "structure": structure,
            "bias": bias,
            "recent_swing_highs": swing_highs[-3:],
            "recent_swing_lows": swing_lows[-3:]
        }
    
    def _determine_structure(self, swing_highs: List[Tuple], swing_lows: List[Tuple]) -> str:
        """Tentukan struktur market"""
        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return "insufficient_swings"
        
        # Check trends
        highs_trend = "higher" if swing_highs[-1][1] > swing_highs[-2][1] else "lower"
        lows_trend = "higher" if swing_lows[-1][1] > swing_lows[-2][1] else "lower"
        
        if highs_trend == "higher" and lows_trend == "higher":
            return "higher_highs_higher_lows"
        elif highs_trend == "lower" and lows_trend == "lower":
            return "lower_highs_lower_lows"
        else:
            return "ranging"