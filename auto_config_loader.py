
import json
from binance.client import Client
from binance.exceptions import BinanceAPIException

def get_futures_balance(api_key, api_secret):
    """Get USDT balance from Binance Futures account with proper error handling"""
    try:
        # Deteksi testnet atau real dengan lebih akurat
        is_testnet = False
        if api_key and api_secret:
            # Testnet API key biasanya lebih pendek atau mengandung 'test'
            if len(api_key) < 50 or "test" in api_key.lower():
                is_testnet = True
        
        client = Client(api_key, api_secret, testnet=is_testnet)
        
        # Test koneksi dulu
        client.futures_ping()
        
        # Ambil balance dari Futures account
        balances = client.futures_account_balance()
        usdt_balance = next((float(x['balance']) for x in balances if x['asset'] == 'USDT'), 0)
        
        print(f"[INFO] Successfully connected to Binance Futures ({'TESTNET' if is_testnet else 'REAL'})")
        return usdt_balance
        
    except BinanceAPIException as e:
        print(f"[ERROR] Binance API Error: {e}")
        if "API-key format invalid" in str(e):
            print("[ERROR] API key format salah atau tidak valid")
        elif "restricted location" in str(e):
            print("[ERROR] Server Anda diblokir oleh Binance. Gunakan VPS di region yang didukung.")
        return 0
    except Exception as e:
        print(f"[ERROR] Failed to get Futures balance: {e}")
        return 0

def load_config_auto(api_key, api_secret, config_file="config_hybrid_all.json"):
    """Load configuration based on account balance"""
    if not api_key or not api_secret:
        print("[ERROR] API key atau secret tidak tersedia")
        return None
    
    balance = get_futures_balance(api_key, api_secret)
    
    if balance == 0:
        print("[WARN] Tidak bisa mendapatkan balance. Menggunakan config default.")
        # Return config untuk balance minimal
        with open(config_file, "r") as f:
            all_configs = json.load(f)
        return all_configs["$3"]  # Config untuk $3 balance
    
    print(f"[INFO] Detected Futures Balance: ${balance:.2f}")

    with open(config_file, "r") as f:
        all_configs = json.load(f)

    keys = sorted([int(k.strip('$')) for k in all_configs])
    eligible_keys = [k for k in keys if k <= balance]

    if not eligible_keys:
        chosen_key = keys[0]
        print(f"[WARN] Balance ${balance:.2f} terlalu kecil. Menggunakan config minimal ${chosen_key}")
    else:
        chosen_key = max(eligible_keys)

    print(f"[INFO] Using config for balance: ${chosen_key}")
    return all_configs[f"${chosen_key}"]
