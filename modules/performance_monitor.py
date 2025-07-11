#!/usr/bin/env python3
"""
Performance Monitor Module - Auto Upgrade System
Automatically tracks performance and upgrades position count based on metrics
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Auto performance monitoring dan upgrade system"""
    
    def __init__(self, config_path: str = "performance_data.json"):
        self.config_path = config_path
        self.performance_data = self._load_performance_data()
        
        # Upgrade criteria
        self.upgrade_criteria = {
            "min_trades": 30,
            "min_win_rate": 0.65,
            "min_profit_factor": 1.5,
            "max_drawdown": 0.10,
            "min_track_record_days": 60,
            "min_balance": 15.0
        }
        
        # Position count tiers
        self.position_tiers = {
            "tier_1": {"max_positions": 1, "min_balance": 5, "min_trades": 0},
            "tier_2": {"max_positions": 2, "min_balance": 15, "min_trades": 30},
            "tier_3": {"max_positions": 3, "min_balance": 50, "min_trades": 100},
            "tier_4": {"max_positions": 4, "min_balance": 100, "min_trades": 200}
        }
    
    def _load_performance_data(self) -> Dict:
        """Load performance data dari file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "trades": [],
                    "current_balance": 5.0,
                    "initial_balance": 5.0,
                    "upgrade_history": [],
                    "current_tier": "tier_1",
                    "last_upgrade": None
                }
        except Exception as e:
            logger.error(f"Error loading performance data: {e}")
            return {
                "trades": [],
                "current_balance": 5.0,
                "initial_balance": 5.0,
                "upgrade_history": [],
                "current_tier": "tier_1",
                "last_upgrade": None
            }
    
    def _save_performance_data(self):
        """Save performance data ke file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.performance_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving performance data: {e}")
    
    def add_trade(self, trade_data: Dict):
        """Add new trade ke performance tracking"""
        try:
            trade_data['timestamp'] = datetime.now().isoformat()
            self.performance_data['trades'].append(trade_data)
            self._save_performance_data()
            
            # Auto check untuk upgrade
            self.check_and_upgrade()
            
        except Exception as e:
            logger.error(f"Error adding trade: {e}")
    
    def update_balance(self, new_balance: float):
        """Update current balance"""
        try:
            self.performance_data['current_balance'] = new_balance
            self._save_performance_data()
            
            # Auto check untuk upgrade
            self.check_and_upgrade()
            
        except Exception as e:
            logger.error(f"Error updating balance: {e}")
    
    def calculate_performance_metrics(self) -> Dict:
        """Calculate performance metrics"""
        try:
            trades = self.performance_data['trades']
            if not trades:
                return {
                    "total_trades": 0,
                    "win_rate": 0,
                    "profit_factor": 0,
                    "max_drawdown": 0,
                    "track_record_days": 0,
                    "current_balance": self.performance_data['current_balance']
                }
            
            # Calculate metrics
            total_trades = len(trades)
            winning_trades = [t for t in trades if t.get('profit_pct', 0) > 0]
            losing_trades = [t for t in trades if t.get('profit_pct', 0) < 0]
            
            win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
            
            # Calculate profit factor
            total_profit = sum(t.get('profit_pct', 0) for t in winning_trades)
            total_loss = abs(sum(t.get('profit_pct', 0) for t in losing_trades))
            profit_factor = total_profit / total_loss if total_loss > 0 else 0
            
            # Calculate max drawdown
            max_drawdown = self._calculate_max_drawdown(trades)
            
            # Calculate track record days
            if trades:
                first_trade = datetime.fromisoformat(trades[0]['timestamp'])
                last_trade = datetime.fromisoformat(trades[-1]['timestamp'])
                track_record_days = (last_trade - first_trade).days
            else:
                track_record_days = 0
            
            return {
                "total_trades": total_trades,
                "win_rate": win_rate,
                "profit_factor": profit_factor,
                "max_drawdown": max_drawdown,
                "track_record_days": track_record_days,
                "current_balance": self.performance_data['current_balance'],
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades)
            }
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return {
                "total_trades": 0,
                "win_rate": 0,
                "profit_factor": 0,
                "max_drawdown": 0,
                "track_record_days": 0,
                "current_balance": self.performance_data['current_balance']
            }
    
    def _calculate_max_drawdown(self, trades: List[Dict]) -> float:
        """Calculate maximum drawdown"""
        try:
            if not trades:
                return 0
            
            balance = self.performance_data['initial_balance']
            peak_balance = balance
            max_drawdown = 0
            
            for trade in trades:
                profit_pct = trade.get('profit_pct', 0)
                balance *= (1 + profit_pct)
                
                if balance > peak_balance:
                    peak_balance = balance
                
                drawdown = (peak_balance - balance) / peak_balance
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
            
            return max_drawdown
            
        except Exception as e:
            logger.error(f"Error calculating drawdown: {e}")
            return 0
    
    def check_and_upgrade(self) -> Optional[Dict]:
        """Check if upgrade is possible dan return upgrade config"""
        try:
            metrics = self.calculate_performance_metrics()
            current_balance = metrics['current_balance']
            current_tier = self.performance_data['current_tier']
            
            # Check upgrade criteria
            can_upgrade = (
                metrics['total_trades'] >= self.upgrade_criteria['min_trades'] and
                metrics['win_rate'] >= self.upgrade_criteria['min_win_rate'] and
                metrics['profit_factor'] >= self.upgrade_criteria['min_profit_factor'] and
                metrics['max_drawdown'] <= self.upgrade_criteria['max_drawdown'] and
                metrics['track_record_days'] >= self.upgrade_criteria['min_track_record_days'] and
                current_balance >= self.upgrade_criteria['min_balance']
            )
            
            if not can_upgrade:
                return None
            
            # Determine next tier
            next_tier = self._get_next_tier(current_tier, current_balance, metrics['total_trades'])
            
            if next_tier and next_tier != current_tier:
                upgrade_config = self._generate_upgrade_config(next_tier, metrics)
                
                # Record upgrade
                upgrade_record = {
                    "timestamp": datetime.now().isoformat(),
                    "from_tier": current_tier,
                    "to_tier": next_tier,
                    "metrics": metrics,
                    "config": upgrade_config
                }
                
                self.performance_data['upgrade_history'].append(upgrade_record)
                self.performance_data['current_tier'] = next_tier
                self.performance_data['last_upgrade'] = datetime.now().isoformat()
                self._save_performance_data()
                
                logger.info(f"🔄 AUTO UPGRADE: {current_tier} → {next_tier}")
                return upgrade_config
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking upgrade: {e}")
            return None
    
    def _get_next_tier(self, current_tier: str, balance: float, total_trades: int) -> Optional[str]:
        """Get next tier based on current performance"""
        try:
            tier_order = ["tier_1", "tier_2", "tier_3", "tier_4"]
            current_index = tier_order.index(current_tier)
            
            for i in range(current_index + 1, len(tier_order)):
                next_tier = tier_order[i]
                tier_requirements = self.position_tiers[next_tier]
                
                if (balance >= tier_requirements['min_balance'] and 
                    total_trades >= tier_requirements['min_trades']):
                    return next_tier
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting next tier: {e}")
            return None
    
    def _generate_upgrade_config(self, new_tier: str, metrics: Dict) -> Dict:
        """Generate new config untuk upgrade"""
        try:
            tier_config = self.position_tiers[new_tier]
            max_positions = tier_config['max_positions']
            
            # Generate config based on tier
            if new_tier == "tier_2":  # 1 → 2 positions
                config = {
                    "max_open_trades": 2,
                    "position_sizing": {
                        "method": "kelly_partial",
                        "fraction": 0.6  # Reduced from 0.8
                    },
                    "confidence_threshold": 70,  # Reduced from 75
                    "risk_level": "conservative"
                }
            elif new_tier == "tier_3":  # 2 → 3 positions
                config = {
                    "max_open_trades": 3,
                    "position_sizing": {
                        "method": "kelly_partial",
                        "fraction": 0.5  # Further reduced
                    },
                    "confidence_threshold": 65,
                    "risk_level": "balanced"
                }
            elif new_tier == "tier_4":  # 3 → 4 positions
                config = {
                    "max_open_trades": 4,
                    "position_sizing": {
                        "method": "kelly_partial",
                        "fraction": 0.4
                    },
                    "confidence_threshold": 60,
                    "risk_level": "balanced"
                }
            else:
                config = {}
            
            return {
                "tier": new_tier,
                "max_positions": max_positions,
                "config": config,
                "reason": f"Performance metrics met upgrade criteria: WR={metrics['win_rate']:.1%}, PF={metrics['profit_factor']:.2f}, Trades={metrics['total_trades']}"
            }
            
        except Exception as e:
            logger.error(f"Error generating upgrade config: {e}")
            return {}
    
    def get_current_status(self) -> Dict:
        """Get current performance status"""
        try:
            metrics = self.calculate_performance_metrics()
            current_tier = self.performance_data['current_tier']
            tier_config = self.position_tiers[current_tier]
            
            return {
                "current_tier": current_tier,
                "max_positions": tier_config['max_positions'],
                "metrics": metrics,
                "upgrade_criteria": self.upgrade_criteria,
                "next_upgrade_requirements": self._get_upgrade_requirements(metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {}
    
    def _get_upgrade_requirements(self, metrics: Dict) -> Dict:
        """Get requirements untuk next upgrade"""
        try:
            current_tier = self.performance_data['current_tier']
            next_tier = self._get_next_tier(current_tier, metrics['current_balance'], metrics['total_trades'])
            
            if not next_tier:
                return {"status": "No upgrade available"}
            
            next_tier_config = self.position_tiers[next_tier]
            
            return {
                "next_tier": next_tier,
                "requirements": {
                    "min_balance": next_tier_config['min_balance'],
                    "min_trades": next_tier_config['min_trades'],
                    "current_balance": metrics['current_balance'],
                    "current_trades": metrics['total_trades'],
                    "balance_met": metrics['current_balance'] >= next_tier_config['min_balance'],
                    "trades_met": metrics['total_trades'] >= next_tier_config['min_trades']
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting upgrade requirements: {e}")
            return {"status": "Error calculating requirements"}