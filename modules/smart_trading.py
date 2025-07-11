#!/usr/bin/env python3
"""
Smart Trading Module - SUPER BRILLIANT PROFESSIONAL Edition
Enhanced with genius-level pattern recognition and confluence analysis
"""

import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Tuple
import logging

from .market_analysis import MarketRegimeDetector, LiquidityZoneDetector, MarketStructureAnalyzer
from .position_sizing import KellyCriterionCalculator
from .session_timing import TradingSessionAnalyzer
from .indicators import SmartIndicators

logger = logging.getLogger(__name__)

class SmartEntry:
    """SUPER BRILLIANT PRO TRADER - Genius Level Intelligence"""
    
    def __init__(self, config):
        self.config = config
        
        # Initialize professional modules
        self.regime_detector = MarketRegimeDetector()
        self.liquidity_detector = LiquidityZoneDetector()
        self.structure_analyzer = MarketStructureAnalyzer()
        self.kelly_calculator = KellyCriterionCalculator()
        self.session_analyzer = TradingSessionAnalyzer()
        
        # Performance tracking
        self.trades_history = []
        
        # GENIUS FEATURES - Pattern recognition database
        self.pattern_memory = {}
        self.confluence_threshold = 70  # Minimum confluence untuk entry
    
    def analyze_entry(self, klines_data) -> Dict[str, Any]:
        """SUPER BRILLIANT Entry Analysis - Genius Level Intelligence"""
        try:
            if len(klines_data) < 100:  # Butuh data lebih banyak untuk genius analysis
                return {"action": "wait", "confidence": 0, "reason": "Data insufficient untuk genius analysis"}
            
            # Extract comprehensive price data
            highs = [float(k[2]) for k in klines_data]
            lows = [float(k[3]) for k in klines_data]
            opens = [float(k[1]) for k in klines_data]
            closes = [float(k[4]) for k in klines_data]
            volumes = [float(k[5]) for k in klines_data]
            
            score = 0
            signals = []
            pro_analysis = {}
            genius_features = {}
            
            # 1. ENHANCED MARKET REGIME (25 points) - Improved intelligence
            try:
                regime_data = self.regime_detector.detect_market_regime(closes, volumes)
                regime_score = self._score_enhanced_regime(regime_data, closes, volumes)
                score += regime_score
                signals.append(f"Regime: {regime_data['regime']} ({regime_data['confidence']:.1f}%)")
                pro_analysis['market_regime'] = regime_data
            except Exception as e:
                logger.error(f"Error in regime analysis: {e}")
                score += 5  # Default score
            
            # 2. GENIUS PATTERN RECOGNITION (20 points) - NEW SUPER FEATURE
            try:
                pattern_data = self._detect_genius_patterns(highs, lows, opens, closes, volumes)
                pattern_score = self._score_pattern_recognition(pattern_data)
                score += pattern_score
                signals.append(f"Patterns: {pattern_data['primary_pattern']}")
                genius_features['pattern_recognition'] = pattern_data
            except Exception as e:
                logger.error(f"Error in pattern analysis: {e}")
                score += 5  # Default score
            
            # 3. ADVANCED LIQUIDITY ZONES (20 points) - Enhanced
            try:
                liquidity_data = self.liquidity_detector.detect_liquidity_zones(closes)
                liquidity_enhanced = self._enhance_liquidity_analysis(liquidity_data, highs, lows, volumes)
                liquidity_score = self._score_enhanced_liquidity(liquidity_enhanced, closes[-1])
                score += liquidity_score
                signals.append(f"Liquidity: {liquidity_enhanced['enhanced_bias']}")
                pro_analysis['liquidity_zones'] = liquidity_enhanced
            except Exception as e:
                logger.error(f"Error in liquidity analysis: {e}")
                score += 5  # Default score
            
            # 4. MULTI-TIMEFRAME CONFLUENCE (15 points) - GENIUS FEATURE
            try:
                confluence_data = self._analyze_multi_timeframe_confluence(closes, volumes)
                confluence_score = self._score_confluence_analysis(confluence_data)
                score += confluence_score
                signals.append(f"Confluence: {confluence_data['alignment_strength']:.1f}%")
                genius_features['confluence'] = confluence_data
            except Exception as e:
                logger.error(f"Error in confluence analysis: {e}")
                score += 3  # Default score
            
            # 5. ADVANCED MARKET STRUCTURE (10 points) - Enhanced
            try:
                structure_data = self.structure_analyzer.analyze_market_structure(closes)
                structure_enhanced = self._enhance_structure_analysis(structure_data, highs, lows)
                structure_score = self._score_enhanced_structure(structure_enhanced)
                score += structure_score
                signals.append(f"Structure: {structure_enhanced['enhanced_bias']}")
                pro_analysis['market_structure'] = structure_enhanced
            except Exception as e:
                logger.error(f"Error in structure analysis: {e}")
                score += 3  # Default score
            
            # 6. GENIUS VOLUME ANALYSIS (10 points) - NEW BRILLIANT FEATURE
            try:
                volume_genius = self._analyze_genius_volume_profile(closes, volumes, highs, lows)
                volume_score = self._score_volume_genius(volume_genius)
                score += volume_score
                signals.append(f"Volume: {volume_genius['profile_bias']}")
                genius_features['volume_profile'] = volume_genius
            except Exception as e:
                logger.error(f"Error in volume analysis: {e}")
                score += 3  # Default score
            
            # Apply session timing with GENIUS enhancement
            session_data = self.session_analyzer.get_session_adjustment_factor()
            session_enhanced = self._enhance_session_analysis(session_data, closes, volumes)
            final_score = score * session_enhanced['enhanced_multiplier']
            final_score = min(final_score, 100)
            
            # GENIUS DIRECTION DETERMINATION with confluence
            direction = self._determine_genius_direction(pro_analysis, genius_features, closes[-1])
            
            # OPTIMAL POSITION SIZING with genius risk assessment
            kelly_data = self.kelly_calculator.update_performance_data(self.trades_history)
            position_sizing = self._calculate_genius_position_size(final_score, kelly_data, pro_analysis, genius_features)
            
            # GENIUS CONFIDENCE ASSESSMENT
            genius_confidence = self._assess_genius_confidence(final_score, pro_analysis, genius_features)
            
            # Generate BRILLIANT reason
            reason = f"🧠 Genius Score: {final_score:.1f}/100 | " + " | ".join(signals[:4])
            reason += f" | Kelly: {kelly_data['kelly_percentage']:.3f} | Confidence: {genius_confidence['level']}"
            
            return {
                "action": direction.lower(),
                "confidence": final_score,
                "reason": reason,
                "pro_analysis": pro_analysis,
                "genius_features": genius_features,
                "position_sizing": position_sizing,
                "kelly_data": kelly_data,
                "confidence_level": genius_confidence['level'],
                "genius_score": genius_confidence['genius_score'],
                "risk_reward_ratio": genius_confidence.get('risk_reward', 1.0)
            }
            
        except Exception as e:
            logger.error(f"Error in genius entry analysis: {e}")
            return {"action": "wait", "confidence": 0, "reason": "Error dalam genius analysis"}
    
    def _score_enhanced_regime(self, regime_data: Dict, prices: List[float], volumes: List[float]) -> float:
        """Enhanced regime scoring with trend strength"""
        regime = regime_data.get('regime', 'insufficient_data')
        confidence = regime_data.get('confidence', 0)
        
        # Base scores enhanced
        regime_scores = {
            'trending_strong': 25,
            'trending_weak': 18,
            'volatile': 12,
            'ranging': 8,
            'insufficient_data': 0
        }
        
        base_score = regime_scores.get(regime, 0)
        confidence_multiplier = confidence / 100
        
        # Add trend strength analysis
        if len(prices) >= 50:
            trend_strength = self._calculate_trend_strength(prices)
            trend_multiplier = 1.0 + (trend_strength / 100)  # Max +100% boost
        else:
            trend_multiplier = 1.0
        
        # Volume confirmation
        volume_confirmation = min(regime_data.get('volume_ratio', 1.0), 2.5) / 2.5
        
        return base_score * confidence_multiplier * trend_multiplier * volume_confirmation
    
    def _detect_genius_patterns(self, highs: List[float], lows: List[float], opens: List[float], closes: List[float], volumes: List[float]) -> Dict:
        """GENIUS Pattern Recognition - Advanced candlestick and price action patterns"""
        patterns = {
            'bullish_patterns': [],
            'bearish_patterns': [],
            'continuation_patterns': [],
            'reversal_patterns': []
        }
        
        pattern_strength = 0
        primary_pattern = "none"
        
        # Candlestick Pattern Detection
        candlestick_patterns = self._detect_candlestick_patterns(highs, lows, opens, closes)
        patterns.update(candlestick_patterns)
        
        # Price Action Patterns
        price_action = self._detect_price_action_patterns(highs, lows, closes)
        patterns.update(price_action)
        
        # Support/Resistance Break Patterns
        sr_patterns = self._detect_support_resistance_breaks(highs, lows, closes, volumes)
        patterns.update(sr_patterns)
        
        # Calculate pattern strength
        total_bullish = len(patterns['bullish_patterns'])
        total_bearish = len(patterns['bearish_patterns'])
        total_continuation = len(patterns['continuation_patterns'])
        
        if total_bullish > total_bearish + 1:
            pattern_strength = min(total_bullish * 20, 100)
            primary_pattern = f"bullish_dominant ({total_bullish} signals)"
        elif total_bearish > total_bullish + 1:
            pattern_strength = min(total_bearish * 20, 100)
            primary_pattern = f"bearish_dominant ({total_bearish} signals)"
        elif total_continuation > 2:
            pattern_strength = min(total_continuation * 15, 80)
            primary_pattern = f"continuation ({total_continuation} signals)"
        else:
            primary_pattern = "neutral"
        
        return {
            'patterns': patterns,
            'pattern_strength': pattern_strength,
            'primary_pattern': primary_pattern,
            'bullish_count': total_bullish,
            'bearish_count': total_bearish,
            'continuation_count': total_continuation
        }
    
    def _detect_candlestick_patterns(self, highs: List[float], lows: List[float], opens: List[float], closes: List[float]) -> Dict:
        """Detect major candlestick patterns"""
        patterns = {'bullish_patterns': [], 'bearish_patterns': [], 'continuation_patterns': [], 'reversal_patterns': []}
        
        if len(closes) < 10:
            return patterns
        
        for i in range(2, len(closes)):
            # Doji detection
            body_size = abs(closes[i] - opens[i])
            candle_range = highs[i] - lows[i]
            
            if candle_range > 0.0001 and body_size / candle_range < 0.1:  # Prevent division by zero
                patterns['reversal_patterns'].append(f"doji_at_{i}")
            
            # Hammer/Shooting Star
            if candle_range > 0.0001:  # Prevent division by zero
                lower_shadow = (min(opens[i], closes[i]) - lows[i]) / candle_range
                upper_shadow = (highs[i] - max(opens[i], closes[i])) / candle_range
                
                if lower_shadow > 0.6 and upper_shadow < 0.1:  # Hammer
                    if closes[i] > opens[i]:
                        patterns['bullish_patterns'].append(f"hammer_at_{i}")
                
                if upper_shadow > 0.6 and lower_shadow < 0.1:  # Shooting Star
                    if opens[i] > closes[i]:
                        patterns['bearish_patterns'].append(f"shooting_star_at_{i}")
            
            # Engulfing patterns
            if i >= 1:
                prev_body = abs(closes[i-1] - opens[i-1])
                curr_body = abs(closes[i] - opens[i])
                
                # Bullish Engulfing
                if (opens[i-1] > closes[i-1] and  # Previous bearish
                    closes[i] > opens[i] and      # Current bullish
                    closes[i] > opens[i-1] and   # Engulfs previous open
                    opens[i] < closes[i-1] and   # Engulfs previous close
                    curr_body > prev_body * 1.1): # Larger body
                    patterns['bullish_patterns'].append(f"bullish_engulfing_at_{i}")
                
                # Bearish Engulfing
                if (closes[i-1] > opens[i-1] and  # Previous bullish
                    opens[i] > closes[i] and      # Current bearish
                    opens[i] > closes[i-1] and   # Engulfs previous close
                    closes[i] < opens[i-1] and   # Engulfs previous open
                    curr_body > prev_body * 1.1): # Larger body
                    patterns['bearish_patterns'].append(f"bearish_engulfing_at_{i}")
        
        return patterns
    
    def _detect_price_action_patterns(self, highs: List[float], lows: List[float], closes: List[float]) -> Dict:
        """Detect price action patterns like double tops, head and shoulders, etc."""
        patterns = {'continuation_patterns': [], 'reversal_patterns': []}
        
        if len(closes) < 20:
            return patterns
        
        # Find significant highs and lows
        swing_highs = self._find_swing_points(highs, 'high')
        swing_lows = self._find_swing_points(lows, 'low')
        
        # Double Top/Bottom detection
        if len(swing_highs) >= 2:
            last_high = swing_highs[-1]
            prev_high = swing_highs[-2]
            if abs(last_high['price'] - prev_high['price']) / last_high['price'] < 0.02:
                patterns['reversal_patterns'].append("potential_double_top")
        
        if len(swing_lows) >= 2:
            last_low = swing_lows[-1]
            prev_low = swing_lows[-2]
            if abs(last_low['price'] - prev_low['price']) / last_low['price'] < 0.02:
                patterns['reversal_patterns'].append("potential_double_bottom")
        
        # Trend continuation patterns
        if len(closes) >= 30:
            trend_direction = self._get_trend_direction(closes[-30:])
            if trend_direction == 'uptrend':
                # Look for higher lows
                if len(swing_lows) >= 2 and swing_lows[-1]['price'] > swing_lows[-2]['price']:
                    patterns['continuation_patterns'].append("higher_low_continuation")
            elif trend_direction == 'downtrend':
                # Look for lower highs
                if len(swing_highs) >= 2 and swing_highs[-1]['price'] < swing_highs[-2]['price']:
                    patterns['continuation_patterns'].append("lower_high_continuation")
        
        return patterns
    
    def _detect_support_resistance_breaks(self, highs: List[float], lows: List[float], closes: List[float], volumes: List[float]) -> Dict:
        """Detect support/resistance level breaks"""
        patterns = {'bullish_patterns': [], 'bearish_patterns': []}
        
        if len(closes) < 50:
            return patterns
        
        # Find key levels
        key_levels = self._identify_key_levels(highs, lows, closes)
        current_price = closes[-1]
        
        # Volume confirmation
        avg_volume = np.mean(volumes[-20:]) if len(volumes) >= 20 else volumes[-1]
        current_volume = volumes[-1]
        volume_confirmation = current_volume > avg_volume * 1.2
        
        for level in key_levels:
            distance_pct = abs(current_price - level['price']) / level['price']
            
            # Recent break detection
            if distance_pct < 0.005:  # Within 0.5% of key level
                if level['type'] == 'resistance' and current_price > level['price']:
                    if volume_confirmation:
                        patterns['bullish_patterns'].append(f"resistance_break_with_volume")
                    else:
                        patterns['bullish_patterns'].append(f"resistance_break")
                
                elif level['type'] == 'support' and current_price < level['price']:
                    if volume_confirmation:
                        patterns['bearish_patterns'].append(f"support_break_with_volume")
                    else:
                        patterns['bearish_patterns'].append(f"support_break")
        
        return patterns
    
    def _analyze_multi_timeframe_confluence(self, closes: List[float], volumes: List[float]) -> Dict:
        """Multi-timeframe analysis for confluence"""
        confluence_data = {
            'short_term_bias': 'neutral',
            'medium_term_bias': 'neutral',
            'long_term_bias': 'neutral',
            'alignment_strength': 0
        }
        
        if len(closes) < 100:
            return confluence_data
        
        # Short-term (last 20 candles)
        short_term = closes[-20:]
        short_trend = self._get_trend_direction(short_term)
        confluence_data['short_term_bias'] = short_trend
        
        # Medium-term (last 50 candles)
        medium_term = closes[-50:]
        medium_trend = self._get_trend_direction(medium_term)
        confluence_data['medium_term_bias'] = medium_trend
        
        # Long-term (last 100 candles)
        long_term = closes[-100:]
        long_trend = self._get_trend_direction(long_term)
        confluence_data['long_term_bias'] = long_trend
        
        # Calculate alignment strength
        trends = [short_trend, medium_trend, long_trend]
        
        if all(t == 'uptrend' for t in trends):
            confluence_data['alignment_strength'] = 100
        elif all(t == 'downtrend' for t in trends):
            confluence_data['alignment_strength'] = 100
        elif trends.count('uptrend') == 2:
            confluence_data['alignment_strength'] = 75
        elif trends.count('downtrend') == 2:
            confluence_data['alignment_strength'] = 75
        elif all(t == 'sideways' for t in trends):
            confluence_data['alignment_strength'] = 30
        else:
            confluence_data['alignment_strength'] = 50
        
        return confluence_data
    
    def _enhance_liquidity_analysis(self, liquidity_data: Dict, highs: List[float], lows: List[float], volumes: List[float]) -> Dict:
        """Enhanced liquidity analysis with volume profile"""
        enhanced = liquidity_data.copy()
        
        # Add volume-weighted analysis
        if len(volumes) >= 20:
            high_volume_zones = self._identify_high_volume_zones(highs, lows, volumes)
            enhanced['high_volume_zones'] = high_volume_zones
            
            # Enhanced bias calculation
            current_price = (highs[-1] + lows[-1]) / 2
            volume_bias = self._calculate_volume_bias(current_price, high_volume_zones)
            
            # Combine original bias with volume bias
            original_bias = liquidity_data.get('current_bias', 'neutral')
            enhanced_bias = self._combine_bias_signals(original_bias, volume_bias)
            enhanced['enhanced_bias'] = enhanced_bias
        else:
            enhanced['enhanced_bias'] = liquidity_data.get('current_bias', 'neutral')
        
        return enhanced
    
    def _analyze_genius_volume_profile(self, closes: List[float], volumes: List[float], highs: List[float], lows: List[float]) -> Dict:
        """Genius volume profile analysis"""
        volume_data = {
            'profile_bias': 'neutral',
            'volume_strength': 0,
            'accumulation_distribution': 0,
            'money_flow_index': 50
        }
        
        if len(volumes) < 20:
            return volume_data
        
        # Volume trend analysis
        recent_volume = np.mean(volumes[-10:])
        older_volume = np.mean(volumes[-20:-10])
        volume_trend = (recent_volume - older_volume) / older_volume if older_volume > 0 else 0
        
        # Price-volume divergence
        price_change = (closes[-1] - closes[-10]) / closes[-10]
        volume_change = volume_trend
        
        # Accumulation/Distribution calculation
        ad_values = []
        for i in range(1, len(closes)):
            if highs[i] != lows[i]:
                clv = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / (highs[i] - lows[i])
                ad_values.append(clv * volumes[i])
        
        if ad_values:
            volume_data['accumulation_distribution'] = np.mean(ad_values[-10:])
        
        # Money Flow Index approximation
        if len(closes) >= 14:
            mfi = self._calculate_money_flow_index(highs[-14:], lows[-14:], closes[-14:], volumes[-14:])
            volume_data['money_flow_index'] = mfi
        
        # Determine bias
        if volume_data['accumulation_distribution'] > 0.3 and volume_data['money_flow_index'] > 60:
            volume_data['profile_bias'] = 'strong_bullish'
            volume_data['volume_strength'] = 80
        elif volume_data['accumulation_distribution'] < -0.3 and volume_data['money_flow_index'] < 40:
            volume_data['profile_bias'] = 'strong_bearish'
            volume_data['volume_strength'] = 80
        elif volume_data['accumulation_distribution'] > 0.1:
            volume_data['profile_bias'] = 'bullish'
            volume_data['volume_strength'] = 60
        elif volume_data['accumulation_distribution'] < -0.1:
            volume_data['profile_bias'] = 'bearish'
            volume_data['volume_strength'] = 60
        
        return volume_data
    
    def _determine_genius_direction(self, pro_analysis: Dict, genius_features: Dict, current_price: float) -> str:
        """GENIUS Direction Determination with advanced confluence"""
        bullish_score = 0
        bearish_score = 0
        confidence_multiplier = 1.0
        
        # Market regime (Weight: 3)
        regime_data = pro_analysis.get('market_regime', {})
        if regime_data.get('market_bias') == 'bullish':
            bullish_score += 3
        elif regime_data.get('market_bias') == 'bearish':
            bearish_score += 3
        
        # Pattern recognition (Weight: 3) - NEW
        pattern_data = genius_features.get('pattern_recognition', {})
        if pattern_data.get('bullish_count', 0) > pattern_data.get('bearish_count', 0) + 1:
            bullish_score += 3
        elif pattern_data.get('bearish_count', 0) > pattern_data.get('bullish_count', 0) + 1:
            bearish_score += 3
        
        # Multi-timeframe confluence (Weight: 3) - NEW
        confluence_data = genius_features.get('confluence', {})
        alignment = confluence_data.get('alignment_strength', 0)
        if alignment > 75:
            confidence_multiplier = 1.5
            short_bias = confluence_data.get('short_term_bias')
            if short_bias == 'uptrend':
                bullish_score += 3
            elif short_bias == 'downtrend':
                bearish_score += 3
        
        # Enhanced liquidity zones (Weight: 2)
        liquidity_data = pro_analysis.get('liquidity_zones', {})
        enhanced_bias = liquidity_data.get('enhanced_bias', 'neutral')
        if enhanced_bias in ['bullish', 'strong_bullish']:
            bullish_score += 2
        elif enhanced_bias in ['bearish', 'strong_bearish']:
            bearish_score += 2
        
        # Volume profile (Weight: 2) - NEW
        volume_data = genius_features.get('volume_profile', {})
        volume_bias = volume_data.get('profile_bias', 'neutral')
        if volume_bias in ['bullish', 'strong_bullish']:
            bullish_score += 2
        elif volume_bias in ['bearish', 'strong_bearish']:
            bearish_score += 2
        
        # Enhanced market structure (Weight: 2)
        structure_data = pro_analysis.get('market_structure', {})
        enhanced_bias = structure_data.get('enhanced_bias', 'neutral')
        if enhanced_bias == 'bullish':
            bullish_score += 2
        elif enhanced_bias == 'bearish':
            bearish_score += 2
        
        # Apply confidence multiplier
        bullish_score *= confidence_multiplier
        bearish_score *= confidence_multiplier
        
        # GENIUS Decision Logic - More stringent requirements
        min_score_threshold = 8  # Raised from 5
        score_difference_threshold = 3  # Minimum difference required
        
        if (bullish_score >= min_score_threshold and 
            bullish_score > bearish_score + score_difference_threshold):
            return 'LONG'
        elif (bearish_score >= min_score_threshold and 
              bearish_score > bullish_score + score_difference_threshold):
            return 'SHORT'
        else:
            return 'WAIT'
    
    def _calculate_genius_position_size(self, score: float, kelly_data: Dict, pro_analysis: Dict, genius_features: Dict) -> Dict[str, float]:
        """GENIUS Position Sizing with advanced risk assessment"""
        base_kelly = kelly_data.get('kelly_percentage', 0.02)
        score_multiplier = score / 100
        
        # Risk adjustment based on confluence
        confluence_data = genius_features.get('confluence', {})
        alignment_strength = confluence_data.get('alignment_strength', 0) / 100
        
        # Pattern strength adjustment
        pattern_data = genius_features.get('pattern_recognition', {})
        pattern_strength = pattern_data.get('pattern_strength', 0) / 100
        
        # Volume confirmation adjustment
        volume_data = genius_features.get('volume_profile', {})
        volume_strength = volume_data.get('volume_strength', 0) / 100
        
        # Calculate genius multiplier
        genius_multiplier = (alignment_strength + pattern_strength + volume_strength) / 3
        genius_multiplier = max(0.5, min(genius_multiplier, 1.5))  # Cap between 0.5x and 1.5x
        
        # Determine dynamic risk caps based on account size
        balance = 100.0  # Default balance reference
        if balance < 20:
            max_risk_cap = 0.03  # 3 %
        elif balance < 100:
            max_risk_cap = 0.04  # 4 %
        elif balance < 500:
            max_risk_cap = 0.03  # 3 %
        else:
            max_risk_cap = 0.025 # 2.5 %

        # Final position size calculation
        final_size = base_kelly * score_multiplier * genius_multiplier
        final_size = max(final_size, 0.003)  # Min 0.3%
        final_size = min(final_size, max_risk_cap)
        
        # Auto leverage calculation - will be calculated in position_sizing module
        # This is just a placeholder, actual leverage will be calculated during trade execution
        final_leverage = 3.0  # Default moderate leverage
        
        return {
            'risk_percentage': final_size,
            'leverage': final_leverage,
            'kelly_suggested': base_kelly,
            'genius_multiplier': genius_multiplier,
            'score_multiplier': score_multiplier,
            'confidence_boost': confidence_boost
        }
    
    def _assess_genius_confidence(self, final_score: float, pro_analysis: Dict, genius_features: Dict) -> Dict:
        """GENIUS Confidence Assessment"""
        # Base confidence from score
        base_confidence = final_score
        
        # Confluence bonus
        confluence_data = genius_features.get('confluence', {})
        confluence_bonus = confluence_data.get('alignment_strength', 0) * 0.2
        
        # Pattern recognition bonus
        pattern_data = genius_features.get('pattern_recognition', {})
        pattern_bonus = min(pattern_data.get('pattern_strength', 0) * 0.15, 15)
        
        # Volume confirmation bonus
        volume_data = genius_features.get('volume_profile', {})
        volume_bonus = min(volume_data.get('volume_strength', 0) * 0.1, 10)
        
        # Calculate genius score
        genius_score = base_confidence + confluence_bonus + pattern_bonus + volume_bonus
        genius_score = min(genius_score, 100)
        
        # Determine confidence level
        if genius_score >= 90:
            level = 'GENIUS'
        elif genius_score >= 80:
            level = 'VERY_HIGH'
        elif genius_score >= 70:
            level = 'HIGH'
        elif genius_score >= 60:
            level = 'MEDIUM'
        elif genius_score >= 45:
            level = 'LOW'
        else:
            level = 'VERY_LOW'
        
        # Calculate risk-reward ratio
        risk_reward = self._calculate_risk_reward_ratio(pro_analysis, genius_features)
        
        return {
            'level': level,
            'genius_score': genius_score,
            'base_confidence': base_confidence,
            'confluence_bonus': confluence_bonus,
            'pattern_bonus': pattern_bonus,
            'volume_bonus': volume_bonus,
            'risk_reward': risk_reward
        }
    
    # Helper methods untuk genius features
    def _calculate_trend_strength(self, prices: List[float]) -> float:
        """Calculate trend strength (0-100)"""
        if len(prices) < 10:
            return 0
        
        try:
            # Linear regression for trend
            x = np.arange(len(prices))
            slope, _ = np.polyfit(x, prices, 1)
            
            # R-squared for trend quality - ensure same array sizes
            prices_array = np.array(prices)
            predicted = slope * x + prices_array[0]  # Use prices_array[0] instead of prices[0]
            ss_res = np.sum((prices_array - predicted) ** 2)
            ss_tot = np.sum((prices_array - np.mean(prices_array)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            # Trend strength based on slope magnitude and R-squared
            trend_strength = min(abs(slope) / prices[-1] * 10000, 50) * r_squared
            return min(trend_strength, 100)
        except Exception as e:
            logger.error(f"Error calculating trend strength: {e}")
            return 0
    
    def _find_swing_points(self, data: List[float], point_type: str) -> List[Dict]:
        """Find swing highs or lows"""
        swings = []
        window = 5
        
        for i in range(window, len(data) - window):
            if point_type == 'high':
                is_swing = all(data[i] >= data[j] for j in range(i-window, i+window+1))
            else:  # low
                is_swing = all(data[i] <= data[j] for j in range(i-window, i+window+1))
            
            if is_swing:
                swings.append({'index': i, 'price': data[i]})
        
        return swings[-10:]  # Return last 10 swings
    
    def _get_trend_direction(self, prices: List[float]) -> str:
        """Determine trend direction"""
        if len(prices) < 10:
            return 'neutral'
        
        # Use moving averages for trend
        short_ma = np.mean(prices[-10:])
        long_ma = np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices)
        
        if short_ma > long_ma * 1.002:
            return 'uptrend'
        elif short_ma < long_ma * 0.998:
            return 'downtrend'
        else:
            return 'sideways'
    
    def _identify_key_levels(self, highs: List[float], lows: List[float], closes: List[float]) -> List[Dict]:
        """Identify key support/resistance levels"""
        levels = []
        
        # Find recent highs and lows
        swing_highs = self._find_swing_points(highs, 'high')
        swing_lows = self._find_swing_points(lows, 'low')
        
        # Add resistance levels
        for swing in swing_highs[-5:]:
            levels.append({'price': swing['price'], 'type': 'resistance'})
        
        # Add support levels
        for swing in swing_lows[-5:]:
            levels.append({'price': swing['price'], 'type': 'support'})
        
        return levels
    
    def _identify_high_volume_zones(self, highs: List[float], lows: List[float], volumes: List[float]) -> List[Dict]:
        """Identify high volume price zones"""
        zones = []
        
        if len(volumes) < 20:
            return zones
        
        # Find periods of high volume
        avg_volume = np.mean(volumes)
        volume_threshold = avg_volume * 1.5
        
        for i, volume in enumerate(volumes):
            if volume > volume_threshold and i < len(highs) and i < len(lows):
                price_range = (highs[i] + lows[i]) / 2
                zones.append({
                    'price': price_range,
                    'volume_ratio': volume / avg_volume,
                    'index': i
                })
        
        return zones[-10:]  # Return last 10 zones
    
    def _calculate_volume_bias(self, current_price: float, high_volume_zones: List[Dict]) -> str:
        """Calculate bias based on high volume zones"""
        if not high_volume_zones:
            return 'neutral'
        
        support_zones = [z for z in high_volume_zones if z['price'] < current_price]
        resistance_zones = [z for z in high_volume_zones if z['price'] > current_price]
        
        support_strength = sum(z['volume_ratio'] for z in support_zones)
        resistance_strength = sum(z['volume_ratio'] for z in resistance_zones)
        
        if support_strength > resistance_strength * 1.2:
            return 'bullish'
        elif resistance_strength > support_strength * 1.2:
            return 'bearish'
        else:
            return 'neutral'
    
    def _combine_bias_signals(self, original_bias: str, volume_bias: str) -> str:
        """Combine multiple bias signals"""
        bias_strength = {
            'strong_bullish': 2,
            'bullish': 1,
            'neutral': 0,
            'bearish': -1,
            'strong_bearish': -2
        }
        
        original_score = bias_strength.get(original_bias, 0)
        volume_score = bias_strength.get(volume_bias, 0)
        
        combined_score = original_score + volume_score
        
        if combined_score >= 3:
            return 'strong_bullish'
        elif combined_score >= 1:
            return 'bullish'
        elif combined_score <= -3:
            return 'strong_bearish'
        elif combined_score <= -1:
            return 'bearish'
        else:
            return 'neutral'
    
    def _calculate_money_flow_index(self, highs: List[float], lows: List[float], closes: List[float], volumes: List[float]) -> float:
        """Calculate Money Flow Index"""
        if len(highs) < 2:
            return 50
        
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
        money_flows = []
        
        for i in range(1, len(typical_prices)):
            if typical_prices[i] > typical_prices[i-1]:
                money_flows.append(volumes[i])  # Positive money flow
            elif typical_prices[i] < typical_prices[i-1]:
                money_flows.append(-volumes[i])  # Negative money flow
            else:
                money_flows.append(0)
        
        positive_flow = sum(mf for mf in money_flows if mf > 0)
        negative_flow = abs(sum(mf for mf in money_flows if mf < 0))
        
        if negative_flow == 0:
            return 100
        
        money_ratio = positive_flow / negative_flow
        mfi = 100 - (100 / (1 + money_ratio))
        
        return max(0, min(100, mfi))
    
    def _enhance_session_analysis(self, session_data: Dict, closes: List[float], volumes: List[float]) -> Dict:
        """Enhanced session analysis"""
        enhanced = session_data.copy()
        
        # Add volume-based session strength
        if len(volumes) >= 10:
            current_volume = np.mean(volumes[-10:])
            session_avg_volume = np.mean(volumes[-50:]) if len(volumes) >= 50 else current_volume
            
            volume_multiplier = min(current_volume / session_avg_volume, 2.0) if session_avg_volume > 0 else 1.0
            enhanced_multiplier = session_data['session_adjustment'] * volume_multiplier
            enhanced['enhanced_multiplier'] = min(enhanced_multiplier, 1.5)
        else:
            enhanced['enhanced_multiplier'] = session_data['session_adjustment']
        
        return enhanced
    
    def _score_pattern_recognition(self, pattern_data: Dict) -> float:
        """Score pattern recognition strength"""
        pattern_strength = pattern_data.get('pattern_strength', 0)
        return min(pattern_strength * 0.2, 20)  # Max 20 points
    
    def _score_confluence_analysis(self, confluence_data: Dict) -> float:
        """Score confluence analysis"""
        alignment_strength = confluence_data.get('alignment_strength', 0)
        return min(alignment_strength * 0.15, 15)  # Max 15 points
    
    def _score_enhanced_structure(self, structure_data: Dict) -> float:
        """Score enhanced structure analysis"""
        bias = structure_data.get('enhanced_bias', 'neutral')
        if bias in ['strong_bullish', 'strong_bearish']:
            return 10
        elif bias in ['bullish', 'bearish']:
            return 7
        else:
            return 3
    
    def _score_volume_genius(self, volume_data: Dict) -> float:
        """Score genius volume analysis"""
        volume_strength = volume_data.get('volume_strength', 0)
        return min(volume_strength * 0.1, 10)  # Max 10 points
    
    def _enhance_structure_analysis(self, structure_data: Dict, highs: List[float], lows: List[float]) -> Dict:
        """Enhanced structure analysis"""
        enhanced = structure_data.copy()
        
        # Add momentum-based enhancement
        if len(highs) >= 20 and len(lows) >= 20:
            recent_momentum = self._calculate_momentum_bias(highs[-20:], lows[-20:])
            original_bias = structure_data.get('bias', 'neutral')
            enhanced_bias = self._combine_bias_signals(original_bias, recent_momentum)
            enhanced['enhanced_bias'] = enhanced_bias
        else:
            enhanced['enhanced_bias'] = structure_data.get('bias', 'neutral')
        
        return enhanced
    
    def _score_enhanced_liquidity(self, liquidity_data: Dict, current_price: float) -> float:
        """Score enhanced liquidity analysis"""
        base_score = 10
        
        enhanced_bias = liquidity_data.get('enhanced_bias', 'neutral')
        if enhanced_bias in ['strong_bullish', 'strong_bearish']:
            base_score += 10
        elif enhanced_bias in ['bullish', 'bearish']:
            base_score += 5
        
        distance_to_key = liquidity_data.get('distance_to_key', 999)
        if distance_to_key < 0.5:
            base_score += 5
        elif distance_to_key < 1.0:
            base_score += 3
        
        return min(base_score, 20)
    
    def _calculate_momentum_bias(self, highs: List[float], lows: List[float]) -> str:
        """Calculate momentum bias from price action"""
        if len(highs) < 10 or len(lows) < 10:
            return 'neutral'
        
        # Rate of change analysis
        high_roc = (highs[-1] - highs[-10]) / highs[-10]
        low_roc = (lows[-1] - lows[-10]) / lows[-10]
        
        if high_roc > 0.01 and low_roc > 0.005:
            return 'bullish'
        elif high_roc < -0.01 and low_roc < -0.005:
            return 'bearish'
        else:
            return 'neutral'
    
    def _calculate_risk_reward_ratio(self, pro_analysis: Dict, genius_features: Dict) -> float:
        """Calculate potential risk-reward ratio"""
        # This would typically require target and stop levels
        # For now, we'll estimate based on confluence strength
        
        confluence_data = genius_features.get('confluence', {})
        alignment_strength = confluence_data.get('alignment_strength', 0)
        
        pattern_data = genius_features.get('pattern_recognition', {})
        pattern_strength = pattern_data.get('pattern_strength', 0)
        
        # Higher confluence and pattern strength = better risk-reward potential
        base_rr = 1.0
        confluence_bonus = alignment_strength / 100 * 0.5
        pattern_bonus = pattern_strength / 100 * 0.3
        
        estimated_rr = base_rr + confluence_bonus + pattern_bonus
        return min(estimated_rr, 2.5)  # Cap at 2.5:1
    
    def add_trade_to_history(self, trade_data: Dict):
        """Add trade to history untuk Kelly calculation"""
        self.trades_history.append(trade_data)
        if len(self.trades_history) > 100:  # Increased history for better Kelly calculation
            self.trades_history = self.trades_history[-100:]

class SmartExit:
    """SUPER BRILLIANT PRO TRADER Exit - Genius Level Risk Management"""
    
    def __init__(self, config):
        self.config = config
        self.session_analyzer = TradingSessionAnalyzer()
        self.structure_analyzer = MarketStructureAnalyzer()
        
        # GENIUS EXIT FEATURES
        self.profit_target_levels = [0.3, 0.6, 1.0, 1.5, 2.5]  # Multi-level TP
        self.trailing_stop_levels = {}  # Dynamic trailing stops
        self.exit_confidence_threshold = 75  # Minimum confidence untuk aggressive exits
    
    def should_exit(self, position_data, current_price, klines_data, entry_analysis=None):
        """SUPER BRILLIANT Exit Analysis - Genius Level Risk Management"""
        try:
            entry_price = float(position_data.get('entryPrice', 0))
            side = position_data.get('positionSide', 'LONG')
            position_size = float(position_data.get('positionAmt', 0))
            
            if entry_price == 0:
                return {"action": "hold", "reason": "Invalid entry price"}
            
            # Calculate profit percentage
            if side == 'LONG':
                profit_pct = (current_price - entry_price) / entry_price
            else:
                profit_pct = (entry_price - current_price) / entry_price
            
            # Extract comprehensive market data
            if klines_data and len(klines_data) >= 50:
                highs = [float(k[2]) for k in klines_data]
                lows = [float(k[3]) for k in klines_data]
                opens = [float(k[1]) for k in klines_data]
                closes = [float(k[4]) for k in klines_data]
                volumes = [float(k[5]) for k in klines_data]
            else:
                closes = [current_price]
                highs = lows = opens = volumes = [current_price]
            
            # 1. CRITICAL EMERGENCY STOPS (Highest Priority)
            emergency_exit = self._check_emergency_exits(profit_pct, closes, volumes, entry_analysis)
            if emergency_exit["should_exit"]:
                return emergency_exit
            
            # 2. GENIUS PATTERN-BASED EXITS - NEW SUPER FEATURE
            pattern_exit = self._check_genius_pattern_exits(highs, lows, opens, closes, volumes, side, profit_pct)
            if pattern_exit["should_exit"]:
                return pattern_exit
            
            # 3. DYNAMIC VOLATILITY-BASED STOPS - Enhanced
            volatility_exit = self._check_enhanced_volatility_stops(closes, highs, lows, entry_price, side, profit_pct, entry_analysis)
            if volatility_exit["should_exit"]:
                return volatility_exit
            
            # 4. MULTI-LEVEL SMART PROFIT TAKING - Genius Feature
            profit_exit = self._check_genius_profit_taking(profit_pct, closes, volumes, side, position_size, entry_analysis)
            if profit_exit["should_exit"]:
                return profit_exit
            
            # 5. MARKET STRUCTURE BREAK EXITS - Enhanced
            structure_exit = self._check_enhanced_structure_exits(closes, highs, lows, side, profit_pct, entry_analysis)
            if structure_exit["should_exit"]:
                return structure_exit
            
            # 6. SESSION & TIME-BASED EXITS - Enhanced
            session_exit = self._check_enhanced_session_exits(profit_pct, closes, volumes, entry_analysis)
            if session_exit["should_exit"]:
                return session_exit
            
            # 7. MOMENTUM REVERSAL EXITS - Genius Feature
            momentum_exit = self._check_genius_momentum_exits(closes, volumes, side, profit_pct, entry_analysis)
            if momentum_exit["should_exit"]:
                return momentum_exit
            
            # 8. CORRELATION & MARKET SENTIMENT EXITS - Advanced Feature
            sentiment_exit = self._check_market_sentiment_exits(closes, volumes, side, profit_pct)
            if sentiment_exit["should_exit"]:
                return sentiment_exit
            
            # 9. TRAILING STOP MANAGEMENT - Genius Dynamic System
            trailing_exit = self._manage_genius_trailing_stops(current_price, entry_price, side, profit_pct, closes)
            if trailing_exit["should_exit"]:
                return trailing_exit
            
            # If no exit signal, return enhanced hold with confidence score
            hold_confidence = self._calculate_hold_confidence(profit_pct, closes, volumes, entry_analysis)
            
            return {
                "action": "hold",
                "reason": f"🟢 Hold Strong - P&L: {profit_pct:.2%} | Confidence: {hold_confidence:.1f}%",
                "urgency": "NONE",
                "hold_confidence": hold_confidence,
                "suggested_action": self._get_hold_suggestion(profit_pct, hold_confidence)
            }
            
        except Exception as e:
            logger.error(f"Error in genius exit analysis: {e}")
            return {"action": "hold", "reason": "Exit analysis error", "urgency": "NONE"}
    
    def _check_emergency_exits(self, profit_pct: float, closes: List[float], volumes: List[float], entry_analysis: Dict = None) -> Dict:
        """Critical emergency exit conditions"""
        
        # 1. Hard Stop Loss (3% absolute limit)
        if profit_pct <= -0.03:
            return {
                "action": "close",
                "reason": f"🚨 EMERGENCY STOP: {profit_pct:.2%} - Capital Protection!",
                "urgency": "CRITICAL"
            }
        
        # 2. Flash Crash Detection
        if len(closes) >= 5:
            recent_drop = (closes[-1] - max(closes[-5:])) / max(closes[-5:])
            if recent_drop <= -0.02:  # 2% drop in 5 candles
                return {
                    "action": "close",
                    "reason": f"🚨 FLASH CRASH DETECTED: {recent_drop:.2%}",
                    "urgency": "CRITICAL"
                }
        
        # 3. Volume Spike + Price Drop (Panic selling)
        if len(volumes) >= 10:
            avg_volume = np.mean(volumes[-10:])
            current_volume = volumes[-1]
            volume_spike = current_volume / avg_volume if avg_volume > 0 else 1
            
            if volume_spike > 3.0 and profit_pct < -0.01:
                return {
                    "action": "close",
                    "reason": f"🚨 PANIC SELLING: Vol {volume_spike:.1f}x + Loss {profit_pct:.2%}",
                    "urgency": "CRITICAL"
                }
        
        # 4. Entry Confidence-Based Emergency
        if entry_analysis:
            entry_confidence = entry_analysis.get('confidence', 0)
            if entry_confidence < 30 and profit_pct <= -0.015:
                return {
                    "action": "close",
                    "reason": f"🚨 LOW CONFIDENCE EXIT: Entry {entry_confidence:.1f}% + Loss {profit_pct:.2%}",
                    "urgency": "HIGH"
                }
        
        return {"should_exit": False, "reason": "No emergency conditions"}
    
    def _check_genius_pattern_exits(self, highs: List[float], lows: List[float], opens: List[float], closes: List[float], volumes: List[float], side: str, profit_pct: float) -> Dict:
        """GENIUS Pattern-Based Exit Recognition"""
        
        if len(closes) < 10:
            return {"should_exit": False, "reason": "Insufficient data for pattern analysis"}
        
        # 1. Reversal Candlestick Patterns
        reversal_patterns = self._detect_exit_candlestick_patterns(highs[-10:], lows[-10:], opens[-10:], closes[-10:])
        
        if reversal_patterns and profit_pct > 0.003:  # Only exit with profit
            pattern_strength = len(reversal_patterns)
            if pattern_strength >= 2:  # Multiple reversal signals
                return {
                    "action": "close",
                    "reason": f"🔄 REVERSAL PATTERNS: {pattern_strength} signals + Profit {profit_pct:.2%}",
                    "urgency": "MEDIUM"
                }
        
        # 2. Exhaustion Patterns
        exhaustion_signal = self._detect_exhaustion_patterns(highs, lows, closes, volumes, side)
        if exhaustion_signal["is_exhausted"] and profit_pct > 0.005:
            return {
                "action": "close",
                "reason": f"😴 EXHAUSTION: {exhaustion_signal['pattern']} + Profit {profit_pct:.2%}",
                "urgency": "MEDIUM"
            }
        
        # 3. Double Top/Bottom at Profit
        double_pattern = self._detect_double_top_bottom_exit(highs, lows, side, profit_pct)
        if double_pattern["should_exit"]:
            return {
                "action": "close",
                "reason": f"🎯 {double_pattern['pattern'].upper()}: Perfect Exit + Profit {profit_pct:.2%}",
                "urgency": "LOW"
            }
        
        # 4. Divergence Patterns
        divergence = self._detect_genius_divergence(closes, volumes)
        if divergence["has_divergence"] and profit_pct > 0.008:
            return {
                "action": "close",
                "reason": f"📊 DIVERGENCE: {divergence['type']} + Profit {profit_pct:.2%}",
                "urgency": "MEDIUM"
            }
        
        return {"should_exit": False, "reason": "No exit patterns detected"}
    
    def _check_enhanced_volatility_stops(self, closes: List[float], highs: List[float], lows: List[float], entry_price: float, side: str, profit_pct: float, entry_analysis: Dict = None) -> Dict:
        """Enhanced volatility-based dynamic stops"""
        
        if len(closes) < 20:
            base_stop = -0.02
        else:
            # Advanced ATR calculation
            true_ranges = []
            for i in range(1, len(closes)):
                high_low = highs[i] - lows[i]
                high_close = abs(highs[i] - closes[i-1])
                low_close = abs(lows[i] - closes[i-1])
                true_range = max(high_low, high_close, low_close)
                true_ranges.append(true_range)
            
            atr = np.mean(true_ranges[-14:]) if len(true_ranges) >= 14 else np.mean(true_ranges)
            volatility_pct = (atr / closes[-1]) * 100
            
            # Genius volatility-based stop calculation
            if volatility_pct > 3.0:
                base_stop = -0.025  # Wider stop for high volatility
            elif volatility_pct > 2.0:
                base_stop = -0.02
            elif volatility_pct < 0.5:
                base_stop = -0.015  # Tighter stop for low volatility
            else:
                base_stop = -0.018
            
            # Market regime adjustment
            market_trend = self._get_market_trend_strength(closes[-50:] if len(closes) >= 50 else closes)
            if market_trend == 'strong_trend':
                base_stop *= 1.2  # Wider stops in trending markets
            elif market_trend == 'choppy':
                base_stop *= 0.8  # Tighter stops in choppy markets
        
        # Entry confidence adjustment
        if entry_analysis:
            confidence = entry_analysis.get('confidence', 50)
            confidence_multiplier = 0.8 + (confidence / 100) * 0.4  # 0.8x to 1.2x
            base_stop *= confidence_multiplier
        
        # Profit protection adjustment
        if profit_pct > 0.01:  # If in 1%+ profit, allow wider stop
            base_stop *= 1.3
        
        final_stop = max(base_stop, -0.03)  # Never more than 3%
        
        if profit_pct <= final_stop:
            return {
                "action": "close",
                "reason": f"📉 SMART STOP: {profit_pct:.2%} (ATR-based: {final_stop:.2%})",
                "urgency": "HIGH"
            }
        
        return {"should_exit": False, "reason": "Volatility stop not triggered"}
    
    def _check_genius_profit_taking(self, profit_pct: float, closes: List[float], volumes: List[float], side: str, position_size: float, entry_analysis: Dict = None) -> Dict:
        """Multi-level genius profit taking system"""
        
        # Get entry confidence for profit target adjustment
        entry_confidence = entry_analysis.get('confidence', 50) if entry_analysis else 50
        confidence_multiplier = 0.7 + (entry_confidence / 100) * 0.6  # 0.7x to 1.3x
        
        # Adaptive profit targets based on market conditions
        market_volatility = self._calculate_market_volatility(closes)
        volatility_multiplier = 0.8 + min(market_volatility * 2, 0.4)  # 0.8x to 1.2x
        
        # Dynamic profit levels
        profit_levels = [
            0.003 * confidence_multiplier * volatility_multiplier,  # Quick scalp
            0.006 * confidence_multiplier * volatility_multiplier,  # Conservative
            0.012 * confidence_multiplier * volatility_multiplier,  # Standard
            0.020 * confidence_multiplier * volatility_multiplier,  # Aggressive
            0.035 * confidence_multiplier * volatility_multiplier   # Moon shot
        ]
        
        # Partial profit taking logic
        for i, level in enumerate(profit_levels):
            if profit_pct >= level:
                # Check trend continuation for higher levels
                if i >= 2:  # For levels 3+ check trend strength
                    trend_strength = self._calculate_trend_continuation_probability(closes, volumes, side)
                    if trend_strength > 70:  # Strong trend continues
                        continue  # Don't exit yet
                
                # Special conditions for each level
                level_names = ["Quick Scalp", "Conservative", "Standard", "Aggressive", "Moon Shot"]
                level_confidence = [95, 85, 75, 65, 50][i]
                
                # Risk-reward optimization
                if i == 0:  # Quick scalp - always take
                    return {
                        "action": "close",
                        "reason": f"⚡ {level_names[i]}: {profit_pct:.2%} (Risk-Free)",
                        "urgency": "LOW"
                    }
                
                elif i == 1:  # Conservative - take if market shows weakness
                    if self._detect_market_weakness(closes, volumes):
                        return {
                            "action": "close",
                            "reason": f"🛡️ {level_names[i]}: {profit_pct:.2%} (Weakness Detected)",
                            "urgency": "LOW"
                        }
                
                elif i >= 2:  # Standard+ levels - use advanced logic
                    market_strength = self._assess_market_continuation_strength(closes, volumes, side)
                    if market_strength < level_confidence:
                        return {
                            "action": "close",
                            "reason": f"🎯 {level_names[i]}: {profit_pct:.2%} (Market Strength: {market_strength:.1f}%)",
                            "urgency": "LOW"
                        }
        
        return {"should_exit": False, "reason": "Profit targets not met or trend continuing"}
    
    def _check_enhanced_structure_exits(self, closes: List[float], highs: List[float], lows: List[float], side: str, profit_pct: float, entry_analysis: Dict = None) -> Dict:
        """Enhanced market structure break detection"""
        
        if len(closes) < 30:
            return {"should_exit": False, "reason": "Insufficient data for structure analysis"}
        
        # Advanced structure analysis
        structure_data = self.structure_analyzer.analyze_market_structure(closes)
        structure = structure_data.get('structure', '')
        
        # Key level breaks
        key_levels = self._identify_critical_levels(highs, lows, closes)
        current_price = closes[-1]
        
        # Structure break with confirmation
        structure_broken = False
        break_reason = ""
        
        if side == 'LONG':
            # Look for bearish structure breaks
            if structure in ['lower_highs_lower_lows']:
                structure_broken = True
                break_reason = "Bearish structure confirmed"
            
            # Support level breaks
            for level in key_levels:
                if level['type'] == 'support' and current_price < level['price'] * 0.998:
                    if profit_pct > 0.002:  # Only exit with some profit
                        structure_broken = True
                        break_reason = f"Support break at {level['price']:.6f}"
                        break
        
        else:  # SHORT
            # Look for bullish structure breaks
            if structure in ['higher_highs_higher_lows']:
                structure_broken = True
                break_reason = "Bullish structure confirmed"
            
            # Resistance level breaks
            for level in key_levels:
                if level['type'] == 'resistance' and current_price > level['price'] * 1.002:
                    if profit_pct > 0.002:  # Only exit with some profit
                        structure_broken = True
                        break_reason = f"Resistance break at {level['price']:.6f}"
                        break
        
        if structure_broken:
            # Volume confirmation
            volume_confirmation = self._check_volume_confirmation(closes, volumes if len(volumes) > 0 else [1])
            urgency = "MEDIUM" if volume_confirmation else "LOW"
            
            return {
                "action": "close",
                "reason": f"🏗️ STRUCTURE BREAK: {break_reason} + Profit {profit_pct:.2%}",
                "urgency": urgency
            }
        
        return {"should_exit": False, "reason": "Market structure intact"}
    
    def _check_enhanced_session_exits(self, profit_pct: float, closes: List[float], volumes: List[float], entry_analysis: Dict = None) -> Dict:
        """Enhanced session and time-based exits"""
        
        session_data = self.session_analyzer.get_session_adjustment_factor()
        weekend_check = self.session_analyzer.is_weekend_approaching()
        
        # Enhanced session logic
        current_session = session_data.get('session', 'unknown')
        session_strength = session_data.get('session_adjustment', 1.0)
        
        # Weekend approach with profit protection
        if weekend_check.get('weekend_approaching'):
            if profit_pct > 0.001:  # Any profit
                return {
                    "action": "close",
                    "reason": f"📅 WEEKEND APPROACH: Secure {profit_pct:.2%} profit",
                    "urgency": "MEDIUM"
                }
            elif profit_pct < -0.01:  # Significant loss
                return {
                    "action": "close",
                    "reason": f"📅 WEEKEND RISK: Cut loss {profit_pct:.2%}",
                    "urgency": "HIGH"
                }
        
        # Low activity session exits
        if current_session in ['off_session', 'asian_quiet']:
            if 0.002 < profit_pct < 0.008:  # Small profit in quiet session
                return {
                    "action": "close",
                    "reason": f"😴 QUIET SESSION: Lock {profit_pct:.2%} profit",
                    "urgency": "LOW"
                }
        
        # High volatility session management
        if current_session == 'london_open' and len(volumes) >= 10:
            volume_spike = volumes[-1] / np.mean(volumes[-10:]) if np.mean(volumes[-10:]) > 0 else 1
            if volume_spike > 2.0 and profit_pct > 0.005:
                return {
                    "action": "close",
                    "reason": f"🌍 LONDON VOLATILITY: {profit_pct:.2%} profit secured",
                    "urgency": "MEDIUM"
                }
        
        return {"should_exit": False, "reason": "Session conditions favorable"}
    
    def _check_genius_momentum_exits(self, closes: List[float], volumes: List[float], side: str, profit_pct: float, entry_analysis: Dict = None) -> Dict:
        """Genius momentum reversal detection"""
        
        if len(closes) < 20:
            return {"should_exit": False, "reason": "Insufficient data for momentum analysis"}
        
        # Advanced RSI with momentum divergence
        rsi = SmartIndicators.rsi(closes)
        rsi_prev = SmartIndicators.rsi(closes[:-1]) if len(closes) > 14 else rsi
        
        # Price momentum
        price_momentum = (closes[-1] - closes[-10]) / closes[-10] if len(closes) >= 10 else 0
        
        # Volume momentum
        volume_momentum = 0
        if len(volumes) >= 10:
            recent_vol = np.mean(volumes[-5:])
            older_vol = np.mean(volumes[-10:-5])
            volume_momentum = (recent_vol - older_vol) / older_vol if older_vol > 0 else 0
        
        # Momentum exhaustion detection
        momentum_exhausted = False
        exhaustion_reason = ""
        
        if side == 'LONG':
            # Overbought with momentum divergence
            if rsi > 75 and rsi < rsi_prev and profit_pct > 0.005:
                momentum_exhausted = True
                exhaustion_reason = f"RSI divergence: {rsi:.1f}"
            
            # Price up but volume declining
            elif price_momentum > 0.01 and volume_momentum < -0.2 and profit_pct > 0.008:
                momentum_exhausted = True
                exhaustion_reason = "Volume divergence"
        
        else:  # SHORT
            # Oversold with momentum divergence
            if rsi < 25 and rsi > rsi_prev and profit_pct > 0.005:
                momentum_exhausted = True
                exhaustion_reason = f"RSI divergence: {rsi:.1f}"
            
            # Price down but volume declining
            elif price_momentum < -0.01 and volume_momentum < -0.2 and profit_pct > 0.008:
                momentum_exhausted = True
                exhaustion_reason = "Volume divergence"
        
        if momentum_exhausted:
            return {
                "action": "close",
                "reason": f"📊 MOMENTUM EXHAUSTION: {exhaustion_reason} + Profit {profit_pct:.2%}",
                "urgency": "MEDIUM"
            }
        
        return {"should_exit": False, "reason": "Momentum remains strong"}
    
    def _check_market_sentiment_exits(self, closes: List[float], volumes: List[float], side: str, profit_pct: float) -> Dict:
        """Advanced market sentiment and correlation analysis"""
        
        if len(closes) < 30:
            return {"should_exit": False, "reason": "Insufficient data for sentiment analysis"}
        
        # Market fear/greed indicator (simplified)
        market_sentiment = self._calculate_market_sentiment(closes, volumes)
        
        # Exit in extreme sentiment with profit
        if market_sentiment == 'extreme_fear' and side == 'SHORT' and profit_pct > 0.01:
            return {
                "action": "close",
                "reason": f"😱 EXTREME FEAR: Perfect SHORT exit + {profit_pct:.2%}",
                "urgency": "LOW"
            }
        
        elif market_sentiment == 'extreme_greed' and side == 'LONG' and profit_pct > 0.01:
            return {
                "action": "close",
                "reason": f"🤑 EXTREME GREED: Perfect LONG exit + {profit_pct:.2%}",
                "urgency": "LOW"
            }
        
        # Volatility clustering exit
        volatility_cluster = self._detect_volatility_clustering(closes)
        if volatility_cluster["is_clustering"] and profit_pct > 0.005:
            return {
                "action": "close",
                "reason": f"📈 VOLATILITY CLUSTER: Secure {profit_pct:.2%} before chaos",
                "urgency": "MEDIUM"
            }
        
        return {"should_exit": False, "reason": "Market sentiment neutral"}
    
    def _manage_genius_trailing_stops(self, current_price: float, entry_price: float, side: str, profit_pct: float, closes: List[float]) -> Dict:
        """Dynamic genius trailing stop management"""
        
        if profit_pct <= 0:
            return {"should_exit": False, "reason": "No profit to trail"}
        
        # Calculate dynamic trailing distance based on volatility
        if len(closes) >= 20:
            volatility = np.std(closes[-20:]) / np.mean(closes[-20:])
            trailing_distance = max(0.005, min(0.02, volatility * 2))  # 0.5% to 2%
        else:
            trailing_distance = 0.01  # 1% default
        
        # Profit-based trailing adjustment
        if profit_pct > 0.02:  # 2%+ profit
            trailing_distance *= 1.5  # Wider trailing
        elif profit_pct > 0.05:  # 5%+ profit
            trailing_distance *= 2.0  # Much wider trailing
        
        # Get or initialize trailing stop
        position_key = f"{side}_{entry_price}"
        
        if position_key not in self.trailing_stop_levels:
            # Initialize trailing stop at current profit level
            initial_trail = current_price * (1 - trailing_distance) if side == 'LONG' else current_price * (1 + trailing_distance)
            self.trailing_stop_levels[position_key] = initial_trail
        
        current_trail = self.trailing_stop_levels[position_key]
        
        # Update trailing stop
        if side == 'LONG':
            new_trail = current_price * (1 - trailing_distance)
            if new_trail > current_trail:
                self.trailing_stop_levels[position_key] = new_trail
                current_trail = new_trail
            
            # Check if price hit trailing stop
            if current_price <= current_trail:
                del self.trailing_stop_levels[position_key]  # Clean up
                return {
                    "action": "close",
                    "reason": f"📈 TRAILING STOP: {profit_pct:.2%} profit secured",
                    "urgency": "LOW"
                }
        
        else:  # SHORT
            new_trail = current_price * (1 + trailing_distance)
            if new_trail < current_trail:
                self.trailing_stop_levels[position_key] = new_trail
                current_trail = new_trail
            
            # Check if price hit trailing stop
            if current_price >= current_trail:
                del self.trailing_stop_levels[position_key]  # Clean up
                return {
                    "action": "close",
                    "reason": f"📉 TRAILING STOP: {profit_pct:.2%} profit secured",
                    "urgency": "LOW"
                }
        
        return {"should_exit": False, "reason": f"Trailing at {trailing_distance:.1%}"}
    
    # Helper methods untuk genius exit features
    def _detect_exit_candlestick_patterns(self, highs: List[float], lows: List[float], opens: List[float], closes: List[float]) -> List[str]:
        """Detect reversal candlestick patterns for exits"""
        patterns = []
        
        if len(closes) < 3:
            return patterns
        
        for i in range(2, len(closes)):
            # Shooting star
            body_size = abs(closes[i] - opens[i])
            candle_range = highs[i] - lows[i]
            
            if candle_range > 0.0001:  # Prevent division by zero
                upper_shadow = (highs[i] - max(opens[i], closes[i])) / candle_range
                lower_shadow = (min(opens[i], closes[i]) - lows[i]) / candle_range
                
                if upper_shadow > 0.6 and lower_shadow < 0.2:
                    patterns.append("shooting_star")
                
                if lower_shadow > 0.6 and upper_shadow < 0.2:
                    patterns.append("hammer")
            
            # Doji
            if candle_range > 0.0001 and body_size / candle_range < 0.15:  # Prevent division by zero
                patterns.append("doji")
        
        return patterns
    
    def _detect_exhaustion_patterns(self, highs: List[float], lows: List[float], closes: List[float], volumes: List[float], side: str) -> Dict:
        """Detect momentum exhaustion patterns"""
        
        if len(closes) < 10:
            return {"is_exhausted": False, "pattern": "insufficient_data"}
        
        # Volume exhaustion
        if len(volumes) >= 10:
            recent_volume = np.mean(volumes[-3:])
            older_volume = np.mean(volumes[-10:-3])
            volume_ratio = recent_volume / older_volume if older_volume > 0 else 1
            
            # Price extension with volume decline
            price_change = (closes[-1] - closes[-5]) / closes[-5]
            
            if side == 'LONG':
                if price_change > 0.01 and volume_ratio < 0.7:
                    return {"is_exhausted": True, "pattern": "volume_exhaustion_up"}
            else:  # SHORT
                if price_change < -0.01 and volume_ratio < 0.7:
                    return {"is_exhausted": True, "pattern": "volume_exhaustion_down"}
        
        # Price exhaustion (parabolic move)
        recent_moves = [abs((closes[i] - closes[i-1]) / closes[i-1]) for i in range(1, len(closes))]
        if len(recent_moves) >= 5:
            recent_avg_move = np.mean(recent_moves[-5:])
            if recent_avg_move > 0.015:  # 1.5% average moves
                return {"is_exhausted": True, "pattern": "parabolic_exhaustion"}
        
        return {"is_exhausted": False, "pattern": "none"}
    
    def _detect_double_top_bottom_exit(self, highs: List[float], lows: List[float], side: str, profit_pct: float) -> Dict:
        """Detect double top/bottom patterns for exits"""
        
        if len(highs) < 20 or profit_pct < 0.005:
            return {"should_exit": False, "pattern": "insufficient_setup"}
        
        if side == 'LONG':
            # Look for double top
            recent_highs = highs[-20:]
            max_high = max(recent_highs)
            current_high = highs[-1]
            
            # Find previous high similar to current
            for i in range(len(recent_highs) - 5, 0, -1):
                if abs(recent_highs[i] - current_high) / current_high < 0.01:  # Within 1%
                    return {"should_exit": True, "pattern": "double_top"}
        
        else:  # SHORT
            # Look for double bottom
            recent_lows = lows[-20:]
            min_low = min(recent_lows)
            current_low = lows[-1]
            
            # Find previous low similar to current
            for i in range(len(recent_lows) - 5, 0, -1):
                if abs(recent_lows[i] - current_low) / current_low < 0.01:  # Within 1%
                    return {"should_exit": True, "pattern": "double_bottom"}
        
        return {"should_exit": False, "pattern": "none"}
    
    def _detect_genius_divergence(self, closes: List[float], volumes: List[float]) -> Dict:
        """Detect price-volume divergence"""
        
        if len(closes) < 20 or len(volumes) < 20:
            return {"has_divergence": False, "type": "insufficient_data"}
        
        # Price trend (last 10 vs previous 10)
        recent_price = np.mean(closes[-10:])
        older_price = np.mean(closes[-20:-10])
        price_trend = (recent_price - older_price) / older_price
        
        # Volume trend
        recent_volume = np.mean(volumes[-10:])
        older_volume = np.mean(volumes[-20:-10])
        volume_trend = (recent_volume - older_volume) / older_volume if older_volume > 0 else 0
        
        # Detect divergence
        if price_trend > 0.01 and volume_trend < -0.1:
            return {"has_divergence": True, "type": "bearish_divergence"}
        elif price_trend < -0.01 and volume_trend < -0.1:
            return {"has_divergence": True, "type": "bullish_divergence"}
        
        return {"has_divergence": False, "type": "none"}
    
    def _get_market_trend_strength(self, closes: List[float]) -> str:
        """Assess market trend strength"""
        if len(closes) < 20:
            return 'unknown'
        
        try:
            # Linear regression slope
            x = np.arange(len(closes))
            slope, _ = np.polyfit(x, closes, 1)
            
            # Trend strength
            slope_pct = (slope * len(closes)) / closes[0]
            
            if abs(slope_pct) > 0.02:
                return 'strong_trend'
            elif abs(slope_pct) < 0.005:
                return 'choppy'
            else:
                return 'moderate_trend'
        except Exception as e:
            logger.error(f"Error calculating market trend strength: {e}")
            return 'unknown'
    
    def _calculate_market_volatility(self, closes: List[float]) -> float:
        """Calculate market volatility"""
        if len(closes) < 20:
            return 0.02  # Default 2%
        
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        return np.std(returns)
    
    def _calculate_trend_continuation_probability(self, closes: List[float], volumes: List[float], side: str) -> float:
        """Calculate probability of trend continuation"""
        if len(closes) < 20:
            return 50.0
        
        # Trend consistency
        recent_trend = (closes[-1] - closes[-10]) / closes[-10]
        older_trend = (closes[-10] - closes[-20]) / closes[-20]
        
        trend_consistency = 1 - abs(recent_trend - older_trend) / max(abs(recent_trend), abs(older_trend), 0.001)
        
        # Volume support
        volume_support = 50.0
        if len(volumes) >= 20:
            recent_vol = np.mean(volumes[-10:])
            older_vol = np.mean(volumes[-20:-10])
            if recent_vol > older_vol:
                volume_support = 70.0
        
        return min(trend_consistency * 50 + volume_support, 100.0)
    
    def _detect_market_weakness(self, closes: List[float], volumes: List[float]) -> bool:
        """Detect early signs of market weakness"""
        if len(closes) < 10:
            return False
        
        # Price deceleration
        recent_momentum = (closes[-1] - closes[-5]) / closes[-5]
        older_momentum = (closes[-5] - closes[-10]) / closes[-10] if len(closes) >= 10 else recent_momentum
        
        momentum_declining = recent_momentum < older_momentum * 0.8
        
        # Volume confirmation
        volume_declining = False
        if len(volumes) >= 10:
            recent_vol = np.mean(volumes[-5:])
            older_vol = np.mean(volumes[-10:-5])
            volume_declining = recent_vol < older_vol * 0.9
        
        return momentum_declining and volume_declining
    
    def _assess_market_continuation_strength(self, closes: List[float], volumes: List[float], side: str) -> float:
        """Assess likelihood of market continuation"""
        if len(closes) < 20:
            return 50.0
        
        strength_score = 50.0
        
        # Trend momentum
        momentum = (closes[-1] - closes[-10]) / closes[-10]
        if side == 'LONG' and momentum > 0.01:
            strength_score += 20
        elif side == 'SHORT' and momentum < -0.01:
            strength_score += 20
        
        # Volume confirmation
        if len(volumes) >= 20:
            vol_trend = np.mean(volumes[-10:]) / np.mean(volumes[-20:-10])
            if vol_trend > 1.1:
                strength_score += 15
        
        # Price action quality
        price_consistency = self._calculate_price_action_quality(closes[-20:])
        strength_score += price_consistency * 15
        
        return min(strength_score, 100.0)
    
    def _identify_critical_levels(self, highs: List[float], lows: List[float], closes: List[float]) -> List[Dict]:
        """Identify critical support/resistance levels"""
        levels = []
        
        if len(highs) < 50:
            return levels
        
        # Pivot points
        window = 5
        for i in range(window, len(highs) - window):
            # Swing high
            if all(highs[i] >= highs[j] for j in range(i-window, i+window+1)):
                levels.append({'price': highs[i], 'type': 'resistance', 'strength': 1})
            
            # Swing low
            if all(lows[i] <= lows[j] for j in range(i-window, i+window+1)):
                levels.append({'price': lows[i], 'type': 'support', 'strength': 1})
        
        # Keep only recent and significant levels
        return levels[-20:]
    
    def _check_volume_confirmation(self, closes: List[float], volumes: List[float]) -> bool:
        """Check for volume confirmation of moves"""
        if len(volumes) < 10:
            return False
        
        recent_vol = np.mean(volumes[-5:])
        avg_vol = np.mean(volumes[-20:]) if len(volumes) >= 20 else np.mean(volumes)
        
        return recent_vol > avg_vol * 1.2  # 20% above average
    
    def _calculate_market_sentiment(self, closes: List[float], volumes: List[float]) -> str:
        """Calculate market sentiment indicator"""
        if len(closes) < 30:
            return 'neutral'
        
        # Price velocity
        price_velocity = (closes[-1] - closes[-10]) / closes[-10]
        
        # Volume velocity
        volume_velocity = 0
        if len(volumes) >= 20:
            recent_vol = np.mean(volumes[-10:])
            older_vol = np.mean(volumes[-20:-10])
            volume_velocity = (recent_vol - older_vol) / older_vol if older_vol > 0 else 0
        
        # Volatility
        volatility = np.std(closes[-20:]) / np.mean(closes[-20:])
        
        # Sentiment calculation
        if price_velocity > 0.02 and volume_velocity > 0.3 and volatility > 0.03:
            return 'extreme_greed'
        elif price_velocity < -0.02 and volume_velocity > 0.3 and volatility > 0.03:
            return 'extreme_fear'
        else:
            return 'neutral'
    
    def _detect_volatility_clustering(self, closes: List[float]) -> Dict:
        """Detect volatility clustering"""
        if len(closes) < 30:
            return {"is_clustering": False, "strength": 0}
        
        # Calculate rolling volatility
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        
        recent_vol = np.std(returns[-10:])
        historical_vol = np.std(returns[-30:-10])
        
        vol_ratio = recent_vol / historical_vol if historical_vol > 0 else 1
        
        is_clustering = vol_ratio > 1.5  # 50% higher volatility
        
        return {"is_clustering": is_clustering, "strength": vol_ratio}
    
    def _calculate_hold_confidence(self, profit_pct: float, closes: List[float], volumes: List[float], entry_analysis: Dict = None) -> float:
        """Calculate confidence in holding the position"""
        confidence = 50.0  # Base confidence
        
        # Profit factor
        if profit_pct > 0.01:
            confidence += 20
        elif profit_pct > 0.005:
            confidence += 10
        elif profit_pct < -0.01:
            confidence -= 20
        
        # Trend strength
        if len(closes) >= 20:
            trend_strength = self._get_market_trend_strength(closes)
            if trend_strength == 'strong_trend':
                confidence += 15
            elif trend_strength == 'choppy':
                confidence -= 10
        
        # Entry analysis confidence
        if entry_analysis:
            entry_conf = entry_analysis.get('confidence', 50)
            confidence += (entry_conf - 50) * 0.3
        
        return max(0, min(100, confidence))
    
    def _get_hold_suggestion(self, profit_pct: float, hold_confidence: float) -> str:
        """Get suggestion for holding position"""
        if hold_confidence > 80:
            return "STRONG_HOLD"
        elif hold_confidence > 60:
            return "HOLD"
        elif hold_confidence > 40:
            return "WEAK_HOLD"
        else:
            return "CONSIDER_EXIT"
    
    def _calculate_price_action_quality(self, closes: List[float]) -> float:
        """Calculate price action quality (0-1)"""
        if len(closes) < 10:
            return 0.5
        
        try:
            # Trend consistency
            x = np.arange(len(closes))
            slope, _ = np.polyfit(x, closes, 1)
            closes_array = np.array(closes)
            predicted = slope * x + closes_array[0]  # Use closes_array[0] instead of closes[0]
            
            # R-squared
            ss_res = np.sum((closes_array - predicted) ** 2)
            ss_tot = np.sum((closes_array - np.mean(closes_array)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            return max(0, min(1, r_squared))
        except Exception as e:
            logger.error(f"Error calculating price action quality: {e}")
            return 0.5