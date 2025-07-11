# constants.py
# Dynamic Fee Rate Management

# Default fee rates (bisa diupdate runtime)
DEFAULT_FEE_RATE = 0.0008  # 0.08% default Binance Futures
VIP_FEE_RATE = 0.0004      # 0.04% untuk VIP users
PROMO_FEE_RATE = 0.0006    # 0.06% untuk promo periods

# Current active fee rate (akan diupdate berdasarkan kondisi)
FEE_RATE = DEFAULT_FEE_RATE

def update_fee_rate(new_rate: float = None, fee_type: str = "default"):
    """Update fee rate secara dinamis"""
    global FEE_RATE
    
    if new_rate is not None:
        FEE_RATE = new_rate
    elif fee_type == "vip":
        FEE_RATE = VIP_FEE_RATE
    elif fee_type == "promo":
        FEE_RATE = PROMO_FEE_RATE
    else:
        FEE_RATE = DEFAULT_FEE_RATE
    
    return FEE_RATE

def get_fee_rate() -> float:
    """Get current fee rate"""
    return FEE_RATE

def get_fee_info() -> dict:
    """Get info tentang fee rates"""
    return {
        "current_fee": FEE_RATE,
        "default_fee": DEFAULT_FEE_RATE,
        "vip_fee": VIP_FEE_RATE,
        "promo_fee": PROMO_FEE_RATE
    }