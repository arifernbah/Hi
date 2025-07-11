import numpy as np

def moving_average(prices, window):
    if len(prices) < window:
        return np.mean(prices)
    return np.mean(prices[-window:])

def get_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - 100 / (1 + rs)
    for i in range(period, len(deltas)):
        delta = deltas[i]
        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi = 100 - 100 / (1 + rs)
    return rsi

def get_adx(prices, period=14):
    # Simple ADX approximation (not 100% accurate, but enough for filter)
    if len(prices) < period + 1:
        return 20
    up_moves = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    down_moves = [prices[i-1] - prices[i] for i in range(1, len(prices))]
    plus_dm = [um if um > dm and um > 0 else 0 for um, dm in zip(up_moves, down_moves)]
    minus_dm = [dm if dm > um and dm > 0 else 0 for um, dm in zip(up_moves, down_moves)]
    tr = [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
    atr = np.mean(tr[-period:])
    plus_di = 100 * (np.mean(plus_dm[-period:]) / atr) if atr != 0 else 0
    minus_di = 100 * (np.mean(minus_dm[-period:]) / atr) if atr != 0 else 0
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) != 0 else 0
    return dx

def detect_trend(prices):
    ma20 = moving_average(prices, 20)
    ma50 = moving_average(prices, 50)
    if prices[-1] > ma20 and ma20 > ma50:
        return 'up'
    elif prices[-1] < ma20 and ma20 < ma50:
        return 'down'
    else:
        return 'sideways'

def analyze_market(prices_5m, prices_15m, prices_1h, volumes_5m):
    trend_5m = detect_trend(prices_5m)
    trend_15m = detect_trend(prices_15m)
    trend_1h = detect_trend(prices_1h)
    adx = get_adx(prices_15m)
    rsi = get_rsi(prices_5m)
    reason = f"Trend 5m:{trend_5m}, 15m:{trend_15m}, 1h:{trend_1h}, ADX:{adx:.1f}, RSI:{rsi:.1f}"
    if adx > 20:
        if trend_5m == trend_15m == trend_1h == 'up' and rsi < 70:
            return 'up', 'long', reason
        elif trend_5m == trend_15m == trend_1h == 'down' and rsi > 30:
            return 'down', 'short', reason
        else:
            return 'sideways', None, reason
    else:
        return 'sideways', None, reason