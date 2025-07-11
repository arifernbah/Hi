#!/usr/bin/env python3
"""
Session Timing Module - Global Market Session Analysis
Professional timing analysis untuk optimal entry/exit
"""

import pytz
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TradingSessionAnalyzer:
    """Analisis sesi trading global untuk timing optimal"""
    
    def __init__(self):
        self.sessions = {
            "asian": {
                "start": 23, "end": 8, 
                "volatility": "low",
                "characteristics": "Range-bound, lower volume"
            },
            "london": {
                "start": 7, "end": 16, 
                "volatility": "high",
                "characteristics": "High volatility, trend initiation"
            },
            "newyork": {
                "start": 12, "end": 21, 
                "volatility": "high",
                "characteristics": "Major moves, high volume"
            }
        }
        
        # Major news times to avoid (UTC hours)
        self.news_times = [
            {"time": 12, "name": "EU Economic Data"},
            {"time": 13, "name": "US Market Open"},
            {"time": 17, "name": "US Economic Data"},
            {"time": 21, "name": "US Market Close"}
        ]
    
    def get_session_adjustment_factor(self, dt: datetime = None) -> Dict[str, Any]:
        """Get adjustment factor berdasarkan sesi trading"""
        try:
            if dt is None:
                dt = datetime.now(pytz.UTC)
            
            current_hour = dt.hour
            current_day = dt.weekday()  # 0=Monday, 6=Sunday
            
            # Determine active session and calculate boosts
            session_info = self._identify_current_session(current_hour)
            
            # Day of week adjustment
            day_adjustments = {
                0: 1.0,   # Monday - Normal
                1: 1.1,   # Tuesday - Good
                2: 1.15,  # Wednesday - Best (mid-week)
                3: 1.1,   # Thursday - Good
                4: 0.8,   # Friday - Reduced (weekend approach)
                5: 0.3,   # Saturday - Very low
                6: 0.5    # Sunday - Low
            }
            
            day_adjustment = day_adjustments.get(current_day, 1.0)
            
            # News impact adjustment
            news_impact = self._check_news_impact(current_hour)
            
            # Calculate final adjustment
            session_boost = session_info["volatility_boost"]
            timing_boost = session_info["timing_boost"]
            
            final_adjustment = session_boost * timing_boost * day_adjustment * news_impact
            final_adjustment = max(0.3, min(final_adjustment, 1.8))  # Cap between 30%-180%
            
            return {
                "session": session_info["session"],
                "session_adjustment": final_adjustment,
                "volatility_boost": session_boost,
                "timing_boost": timing_boost,
                "day_adjustment": day_adjustment,
                "news_impact": news_impact,
                "current_hour": current_hour,
                "current_day": current_day,
                "recommendation": self._get_session_recommendation(final_adjustment)
            }
            
        except Exception as e:
            logger.error(f"Error in session analysis: {e}")
            return {
                "session": "unknown",
                "session_adjustment": 1.0,
                "volatility_boost": 1.0,
                "timing_boost": 1.0,
                "day_adjustment": 1.0,
                "news_impact": 1.0,
                "recommendation": "NORMAL"
            }
    
    def _identify_current_session(self, hour: int) -> Dict[str, Any]:
        """Identify current trading session"""
        # London-NY Overlap (12-16 UTC) - BEST
        if 12 <= hour <= 16:
            return {
                "session": "london_newyork_overlap",
                "volatility_boost": 1.4,
                "timing_boost": 1.3,
                "quality": "EXCELLENT"
            }
        
        # London Session (7-16 UTC) - GOOD
        elif 7 <= hour <= 16:
            return {
                "session": "london",
                "volatility_boost": 1.2,
                "timing_boost": 1.1,
                "quality": "GOOD"
            }
        
        # New York Session (12-21 UTC) - GOOD
        elif 12 <= hour <= 21:
            return {
                "session": "newyork", 
                "volatility_boost": 1.15,
                "timing_boost": 1.05,
                "quality": "GOOD"
            }
        
        # Asian Session (23-8 UTC) - MODERATE
        elif 23 <= hour or hour <= 8:
            return {
                "session": "asian",
                "volatility_boost": 0.85,
                "timing_boost": 0.9,
                "quality": "MODERATE"
            }
        
        # Off Session - POOR
        else:
            return {
                "session": "off_session",
                "volatility_boost": 0.6,
                "timing_boost": 0.7,
                "quality": "POOR"
            }
    
    def _check_news_impact(self, hour: int) -> float:
        """Check if current time is near major news releases"""
        try:
            # Check if within 1 hour of major news
            for news in self.news_times:
                if abs(hour - news["time"]) <= 1:
                    return 0.7  # Reduce trading during news
            
            # Special times to avoid
            if hour in [0, 1]:  # Market open/close times
                return 0.8
            
            return 1.0  # Normal times
            
        except Exception:
            return 1.0
    
    def _get_session_recommendation(self, adjustment: float) -> str:
        """Get trading recommendation based on adjustment factor"""
        if adjustment >= 1.3:
            return "EXCELLENT - Prime trading time"
        elif adjustment >= 1.1:
            return "GOOD - Favorable conditions"
        elif adjustment >= 0.9:
            return "NORMAL - Standard conditions"
        elif adjustment >= 0.7:
            return "CAUTION - Reduced activity"
        else:
            return "AVOID - Poor conditions"
    
    def get_optimal_trading_hours(self) -> Dict[str, Any]:
        """Get recommended trading hours"""
        return {
            "best_hours": [12, 13, 14, 15, 16],  # London-NY overlap
            "good_hours": [7, 8, 9, 10, 11, 17, 18, 19, 20, 21],
            "moderate_hours": [23, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            "avoid_hours": [22],  # Transition period
            "recommendations": {
                "scalping": "12-16 UTC (London-NY overlap)",
                "swing_trading": "7-21 UTC (London + NY sessions)",
                "position_trading": "Any time with proper risk management"
            }
        }
    
    def is_weekend_approaching(self, dt: datetime = None) -> Dict[str, Any]:
        """Check if weekend is approaching (Friday evening)"""
        try:
            if dt is None:
                dt = datetime.now(pytz.UTC)
            
            is_friday = dt.weekday() == 4
            is_evening = dt.hour >= 20
            
            weekend_approaching = is_friday and is_evening
            
            return {
                "weekend_approaching": weekend_approaching,
                "is_friday": is_friday,
                "is_evening": is_evening,
                "hours_to_weekend": (24 - dt.hour) if is_friday else None,
                "recommendation": "CLOSE_POSITIONS" if weekend_approaching else "NORMAL"
            }
            
        except Exception as e:
            logger.error(f"Error checking weekend approach: {e}")
            return {
                "weekend_approaching": False,
                "recommendation": "NORMAL"
            }