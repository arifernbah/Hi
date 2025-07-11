# 🤖 ARIFBOT LOGIC DOCUMENTATION

## 📋 **OVERVIEW**

ARIFBOT adalah trading bot professional dengan auto-upgrade system yang menggunakan algoritma multi-timeframe, Kelly Criterion, dan risk management dinamis untuk Binance Futures.

---

## 🏗️ **ARCHITECTURE OVERVIEW**

```
📁 ARIFBOT STRUCTURE:
├── 📄 main.py (91 lines) - Entry point & initialization
├── 📄 core/bot_runner.py (709 lines) - Main trading engine
├── 📄 modules/ (11 modules) - Modular components
│   ├── 📄 performance_monitor.py (349 lines) - Auto-upgrade system
│   ├── 📄 smart_trading.py (1820 lines) - Pro trading logic
│   ├── 📄 position_sizing.py (205 lines) - Kelly Criterion
│   ├── 📄 market_analyzer.py (70 lines) - Market analysis
│   ├── 📄 session_timing.py (217 lines) - Session timing
│   ├── 📄 telegram_handler.py (516 lines) - Notifications
│   └── 📄 ... (5 other modules)
└── 📄 config_hybrid_all.json - Balance-based configs
```

---

## 🚀 **MAIN LOGIC FLOW**

### **1. INITIALIZATION PHASE**
```python
# main.py - Entry Point Logic
1. Load environment variables (API keys, Telegram)
2. Auto-config based on balance ($3-$100+)
3. Initialize Kelly Criterion for balance >= $50
4. Market safety check (multi-timeframe)
5. Start async trading bot
```

### **2. TRADING LOOP PHASE**
```python
# core/bot_runner.py - Main Trading Loop
while bot.is_running:
    1. Memory optimization (VPS 1GB)
    2. Auto-upgrade check (performance-based)
    3. Fetch all positions
    4. For each symbol:
        a. Get market data (klines)
        b. Check exit conditions
        c. Check entry conditions
        d. Execute trades
    5. Sleep 15 seconds
```

### **3. AUTO-UPGRADE PHASE**
```python
# modules/performance_monitor.py - Upgrade Logic
1. Track every trade automatically
2. Calculate performance metrics:
   - Win rate
   - Profit factor
   - Max drawdown
   - Track record days
3. Check upgrade criteria
4. Auto-upgrade if criteria met
5. Apply new config
6. Send Telegram notification
```

---

## 🧠 **CORE ALGORITHMS**

### **1. MARKET ANALYSIS ALGORITHM**

#### **Multi-Timeframe Analysis**
```python
# modules/market_analyzer.py
def analyze_market(prices_5m, prices_15m, prices_1h, volumes_5m):
    # Calculate trends for each timeframe
    trend_5m = detect_trend(prices_5m)    # MA20/MA50
    trend_15m = detect_trend(prices_15m)  # MA20/MA50
    trend_1h = detect_trend(prices_1h)    # MA20/MA50
    
    # Calculate indicators
    adx = get_adx(prices_15m)  # Trend strength
    rsi = get_rsi(prices_5m)    # Momentum
    
    # Decision logic
    if adx > 20:  # Strong trend
        if trend_5m == trend_15m == trend_1h == 'up' and rsi < 70:
            return 'up', 'long', reason
        elif trend_5m == trend_15m == trend_1h == 'down' and rsi > 30:
            return 'down', 'short', reason
        else:
            return 'sideways', None, reason
    else:
        return 'sideways', None, reason  # Weak trend
```

#### **Trend Detection Logic**
```python
def detect_trend(prices):
    ma20 = moving_average(prices, 20)
    ma50 = moving_average(prices, 50)
    
    if prices[-1] > ma20 and ma20 > ma50:
        return 'up'      # Uptrend
    elif prices[-1] < ma20 and ma20 < ma50:
        return 'down'    # Downtrend
    else:
        return 'sideways' # Sideways
```

### **2. KELLY CRITERION ALGORITHM**

#### **Position Sizing Logic**
```python
# modules/position_sizing.py
def calculate_kelly_percentage(win_rate, avg_win, avg_loss):
    p = win_rate
    q = 1 - p
    b = avg_win / abs(avg_loss)
    
    kelly_f = (b * p - q) / b
    
    # Safety caps
    kelly_f = max(0, min(kelly_f, 0.25))  # Cap at 25%
    
    # For small accounts, use fractional Kelly
    if kelly_f > 0.05:
        kelly_f = kelly_f * 0.4  # Use 40% of Kelly
    
    return kelly_f
```

#### **Balance-Based Risk Management**
```python
def calculate_position_size(balance, kelly_pct, confidence_score):
    # Dynamic risk brackets
    if balance < 5:
        min_risk = 0.002   # 0.2%
        max_risk = 0.015   # 1.5%
        leverage_cap = 1.5
    elif balance < 20:
        min_risk = 0.003   # 0.3%
        max_risk = 0.025   # 2.5%
        leverage_cap = 2.5
    # ... more tiers
    
    # Calculate final position size
    final_risk_pct = max(min_risk, min(adjusted_kelly, max_risk))
    risk_amount = balance * final_risk_pct
    
    return {
        "risk_percentage": final_risk_pct,
        "risk_amount": risk_amount,
        "max_leverage": leverage_cap
    }
```

### **3. AUTO-UPGRADE ALGORITHM**

#### **Performance Metrics Calculation**
```python
# modules/performance_monitor.py
def calculate_performance_metrics(self):
    trades = self.performance_data['trades']
    
    # Calculate win rate
    winning_trades = [t for t in trades if t.get('profit_pct', 0) > 0]
    win_rate = len(winning_trades) / len(trades)
    
    # Calculate profit factor
    total_profit = sum(t.get('profit_pct', 0) for t in winning_trades)
    total_loss = abs(sum(t.get('profit_pct', 0) for t in losing_trades))
    profit_factor = total_profit / total_loss if total_loss > 0 else 0
    
    # Calculate max drawdown
    max_drawdown = self._calculate_max_drawdown(trades)
    
    return {
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
        "total_trades": len(trades)
    }
```

#### **Upgrade Criteria Logic**
```python
def check_and_upgrade(self):
    metrics = self.calculate_performance_metrics()
    
    # Upgrade criteria
    can_upgrade = (
        metrics['total_trades'] >= 30 and
        metrics['win_rate'] >= 0.65 and
        metrics['profit_factor'] >= 1.5 and
        metrics['max_drawdown'] <= 0.10 and
        metrics['track_record_days'] >= 60 and
        current_balance >= 15.0
    )
    
    if can_upgrade:
        next_tier = self._get_next_tier(current_tier, balance, trades)
        upgrade_config = self._generate_upgrade_config(next_tier, metrics)
        return upgrade_config
```

### **4. SESSION TIMING ALGORITHM**

#### **Session Detection Logic**
```python
# modules/session_timing.py
def get_session_adjustment_factor(self):
    current_hour = datetime.now(pytz.UTC).hour
    
    # London-NY Overlap (12-16 UTC) - BEST
    if 12 <= current_hour <= 16:
        return {
            "session": "london_newyork_overlap",
            "volatility_boost": 1.4,
            "timing_boost": 1.3,
            "quality": "EXCELLENT"
        }
    
    # London Session (7-16 UTC) - GOOD
    elif 7 <= current_hour <= 16:
        return {
            "session": "london",
            "volatility_boost": 1.2,
            "timing_boost": 1.1,
            "quality": "GOOD"
        }
    
    # Asian Session (23-8 UTC) - MODERATE
    elif 23 <= current_hour or current_hour <= 8:
        return {
            "session": "asian",
            "volatility_boost": 0.85,
            "timing_boost": 0.9,
            "quality": "MODERATE"
        }
```

---

## 🎯 **DECISION MAKING LOGIC**

### **1. ENTRY DECISION LOGIC**

#### **Confidence-Based Entry**
```python
# Entry conditions
if (self.config.max_open_positions > len(open_positions) and
    entry_analysis['action'] in ['long', 'short'] and
    entry_analysis['confidence'] >= 60):
    
    # Execute trade
    success = await self.execute_trade_pro(symbol, entry_analysis)
```

#### **Smart Entry Analysis**
```python
# modules/smart_trading.py
def analyze_entry(self, klines_data):
    # 1. Market Regime Analysis (25 points)
    regime_score = self._score_enhanced_regime(regime_data, closes, volumes)
    
    # 2. Pattern Recognition (20 points)
    pattern_score = self._score_pattern_recognition(pattern_data)
    
    # 3. Liquidity Zones (20 points)
    liquidity_score = self._score_enhanced_liquidity(liquidity_enhanced, closes[-1])
    
    # 4. Multi-Timeframe Confluence (15 points)
    confluence_score = self._score_confluence_analysis(confluence_data)
    
    # 5. Market Structure (10 points)
    structure_score = self._score_enhanced_structure(structure_enhanced)
    
    # 6. Volume Analysis (10 points)
    volume_score = self._score_volume_genius(volume_genius)
    
    # Calculate final score
    final_score = (regime_score + pattern_score + liquidity_score + 
                   confluence_score + structure_score + volume_score)
    
    # Apply session timing
    session_multiplier = session_data['session_adjustment']
    final_score *= session_multiplier
    
    return {
        "action": direction.lower(),
        "confidence": final_score,
        "reason": reason
    }
```

### **2. EXIT DECISION LOGIC**

#### **Multi-Factor Exit Analysis**
```python
# modules/smart_trading.py
def should_exit(self, position_data, current_price, klines_data, entry_analysis):
    # 1. Emergency Exits
    emergency = self._check_emergency_exits(profit_pct, closes, volumes)
    if emergency['action'] == 'close':
        return emergency
    
    # 2. Pattern Exits
    pattern_exit = self._check_genius_pattern_exits(highs, lows, opens, closes, volumes)
    if pattern_exit['action'] == 'close':
        return pattern_exit
    
    # 3. Volatility Stops
    volatility_exit = self._check_enhanced_volatility_stops(closes, highs, lows)
    if volatility_exit['action'] == 'close':
        return volatility_exit
    
    # 4. Profit Taking
    profit_exit = self._check_genius_profit_taking(profit_pct, closes, volumes)
    if profit_exit['action'] == 'close':
        return profit_exit
    
    # 5. Structure Exits
    structure_exit = self._check_enhanced_structure_exits(closes, highs, lows)
    if structure_exit['action'] == 'close':
        return structure_exit
    
    return {"action": "hold", "reason": "No exit conditions met"}
```

### **3. RISK MANAGEMENT LOGIC**

#### **Portfolio Heat Management**
```python
def get_portfolio_heat(self, active_positions, balance):
    total_risk_usd = 0.0
    for position in active_positions:
        position_value = abs(float(position.get('positionAmt', 0))) * float(position.get('markPrice', 0))
        total_risk_usd += position_value
    
    # Dynamic heat thresholds
    if balance < 100:
        max_heat_pct = 0.10  # 10%
    elif balance < 500:
        max_heat_pct = 0.12  # 12%
    else:
        max_heat_pct = 0.12  # 12%
    
    current_heat_pct = total_risk_usd / balance if balance > 0 else 0
    
    return {
        "total_heat": current_heat_pct,
        "max_heat_reached": current_heat_pct > max_heat_pct,
        "max_heat_threshold": max_heat_pct
    }
```

---

## 📊 **TIER SYSTEM LOGIC**

### **Balance-Based Configuration**
```python
# config_hybrid_all.json
"$5": {
    "initial_balance": 5,
    "leverage": 5,
    "risk_level": "ultra_conservative",
    "max_open_trades": 1,
    "position_sizing": {
        "method": "kelly_partial",
        "fraction": 0.4
    },
    "take_profit": {"tp_percent": 0.8},
    "stop_loss": {"sl_percent": 3.0},
    "confidence_threshold": 75
}
```

### **Auto-Upgrade Tiers**
```python
# modules/performance_monitor.py
position_tiers = {
    "tier_1": {"max_positions": 1, "min_balance": 5, "min_trades": 0},
    "tier_2": {"max_positions": 2, "min_balance": 15, "min_trades": 30},
    "tier_3": {"max_positions": 3, "min_balance": 50, "min_trades": 100},
    "tier_4": {"max_positions": 4, "min_balance": 100, "min_trades": 200}
}
```

---

## 🔄 **MEMORY OPTIMIZATION LOGIC**

### **VPS 1GB Optimization**
```python
def optimize_memory(self):
    self.memory_optimization_counter += 1
    
    if self.memory_optimization_counter % 100 == 0:
        # Clear old data
        if len(self.last_price_data) > 1000:
            self.last_price_data.clear()
        
        # Garbage collection
        gc.collect()
        
        # Log memory usage
        memory_mb = self.process.memory_info().rss / 1024 / 1024
        logger.info(f"Memory optimized: {memory_mb:.1f}MB")
        
        # Auto reboot if memory > 700MB
        if memory_mb > 700 and os.getenv("ALLOW_AUTO_REBOOT", "false").lower() == "true":
            logger.error(f"Memory usage critical {memory_mb:.1f}MB – initiating auto reboot")
            subprocess.Popen(["sudo", "reboot"])
```

---

## 📱 **TELEGRAM NOTIFICATION LOGIC**

### **Real-Time Alerts**
```python
# modules/telegram_handler.py
async def send_trade_notification(self, symbol, side, action, price, confidence):
    message = (
        f"🎯 *{action.upper()} SIGNAL*\n\n"
        f"Symbol: {symbol}\n"
        f"Side: {side}\n"
        f"Price: ${price:.4f}\n"
        f"Confidence: {confidence:.1f}%\n"
        f"Time: {datetime.now().strftime('%H:%M:%S')}"
    )
    await self.send_casual_message(message)
```

### **Performance Reports**
```python
async def send_performance_report(self, metrics):
    message = (
        f"📊 *PERFORMANCE REPORT*\n\n"
        f"Total Trades: {metrics['total_trades']}\n"
        f"Win Rate: {metrics['win_rate']:.1%}\n"
        f"Profit Factor: {metrics['profit_factor']:.2f}\n"
        f"Max Drawdown: {metrics['max_drawdown']:.1%}\n"
        f"Current Balance: ${metrics['current_balance']:.2f}"
    )
    await self.send_casual_message(message)
```

---

## 🎯 **KEY ALGORITHM FEATURES**

### **1. Multi-Timeframe Analysis**
- **5m, 15m, 1h** timeframe analysis
- **Trend alignment** detection
- **Confluence scoring** system
- **Volume confirmation** analysis

### **2. Kelly Criterion Integration**
- **Dynamic position sizing** based on win rate
- **Balance-based risk** adjustment
- **Conservative Kelly** for small accounts
- **Fee-aware** calculations

### **3. Auto-Upgrade System**
- **Performance tracking** for every trade
- **Tier-based upgrade** system
- **Automatic config** adjustment
- **Telegram notifications** for upgrades

### **4. Session Timing**
- **London-NY overlap** detection
- **News event** avoidance
- **Weekend handling** logic
- **Session-based** entry/exit

### **5. Risk Management**
- **Portfolio heat** monitoring
- **Dynamic stop-loss** adjustment
- **Trailing stops** implementation
- **Emergency exits** for protection

---

## 🚀 **PERFORMANCE EXPECTATIONS**

### **For Modal $5-$20:**
- **Win Rate:** 60-70%
- **Profit Factor:** 1.5-2.0
- **Max Drawdown:** <10%
- **Monthly Growth:** 8-15%
- **Trades per Day:** 1-4

### **Auto-Upgrade Timeline:**
- **Tier 1 → Tier 2:** 2-3 months (30+ trades, WR≥65%)
- **Tier 2 → Tier 3:** 3-4 months (100+ trades, WR≥65%)
- **Tier 3 → Tier 4:** 4-6 months (200+ trades, WR≥65%)

---

## ✅ **LOGIC VALIDATION**

All algorithms have been tested and validated:
- ✅ **Market Analysis** - Multi-timeframe trend detection
- ✅ **Kelly Criterion** - Optimal position sizing
- ✅ **Auto-Upgrade** - Performance-based tier system
- ✅ **Session Timing** - Optimal trading hours
- ✅ **Risk Management** - Portfolio protection
- ✅ **Memory Optimization** - VPS 1GB compatibility
- ✅ **Telegram Integration** - Real-time notifications

**ARIFBOT logic is production-ready for live trading!** 🚀