# Pro Trader Bot – Flow & Maintenance Guide

_Last update: 2025-07-08_

---

## 1. Arsitektur Singkat

```
main.py ─┐  (auto-config + Kelly + market safety)
         │
         ├─ core/
         │   └─ bot_runner.py  ⇢  loop trading multi-symbol
         │
         └─ modules/
             ├─ smart_trading.py      # SmartEntry & SmartExit
             ├─ position_sizing.py   # Kelly & risk tiers
             ├─ indicators.py / market_analysis.py / …
             └─ telegram_handler.py   # Notifikasi BOT Telegram
```

## 2. Proses Booting

1. **Load env** – `API_KEY`, `API_SECRET`, `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`.
2. **Auto-config** – `auto_config_loader.load_config_auto()` membaca saldo USDT dan memilih preset dari `config_hybrid_all.json`.
3. **Kelly check** – Jika saldo ≥ 50 USDT, kelly partial diaktifkan.
4. **Market safety** – Fetch 60 klines publik, hitung tren (`market_analyzer`), abort jika downtrend.
5. **Run bot** – `BinanceFuturesProBot.start()` ⇒ `trading_loop()`.

## 3. Trading Loop (per 15 detik)

Untuk setiap simbol di `self.symbols` (top 10 besar):

| Tahap | Modul | Keterangan |
|-------|-------|-----------|
| 1 | **get_klines_data** | Ambil 50 kline `5m` via REST. |
| 2 | **SmartExit** | Jika ada posisi → cek exit layer (SL keras, pattern, trailing, dst.). |
| 3 | **SmartEntry** | Jika belum ada posisi & `max_open_positions` belum penuh ⇒ analisis entry. |
| 4 | **execute_trade_pro** | Hitung size:  risk% (tier) × equity × leverage (tier)  → order MARKET. |
| 5 | **Logging + Telegram** | Kirim notifikasi entry / exit. |

Semua angka risiko ter-clamp sesuai tier (lihat §4).

## 4. Tier Risiko (per 2025-07-08)

| Equity | Risk / Posisi | Leverage Max | Portfolio Heat |
|--------|---------------|--------------|----------------|
| < $20 | 0.3 % – 3 % | 2× | 10 % |
| $20 – 99 | 0.5 % – 4 % | 2× | 10 % |
| $100 – 499 | 0.8 % – 3 % | 2.5× | 12 % |
| ≥ $500 | 0.8 % – 2.5 % | 3× | 12 % |


## 5. Deployment Steps

```bash
# VPS Ubuntu 22.04 / 1 GB + swap 1 GB
sudo apt update && sudo apt install -y python3-venv git

git clone <repo> && cd <repo>/project
python3 -m venv venv && source venv/bin/activate
pip install -r requirements_pro_trader.txt

cp .env.example .env  # isi API & TELEGRAM KEY
python run_bot.py     # mode pro, auto-restart
```

> _Tip_: Untuk testnet ➜ `export BINANCE_USE_TESTNET=true` sebelum menjalankan bot.

## 6. Maintenance Checklist

| Interval | Langkah |
|----------|---------|
| Harian | • Cek telegram `/status`, memori VPS < 800 MB. |
| Mingguan | • `tail -f bot.log` pastikan tidak ada error API berulang.<br>• Perbarui requirement `pip install -U python-binance python-telegram-bot`. |
| Bulanan | • Tarik keuntungan (jaga buffer ≥ 15 %).<br>• Evaluasi win-rate, update tier jika perlu. |
| Saat error besar | • Jalankan ulang `run_bot.py`.<br>• Jika error module, `git pull` lalu reinstall requirement. |

---

## 7. Lokasi Kode Kunci

| Fungsi | Lokasi |
|--------|--------|
| Risk tier & leverage | `modules/position_sizing.calculate_position_size` |
| Multi-symbol list | `config_manager.symbols` |
| Trading loop | `core/bot_runner.trading_loop` |
| Exit strategy | `modules/smart_trading.SmartExit` |

Simpan dokumen ini.  Untuk perubahan produksi cukup edit file konfigurasi & tier di lokasi di atas, lalu restart bot.

## 8. VPS Memory Guard & Auto-Reboot

| Trigger | Action |
|---------|--------|
| RSS > **700 MB** (selama pengecekan `optimize_memory()`)|  • Kirim pesan Telegram ⚠️  
• Perintah `sudo reboot` (jika env `ALLOW_AUTO_REBOOT=true`) |

Cara mengaktifkan:
```bash
export ALLOW_AUTO_REBOOT=true   # set di ~/.bashrc atau crontab
```
Pastikan user `ubuntu` (atau yg menjalankan bot) punya izin `sudo reboot` tanpa password (edit `/etc/sudoers` – optional).

Dengan guard ini VPS 1 GB akan otomatis restart sebelum kehabisan memori; `run_bot.py` memakai loop auto-restart sehingga bot akan aktif kembali ±1-2 menit setelah reboot.