#!/usr/bin/env python3
"""
Position Sizing Module - Kelly Criterion & Risk Management
Professional grade position sizing untuk optimal capital allocation
"""

import numpy as np
from typing import Dict, List
import logging
from modules.constants import get_fee_rate

logger = logging.getLogger(__name__)

class KellyCriterionCalculator:
    """Kelly Criterion untuk optimal position sizing"""
    
    def __init__(self):
        self.default_win_rate = 0.6
        self.default_avg_win = 0.015
        self.default_avg_loss = 0.01
        
    def calculate_kelly_percentage(self, win_rate: float, avg_win: float, avg_loss: float) -> float:
        """
        Kelly Criterion: f* = (bp - q) / b
        where:
        - f* = fraction of capital to wager
        - b = odds received on the wager (avg_win / avg_loss)
        - p = probability of winning
        - q = probability of losing (1 - p)
        """
        try:
            if avg_loss <= 0 or win_rate <= 0 or win_rate >= 1:
                return 0.01  # Conservative fallback
            
            p = win_rate
            q = 1 - p
            b = avg_win / abs(avg_loss)
            
            kelly_f = (b * p - q) / b
            
            # Safety caps
            kelly_f = max(0, min(kelly_f, 0.25))  # Cap at 25%
            
            # For small accounts, use fractional Kelly (more conservative)
            if kelly_f > 0.05:
                kelly_f = kelly_f * 0.4  # Use 40% of Kelly for safety
            
            return kelly_f
            
        except Exception as e:
            logger.error(f"Error calculating Kelly percentage: {e}")
            return 0.02  # Conservative fallback
    
    def update_performance_data(self, trades: List[Dict]) -> Dict[str, float]:
        """Update performance metrics dari trading history"""
        try:
            if len(trades) < 5:
                # Use default values for insufficient data
                return {
                    "win_rate": self.default_win_rate,
                    "avg_win": self.default_avg_win,
                    "avg_loss": self.default_avg_loss,
                    "kelly_percentage": self.calculate_kelly_percentage(
                        self.default_win_rate, 
                        self.default_avg_win, 
                        self.default_avg_loss
                    ),
                    "total_trades": len(trades)
                }
            
            # Separate wins and losses
            wins = [t["profit_pct"] for t in trades if t.get("profit_pct", 0) > 0]
            losses = [abs(t["profit_pct"]) for t in trades if t.get("profit_pct", 0) < 0]
            
            # Calculate metrics
            win_rate = len(wins) / len(trades) if trades else 0
            avg_win = np.mean(wins) if wins else self.default_avg_win
            avg_loss = np.mean(losses) if losses else self.default_avg_loss
            
            kelly_pct = self.calculate_kelly_percentage(win_rate, avg_win, avg_loss)
            
            return {
                "win_rate": win_rate,
                "avg_win": avg_win,
                "avg_loss": avg_loss,
                "kelly_percentage": kelly_pct,
                "total_trades": len(trades),
                "winning_trades": len(wins),
                "losing_trades": len(losses)
            }
            
        except Exception as e:
            logger.error(f"Error updating performance data: {e}")
            return {
                "win_rate": self.default_win_rate,
                "avg_win": self.default_avg_win,
                "avg_loss": self.default_avg_loss,
                "kelly_percentage": 0.02,
                "total_trades": 0
            }
    
    def calculate_position_size(self, balance: float, kelly_pct: float, confidence_score: float) -> Dict[str, float]:
        """
        Calculate optimal position size berdasarkan:
        - Kelly Criterion percentage
        - Current confidence score (0-100)
        - Account balance
        """
        try:
            # Base Kelly percentage
            base_kelly = kelly_pct
            
            # Adjust based on confidence score
            confidence_multiplier = confidence_score / 100
            
            # Conservative adjustment untuk small accounts + dynamic tiers
            adjusted_kelly = base_kelly * confidence_multiplier

            # Dynamic risk brackets - OPTIMIZED MODE
            if balance < 20:
                min_risk = 0.005   # 0.5%
                max_risk = 0.035   # 3.5% (moderate)
            elif balance < 100:
                min_risk = 0.007   # 0.7%
                max_risk = 0.045   # 4.5% (optimized)
            elif balance < 500:
                min_risk = 0.005
                max_risk = 0.04    # 4% (optimized)
            else:
                min_risk = 0.005
                max_risk = 0.035   # 3.5% (optimized)

            final_risk_pct = max(min_risk, min(adjusted_kelly, max_risk))
            
            # Calculate actual position size
            risk_amount = balance * final_risk_pct
            # Adjust risk to account for total fees so that risk+fee <= risk_amount
            fee_buffer = balance * get_fee_rate()
            risk_amount = max(risk_amount - fee_buffer, 0)
            
            # Auto leverage calculation
            leverage_cap = self.calculate_auto_leverage(symbol, balance, market_data)

            return {
                "risk_percentage": final_risk_pct,
                "risk_amount": risk_amount,
                "kelly_suggested": base_kelly,
                "confidence_multiplier": confidence_multiplier,
                "max_leverage": min(leverage_cap, 1 + confidence_multiplier * 2)  # 1x-5x dynamic
            }
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return {
                "risk_percentage": 0.02,
                "risk_amount": balance * 0.02,
                "kelly_suggested": 0.02,
                "confidence_multiplier": 0.6,
                "max_leverage": 2
            }
    
    def get_portfolio_heat(self, active_positions: List[Dict], balance: float) -> Dict[str, float]:
         """Calculate portfolio heat (total risk across positions)"""
         try:
             if not active_positions:
                 return {
                     "total_heat": 0.0,
                     "position_count": 0,
                     "max_heat_reached": False
                 }
             
             total_risk_usd = 0.0
             for position in active_positions:
                 position_value = abs(float(position.get('positionAmt', 0))) * float(position.get('markPrice', 0))
                 total_risk_usd += position_value
             
             # Dynamic heat thresholds
             if balance < 100:
                 max_heat_pct = 0.10  # 10%
             elif balance < 500:
                 max_heat_pct = 0.12 # 12%
             else:
                 max_heat_pct = 0.12  # keep 12% for big account as well
             
             current_heat_pct = total_risk_usd / balance if balance > 0 else 0
             
             return {
                 "total_heat": current_heat_pct,
                 "position_count": len(active_positions),
                 "max_heat_reached": current_heat_pct > max_heat_pct,
                 "max_heat_threshold": max_heat_pct
             }
         except Exception as e:
             logger.error(f"Error calculating portfolio heat: {e}")
             return {
                 "total_heat": 0.0,
                 "position_count": 0,
                 "max_heat_reached": False
             }

    def calculate_auto_leverage(self, symbol: str, balance: float, market_data: Dict = None) -> float:
        """Calculate optimal leverage based on market conditions, balance, and symbol"""
        try:
            # Base leverage by balance tier - OPTIMIZED
            if balance < 20:
                base_leverage = 2.5
            elif balance < 100:
                base_leverage = 3.5  # Increased from 3.0
            elif balance < 500:
                base_leverage = 4.0  # Increased from 3.5
            else:
                base_leverage = 4.5  # Increased from 4.0
            
            # Symbol-specific adjustment
            symbol_adjustment = 1.0
            if symbol in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]:
                # Major coins - more stable, higher leverage
                symbol_adjustment = 1.2
            elif symbol in ["DOGEUSDT", "SHIBUSDT", "PEPEUSDT"]:
                # Meme coins - very volatile, lower leverage
                symbol_adjustment = 0.7
            elif symbol in ["ADAUSDT", "SOLUSDT", "MATICUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT"]:
                # Altcoins - moderate volatility
                symbol_adjustment = 0.9
            
            # Volatility-based adjustment
            volatility_adjustment = 1.0
            if market_data and 'volatility' in market_data:
                volatility = market_data['volatility']
                if volatility < 0.02:  # < 2% volatility
                    volatility_adjustment = 1.3  # Higher leverage
                elif volatility < 0.04:  # 2-4% volatility
                    volatility_adjustment = 1.0  # Normal leverage
                elif volatility < 0.06:  # 4-6% volatility
                    volatility_adjustment = 0.8  # Lower leverage
                else:  # > 6% volatility
                    volatility_adjustment = 0.6  # Much lower leverage
            
            # Calculate final leverage
            final_leverage = base_leverage * symbol_adjustment * volatility_adjustment
            
            # Apply safety limits - OPTIMIZED
            max_leverage = 6.0 if balance >= 100 else 4.0  # Increased limits
            min_leverage = 1.5
            
            final_leverage = max(min_leverage, min(final_leverage, max_leverage))
            
            logger.info(f"AUTO LEVERAGE: {symbol} - Base:{base_leverage:.1f} Symbol:{symbol_adjustment:.1f} Vol:{volatility_adjustment:.1f} Final:{final_leverage:.1f}")
            
            return round(final_leverage, 1)
            
        except Exception as e:
            logger.error(f"Error calculating auto leverage: {e}")
            # Fallback to safe leverage
            return 2.5 if balance < 20 else 3.0