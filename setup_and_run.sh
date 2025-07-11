#!/usr/bin/env bash
set -e

echo "🤖 ARIFBOT - Binance Futures Trading Bot"
echo "📊 Mode: Professional Futures Trading"
echo "🔧 Setting up environment..."

# Cari python3.10 dari pyenv atau fallback ke python3
PYTHON_BIN=""
if command -v python3.10 >/dev/null 2>&1; then
  PYTHON_BIN="python3.10"
elif [ -f "$HOME/.pyenv/versions/3.10.14/bin/python" ]; then
  PYTHON_BIN="$HOME/.pyenv/versions/3.10.14/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "[ERROR] Python 3.10 tidak ditemukan. Install dulu Python 3.10."
  echo "Saran: Gunakan pyenv untuk install Python 3.10.14"
  exit 1
fi

echo "[INFO] Menggunakan Python: $($PYTHON_BIN --version)"

# 1. Setup Python virtual environment
if [ ! -d "venv" ]; then
  echo "[INFO] Membuat virtual environment..."
  $PYTHON_BIN -m venv venv
fi

# 2. Aktifkan venv dan upgrade pip
source venv/bin/activate
python --version
pip install --upgrade pip setuptools wheel

# 3. Install dependencies
pip install -r requirements_pro_trader.txt

# 4. Copy .env.template ke .env jika belum ada
if [ ! -f ".env" ]; then
  cp .env.template .env
  echo "[INFO] File .env sudah dibuat. Silakan isi API_KEY, API_SECRET, TELEGRAM_TOKEN, dan TELEGRAM_CHAT_ID di file .env sebelum menjalankan bot."
  echo "⚠️  PENTING: Bot ini khusus untuk Binance Futures (bukan Spot)"
  echo "📝 Contoh format .env:"
  cat .env.template
  exit 0
fi

# 5. Validasi .env
if [ ! -s ".env" ]; then
  echo "[ERROR] File .env kosong. Silakan isi API key dan secret terlebih dahulu."
  exit 1
fi

echo "✅ Setup selesai! Bot siap untuk Binance Futures Trading"
echo "🚀 Menjalankan bot..."

# 6. Jalankan bot
python main.py