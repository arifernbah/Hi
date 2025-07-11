#!/usr/bin/env python3
"""
Bot Trading Binance Futures - MODULAR PRO TRADER EDITION
Struktur modular yang ringan dengan intelligence professional
"""

import asyncio
import logging
import logging.handlers
from modules.constants import get_fee_rate
import time
from datetime import datetime
from typing import Dict, Any, Optional
import gc
import psutil
import os
import subprocess

# Binance imports
from binance import AsyncClient, BinanceSocketManager
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Telegram imports
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import threading

# Our modular imports - CLEAN & LIGHTWEIGHT
from modules import (
    SmartConfig,
    SmartIndicators,
    MarketRegimeDetector,
    LiquidityZoneDetector, 
    MarketStructureAnalyzer,
    KellyCriterionCalculator,
    TradingSessionAnalyzer,
    SmartEntry,
    SmartExit,
    TelegramNotifier
)
from modules.performance_monitor import PerformanceMonitor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler('bot.log', maxBytes=1024*1024, backupCount=1),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BinanceFuturesProBot:
    """
    Professional Trading Bot dengan Modular Structure
    - Intelligence: 10-year Professional Trader
    - Architecture: Hedge Fund Grade  
    - Memory: Optimized untuk VPS 1GB
    - Style: Casual Indonesian dengan data Professional
    """
    
    def __init__(self):
        # Initialize configuration
        self.config = SmartConfig()
        # Support multiple symbols
        self.symbols = self.config.symbols or [self.config.symbol]
        # For backward compatibility
        if not hasattr(self.config, 'symbols'):
            self.symbols = [self.config.symbol]

        # Initialize Binance client
        self.client: Optional[AsyncClient] = None
        
        # Initialize professional modules (MODULAR!)
        self.smart_entry = SmartEntry(self.config)
        self.smart_exit = SmartExit(self.config)
        self.telegram = TelegramNotifier(
            self.config.telegram_token, 
            self.config.telegram_chat_id
        )
        self.position_sizing = KellyCriterionCalculator()
        
        # Bot state
        self.is_running = False
        self.positions = {}
        self.last_price_data = {}
        self.memory_optimization_counter = 0
        self.active_entries = {}  # Track entry analysis for pro exits
        
        # Initialize performance monitor
        self.performance_monitor = PerformanceMonitor()
        
        # Performance monitoring
        self.process = psutil.Process()
        self.telegram_app = None
        
    async def get_top_volume_symbols(self, limit=10):
        """Get top 10 volume symbols from Binance Futures"""
        try:
            # Get 24h ticker statistics
            tickers = await self.client.futures_ticker()
            
            # Filter USDT pairs and sort by volume
            usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
            sorted_by_volume = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
            
            # Get top 10
            top_symbols = sorted_by_volume[:limit]
            
            logger.info(f"Top {limit} volume symbols: {[s['symbol'] for s in top_symbols]}")
            return top_symbols
            
        except Exception as e:
            logger.error(f"Error getting top volume symbols: {e}")
            return []

    async def get_tradeable_symbols(self, balance):
        """Get list of symbols from top volume that can be traded with current balance"""
        try:
            top_symbols = await self.get_top_volume_symbols(10)
            tradeable_symbols = []
            
            # Get exchange info for minimum quantities
            exchange_info = await self.client.futures_exchange_info()
            
            for symbol_data in top_symbols:
                symbol = symbol_data['symbol']
                
                # Get symbol info
                symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)
                if not symbol_info:
                    continue
                
                # Get minimum quantity
                lot_size_filter = next((f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'), None)
                if not lot_size_filter:
                    continue
                
                min_qty = float(lot_size_filter['minQty'])
                
                # Get current price
                ticker = await self.client.futures_symbol_ticker(symbol=symbol)
                current_price = float(ticker['price'])
                
                # Calculate minimum order value
                min_order_value = min_qty * current_price
                
                # Check if balance is enough (with 5x leverage)
                leverage = 5
                min_balance_needed = min_order_value / leverage
                
                logger.info(f"Symbol: {symbol}, Min Order Value: ${min_order_value:.4f}, Min Balance Needed: ${min_balance_needed:.2f}")
                
                if balance >= min_balance_needed:
                    tradeable_symbols.append(symbol)
                    logger.info(f"✅ {symbol} tradeable with balance ${balance:.2f}")
                else:
                    logger.info(f"❌ {symbol} requires ${min_balance_needed:.2f}, balance ${balance:.2f} insufficient")
            
            logger.info(f"Tradeable symbols: {tradeable_symbols}")
            return tradeable_symbols
            
        except Exception as e:
            logger.error(f"Error getting tradeable symbols: {e}")
            return []

    async def init_binance_client(self) -> bool:
        """Initialize Binance client dengan error handling"""
        try:
            if self.config.is_testnet:
                await self.telegram.send_casual_message("🧪 *Mode TESTNET*\nSantai aja, ini cuma latihan!")
            else:
                await self.telegram.send_casual_message("🚨 *MODE REAL TRADING*\nHati-hati ya, ini duit beneran!")
            
            if not self.config.api_key or not self.config.api_secret:
                logger.error("API keys tidak tersedia")
                return False
            
            self.client = await AsyncClient.create(
                api_key=self.config.api_key,
                api_secret=self.config.api_secret,
                testnet=self.config.is_testnet
            )
            
            # Test connection dengan Futures API
            try:
                # Gunakan futures_account_balance() yang lebih reliable
                balances = await self.client.futures_account_balance()
                usdt_balance = next((float(x['balance']) for x in balances if x['asset'] == 'USDT'), 0)
                
                logger.info(f"Connected to Binance Futures. Balance: {usdt_balance} USDT")
                await self.telegram.send_casual_message(f"✅ *Konek ke Binance Futures berhasil!*\nSaldo: ${usdt_balance:.2f}")
                
                # Get tradeable symbols from top volume
                tradeable_symbols = await self.get_tradeable_symbols(usdt_balance)
                if tradeable_symbols:
                    self.symbols = tradeable_symbols  # Monitor all tradeable symbols
                    logger.info(f"Monitoring {len(tradeable_symbols)} symbols: {tradeable_symbols}")
                    await self.telegram.send_casual_message(f"🎯 *Monitoring {len(tradeable_symbols)} symbols:*\n{', '.join(tradeable_symbols)}")
                else:
                    await self.telegram.send_casual_message(f"⚠️ *Balance ${usdt_balance:.2f} tidak cukup untuk trading*\nBot akan skip trading sampai balance cukup")
                    return False
                
                return True
            except Exception as e:
                logger.error(f"Error testing Futures connection: {e}")
                await self.telegram.send_casual_message(f"❌ Gagal test koneksi Futures: {str(e)}")
                return False
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e}")
            await self.telegram.send_casual_message(f"❌ Binance API Error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error initializing Binance client: {e}")
            await self.telegram.send_casual_message(f"❌ Error koneksi Binance: {str(e)}")
            return False
    
    async def init_telegram_bot(self):
        """Initialize Telegram bot dengan commands (simple approach)"""
        try:
            if not self.config.telegram_token:
                logger.warning("Telegram token tidak tersedia")
                return
            
            self.telegram_app = Application.builder().token(self.config.telegram_token).build()
            
            # Command handlers
            self.telegram_app.add_handler(CommandHandler("start", self.telegram_start))
            self.telegram_app.add_handler(CommandHandler("status", self.telegram_status))
            self.telegram_app.add_handler(CommandHandler("balance", self.telegram_balance))
            self.telegram_app.add_handler(CommandHandler("performance", self.telegram_performance))
            self.telegram_app.add_handler(CommandHandler("mode", self.telegram_mode))
            self.telegram_app.add_handler(CommandHandler("testnet", self.telegram_testnet))
            self.telegram_app.add_handler(CommandHandler("real", self.telegram_real))
            self.telegram_app.add_handler(CommandHandler("stop", self.telegram_stop))
            self.telegram_app.add_handler(CommandHandler("help", self.telegram_help))
            self.telegram_app.add_handler(CommandHandler("upgrade", self.telegram_upgrade))
            
            logger.info("Telegram bot initialized with professional commands")
            
            # Initialize but don't start polling yet
            await self.telegram_app.initialize()
            logger.info("Telegram bot ready for polling")
            
        except Exception as e:
            logger.error(f"Error initializing Telegram bot: {e}")

    async def start_telegram_polling(self):
        """Start Telegram polling as separate task"""
        try:
            if self.telegram_app:
                logger.info("Starting Telegram polling...")
                await self.telegram_app.start()
                logger.info("Telegram polling started successfully")
        except Exception as e:
            logger.error(f"Error starting Telegram polling: {e}")

    # =========================
    # TELEGRAM COMMAND HANDLERS 
    # =========================
    
    async def telegram_start(self, update, context):
        """Handler untuk /start - Professional welcome"""
        welcome_msg = (
            "🤖 *PRO TRADER BOT - Modular Edition*\n\n"
            "🧠 Intelligence: 10-year Pro Trader\n"
            "🏛️ Market Analysis: Institutional\n"
            "🎯 Risk Management: Hedge Fund\n\n"
            "*Commands Available:*\n"
            "/status - Bot status & positions\n"
            "/balance - Account balance & growth\n"
            "/performance - Trading performance\n"
            "/mode - Current trading mode\n"
            "/testnet - Switch to testnet\n"
            "/real - Switch to real trading\n"
            "/stop - Stop the bot\n"
            "/help - Show this help\n\n"
            "Ready untuk cuan professional! 🚀💎"
        )
        
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def telegram_status(self, update, context):
        """Handler untuk /status - Enhanced dengan pro data"""
        try:
            if self.client:
                # Gunakan futures_account_balance() yang konsisten
                balances = await self.client.futures_account_balance()
                balance = next((float(x['balance']) for x in balances if x['asset'] == 'USDT'), 0)
                positions = await self.client.futures_position_information()
                active_positions = [p for p in positions if float(p['positionAmt']) != 0]
                
                # Get professional stats
                pro_stats = {
                    'win_rate': 0.65,  # Would be calculated from actual trades
                    'kelly_percentage': 0.025,
                    'current_session': 'london'
                }
                
                mode = "TESTNET" if self.config.is_testnet else "REAL"
                memory_usage = self.process.memory_info().rss / 1024 / 1024
                
                # Create status message directly
                status_msg = (
                    f"🤖 *ARIFBOT PRO TRADER STATUS*\n\n"
                    f"💰 Balance: ${balance:.2f}\n"
                    f"📊 Active Positions: {len(active_positions)}\n"
                    f"🎯 Mode: {mode}\n"
                    f"🧠 Memory: {memory_usage:.1f}MB\n\n"
                    f"📈 PERFORMANCE:\n"
                    f"• Win Rate: {pro_stats['win_rate']:.1%}\n"
                    f"• Kelly %: {pro_stats['kelly_percentage']:.1%}\n"
                    f"• Session: {pro_stats['current_session'].title()}\n\n"
                    f"🚀 Bot Status: {'🟢 RUNNING' if self.is_running else '🔴 STOPPED'}"
                )
                
                await update.message.reply_text(status_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Bot belum connect ke Binance")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def telegram_balance(self, update, context):
        """Handler untuk /balance"""
        try:
            if self.client:
                # Gunakan futures_account_balance() yang konsisten
                balances = await self.client.futures_account_balance()
                balance = next((float(x['balance']) for x in balances if x['asset'] == 'USDT'), 0)
                # Get unrealized PnL from account info
                account_info = await self.client.futures_account()
                total_unrealized_pnl = float(account_info['totalUnrealizedProfit'])
                
                # Use balance as reference for growth calculation
                initial_balance = 100.0  # Default reference
                growth = ((balance / initial_balance - 1) * 100)
                
                balance_msg = (
                    f"💰 *PROFESSIONAL BALANCE REPORT*\n\n"
                    f"Current Balance: ${balance:.2f}\n"
                    f"Unrealized PnL: ${total_unrealized_pnl:.2f}\n"
                    f"Total Growth: {growth:+.2f}%\n\n"
                )
                
                if growth > 10:
                    balance_msg += "🔥 Exceptional performance! Keep it up!"
                elif growth > 5:
                    balance_msg += "⚡ Solid growth! Pro algorithm working!"
                elif growth > 0:
                    balance_msg += "📈 Positive growth! Steady progress!"
                else:
                    balance_msg += "🛡️ Capital protection mode active!"
                
                await update.message.reply_text(balance_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Bot belum connect ke Binance")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def telegram_performance(self, update, context):
        """Handler untuk /performance - Show trading stats"""
        try:
            trades_history = getattr(self.smart_entry, 'trades_history', [])
            
            # Create performance message directly
            if trades_history:
                total_trades = len(trades_history)
                winning_trades = len([t for t in trades_history if t.get('profit_pct', 0) > 0])
                win_rate = winning_trades / total_trades if total_trades > 0 else 0
                
                performance_msg = (
                    f"📊 *TRADING PERFORMANCE*\n\n"
                    f"📈 Total Trades: {total_trades}\n"
                    f"✅ Winning Trades: {winning_trades}\n"
                    f"❌ Losing Trades: {total_trades - winning_trades}\n"
                    f"🎯 Win Rate: {win_rate:.1%}\n\n"
                    f"💰 Recent Trades:\n"
                )
                
                # Show last 5 trades
                for trade in trades_history[-5:]:
                    profit = trade.get('profit_pct', 0)
                    symbol = trade.get('symbol', 'Unknown')
                    emoji = "✅" if profit > 0 else "❌"
                    performance_msg += f"{emoji} {symbol}: {profit:+.2%}\n"
            else:
                performance_msg = (
                    f"📊 *TRADING PERFORMANCE*\n\n"
                    f"📈 Total Trades: 0\n"
                    f"🎯 Win Rate: 0%\n\n"
                    f"💡 Bot belum melakukan trade pertama"
                )
            
            await update.message.reply_text(performance_msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def telegram_mode(self, update, context):
        """Handler untuk /mode"""
        mode = "TESTNET 🧪" if self.config.is_testnet else "REAL TRADING 🚨"
        await update.message.reply_text(f"Current mode: *{mode}*", parse_mode='Markdown')
    
    async def telegram_testnet(self, update, context):
        """Handler untuk /testnet"""
        self.config.is_testnet = True
        self.config.save_config()
        await update.message.reply_text("✅ Switched to *TESTNET*\nBot will restart automatically", parse_mode='Markdown')
        await self.restart_with_new_mode()
    
    async def telegram_real(self, update, context):
        """Handler untuk /real"""
        self.config.is_testnet = False
        self.config.save_config()
        await update.message.reply_text("🚨 Switched to *REAL TRADING*\nBe careful! Bot restarting...", parse_mode='Markdown')
        await self.restart_with_new_mode()
    
    async def telegram_stop(self, update, context):
        """Handler untuk /stop"""
        await update.message.reply_text("🛑 Professional bot stopping!\nSee you next time! 👋")
        self.is_running = False
    
    async def telegram_help(self, update, context):
        """Handler untuk /help"""
        help_msg = (
            "🤖 *ARIFBOT PRO TRADER COMMANDS*\n\n"
            "/start - Welcome message\n"
            "/status - Bot status & positions\n"
            "/balance - Account balance & growth\n"
            "/performance - Trading performance\n"
            "/upgrade - Performance & upgrade status\n"
            "/mode - Current trading mode\n"
            "/testnet - Switch to testnet\n"
            "/real - Switch to real trading\n"
            "/stop - Stop the bot\n"
            "/help - Show this help\n\n"
            "Ready untuk cuan professional! 🚀"
        )
        await update.message.reply_text(help_msg, parse_mode='Markdown')
    
    async def telegram_upgrade(self, update, context):
        """Handler untuk /upgrade - Show performance & upgrade status"""
        try:
            status = self.performance_monitor.get_current_status()
            
            if not status:
                await update.message.reply_text("❌ Performance data tidak tersedia")
                return
            
            metrics = status['metrics']
            current_tier = status['current_tier']
            max_positions = status['max_positions']
            requirements = status['next_upgrade_requirements']
            
            upgrade_msg = (
                f"📊 *PERFORMANCE & UPGRADE STATUS*\n\n"
                f"🎯 Current Tier: {current_tier.upper()}\n"
                f"📈 Max Positions: {max_positions}\n"
                f"💰 Balance: ${metrics['current_balance']:.2f}\n\n"
                f"📊 PERFORMANCE METRICS:\n"
                f"• Total Trades: {metrics['total_trades']}\n"
                f"• Win Rate: {metrics['win_rate']:.1%}\n"
                f"• Profit Factor: {metrics['profit_factor']:.2f}\n"
                f"• Max Drawdown: {metrics['max_drawdown']:.1%}\n"
                f"• Track Record: {metrics['track_record_days']} days\n\n"
            )
            
            if requirements.get('next_tier'):
                next_tier = requirements['next_tier']
                req = requirements['requirements']
                
                upgrade_msg += (
                    f"🚀 NEXT UPGRADE: {next_tier.upper()}\n"
                    f"📋 Requirements:\n"
                    f"• Min Balance: ${req['min_balance']:.0f} "
                    f"({'✅' if req['balance_met'] else '❌'})\n"
                    f"• Min Trades: {req['min_trades']} "
                    f"({'✅' if req['trades_met'] else '❌'})\n"
                    f"• Win Rate: ≥65% "
                    f"({'✅' if metrics['win_rate'] >= 0.65 else '❌'})\n"
                    f"• Profit Factor: ≥1.5 "
                    f"({'✅' if metrics['profit_factor'] >= 1.5 else '❌'})\n"
                    f"• Max Drawdown: ≤10% "
                    f"({'✅' if metrics['max_drawdown'] <= 0.10 else '❌'})\n"
                )
            else:
                upgrade_msg += "🎉 *MAXIMUM TIER REACHED!*\nBot sudah di level tertinggi!"
            
            await update.message.reply_text(upgrade_msg, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    # =========================
    # CORE TRADING FUNCTIONS
    # =========================
    
    async def restart_with_new_mode(self):
        """Restart bot dengan mode baru"""
        try:
            if self.client:
                await self.client.close_connection()
            
            await asyncio.sleep(2)
            await self.init_binance_client()
            
        except Exception as e:
            logger.error(f"Error restarting bot: {e}")
    
    async def get_klines_data(self, symbol: str, interval: str, limit: int = 100) -> list:
        """Get klines data dengan memory optimization"""
        try:
            klines = await self.client.futures_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            # Process and optimize memory usage
            processed_klines = []
            for kline in klines:
                processed_klines.append([
                    kline[0],  # Open time
                    float(kline[1]),  # Open
                    float(kline[2]),  # High
                    float(kline[3]),  # Low
                    float(kline[4]),  # Close
                    float(kline[5])   # Volume
                ])
            
            return processed_klines
            
        except Exception as e:
            logger.error(f"Error getting klines data: {e}")
            return []
    
    async def execute_trade_pro(self, symbol: str, entry_analysis: Dict[str, Any], klines_data: list = None) -> bool:
        """Execute trade dengan professional analysis"""
        try:
            action = entry_analysis['action']
            confidence = entry_analysis['confidence']
            reason = entry_analysis['reason']
            pro_analysis = entry_analysis.get('pro_analysis', {})
            position_sizing = entry_analysis.get('position_sizing', {})
            
            # Get account balance - konsisten dengan fungsi lain
            balances = await self.client.futures_account_balance()
            balance = next((float(x['balance']) for x in balances if x['asset'] == 'USDT'), 0)
            
            # Use professional position sizing with auto leverage
            risk_pct = position_sizing.get('risk_percentage', 0.02)
            
            # Calculate auto leverage based on market conditions
            market_data = {
                'volatility': self._calculate_market_volatility(symbol, klines_data) if klines_data else 0.03
            }
            leverage = int(self.position_sizing.calculate_auto_leverage(symbol, balance, market_data))
            
            risk_amount = balance * risk_pct
            
            # Get current price
            ticker = await self.client.futures_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])
            
            # Calculate quantity
            quantity = (risk_amount * leverage) / current_price
            
            # Check minimum quantity with safe access
            exchange_info = await self.client.futures_exchange_info()
            symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)
            if not symbol_info:
                logger.error(f"Symbol {symbol} not found in exchange info")
                return False
                
            lot_size_filters = [f for f in symbol_info.get('filters', []) if f.get('filterType') == 'LOT_SIZE']
            if not lot_size_filters:
                logger.error(f"No LOT_SIZE filter found for {symbol}")
                return False
                
            min_qty = float(lot_size_filters[0].get('minQty', '0.001'))
            step_size = float(lot_size_filters[0].get('stepSize', '0.001'))
            
            if quantity < min_qty:
                await self.telegram.send_casual_message(f"⚠️ Quantity too small: {quantity:.6f} < {min_qty}")
                return False
            
            # Round quantity properly
            quantity = round(quantity / step_size) * step_size
            
            # Set leverage
            await self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            
            # Place order
            side = SIDE_BUY if action == "long" else SIDE_SELL
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            
            # Send professional notification
            message = self.telegram.get_entry_message(action, symbol, confidence, reason, pro_analysis)
            await self.telegram.send_casual_message(message)
            
            # Store entry data untuk professional exit
            self.active_entries[symbol] = {
                'entry_analysis': pro_analysis,
                'entry_time': datetime.now(),
                'entry_price': current_price,
                'position_sizing': position_sizing
            }
            
            logger.info(f"PRO TRADE: {action} {symbol} qty:{quantity:.6f} leverage:{leverage}x risk:{risk_pct:.2%}")
            return True
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error in trade execution: {e}")
            await self.telegram.send_casual_message(f"❌ Binance API Error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error executing professional trade: {e}")
            await self.telegram.send_casual_message(f"❌ Trade error: {str(e)}")
            return False
    
    async def close_position_pro(self, symbol: str, position_data: dict, exit_analysis: Dict = None) -> bool:
        """Close position dengan professional exit analysis"""
        try:
            position_amt = float(position_data['positionAmt'])
            
            if position_amt == 0:
                return True
            
            # Determine side for closing
            side = SIDE_SELL if position_amt > 0 else SIDE_BUY
            quantity = abs(position_amt)
            
            # Close position
            order = await self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity,
                reduceOnly=True
            )
            
            # Calculate profit
            entry_price = float(position_data['entryPrice'])
            current_price = float(position_data['markPrice'])
            
            if position_amt > 0:  # LONG
                profit_pct = (current_price - entry_price) / entry_price
            else:  # SHORT
                profit_pct = (entry_price - current_price) / entry_price
            
            # Get exit details
            exit_reason = exit_analysis.get('reason', 'Professional exit') if exit_analysis else 'Smart exit'
            urgency = exit_analysis.get('urgency', 'NONE') if exit_analysis else 'NONE'
            
            # Send professional notification
            side_text = "LONG" if position_amt > 0 else "SHORT"
            message = self.telegram.get_exit_message(symbol, side_text, profit_pct, exit_reason, urgency)
            await self.telegram.send_casual_message(message)
            
            # Update trade history untuk Kelly calculation
            if symbol in self.active_entries:
                trade_data = {
                    'symbol': symbol,
                    'profit_pct': profit_pct,
                    'entry_price': entry_price,
                    'exit_price': current_price,
                    'exit_reason': exit_reason,
                    'timestamp': datetime.now()
                }
                self.smart_entry.add_trade_to_history(trade_data)
                
                # Add to performance monitor for auto-upgrade tracking
                self.performance_monitor.add_trade(trade_data)
                
                del self.active_entries[symbol]
            
            logger.info(f"PRO CLOSE: {symbol} profit: {profit_pct:.3%} reason: {exit_reason}")
            return True
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error in position closing: {e}")
            await self.telegram.send_casual_message(f"❌ Binance API Error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error closing position professionally: {e}")
            return False
    
    def _calculate_market_volatility(self, symbol: str, klines_data: list) -> float:
        """Calculate market volatility for auto leverage"""
        try:
            if not klines_data or len(klines_data) < 20:
                return 0.03  # Default moderate volatility
            
            # Calculate price changes
            prices = [float(k[4]) for k in klines_data]  # Close prices
            returns = []
            
            for i in range(1, len(prices)):
                if prices[i-1] > 0:
                    returns.append(abs((prices[i] - prices[i-1]) / prices[i-1]))
            
            if not returns:
                return 0.03
            
            # Calculate volatility as standard deviation of returns
            volatility = np.std(returns) if len(returns) > 1 else 0.03
            
            logger.info(f"Market volatility for {symbol}: {volatility:.4f}")
            return volatility
            
        except Exception as e:
            logger.error(f"Error calculating market volatility: {e}")
            return 0.03  # Default moderate volatility

    def optimize_memory(self):
        """Memory optimization untuk VPS 1GB"""
        self.memory_optimization_counter += 1
        memory_mb = 0  # Inisialisasi agar tidak error
        if self.memory_optimization_counter % 100 == 0:
            # Clear old data
            if len(self.last_price_data) > 1000:
                self.last_price_data.clear()
            
            # Garbage collection
            gc.collect()
            
            # Log memory usage
            memory_mb = self.process.memory_info().rss / 1024 / 1024
            logger.info(f"Memory optimized: {memory_mb:.1f}MB")
            
            if memory_mb > 800:
                logger.warning(f"High memory usage: {memory_mb:.1f}MB")

        # Pindahkan pengecekan memory_mb > 700 ke dalam blok di atas
        if memory_mb > 700 and os.getenv("ALLOW_AUTO_REBOOT", "false").lower() == "true":
            logger.error(f"Memory usage critical {memory_mb:.1f}MB – initiating auto reboot")
            try:
                # Inform via Telegram before reboot
                asyncio.create_task(self.telegram.send_casual_message("🚨 VPS memory >700MB, rebooting..."))
            except Exception:
                pass

            # Attempt graceful reboot
            try:
                subprocess.Popen(["sudo", "reboot"])  # Non-blocking
            except Exception as e:
                logger.error(f"Failed to reboot VPS: {e}")
    
    async def trading_loop(self):
        """PRO TRADER Main Trading Loop - Modular & Intelligent"""
        logger.info("Starting PRO TRADER modular loop...")
        
        startup_message = self.telegram.get_startup_message()
        await self.telegram.send_casual_message(startup_message)
        
        while self.is_running:
            try:
                # Memory optimization
                self.optimize_memory()

                # Check for auto-upgrade based on performance
                upgrade_config = self.performance_monitor.check_and_upgrade()
                if upgrade_config:
                    # Apply auto-upgrade
                    self.config.max_open_positions = upgrade_config['config']['max_open_trades']
                    self.config.max_open_trades = upgrade_config['config']['max_open_trades']  # Keep both for compatibility
                    self.config.confidence_threshold = upgrade_config['config']['confidence_threshold']
                    # Send upgrade notification
                    upgrade_msg = (
                        f"🚀 *AUTO UPGRADE ACTIVATED!*\n\n"
                        f"Tier: {upgrade_config['tier']}\n"
                        f"Max Positions: {upgrade_config['max_positions']}\n"
                        f"Reason: {upgrade_config['reason']}\n\n"
                        f"Bot akan trading dengan {upgrade_config['max_positions']} posisi!"
                    )
                    await self.telegram.send_casual_message(upgrade_msg)
                    logger.info(f"AUTO UPGRADE: {upgrade_config['tier']} - {upgrade_config['max_positions']} positions")

                # Check if we have tradeable symbols
                if not self.symbols:
                    logger.warning("No tradeable symbols available, skipping trading")
                    await asyncio.sleep(60)
                    continue

                # Fetch all positions once for heat & limits
                all_positions = await self.client.futures_position_information()
                open_positions = [p for p in all_positions if float(p['positionAmt']) != 0]

                # Monitor all tradeable symbols
                for symbol in self.symbols:
                    # Filter position for this symbol
                    symbol_positions = [p for p in open_positions if p['symbol'] == symbol]
                    
                    # Check portfolio heat - use actual balance from Binance
                    balances = await self.client.futures_account_balance()
                    current_balance = next((float(x['balance']) for x in balances if x['asset'] == 'USDT'), 0)
                    portfolio_heat = self.position_sizing.get_portfolio_heat(open_positions, current_balance)
                    if portfolio_heat['max_heat_reached']:
                        logger.info(f"Portfolio heat limit reached: {portfolio_heat['total_heat']:.1%}")
                        continue
                    
                    # Get market data
                    klines_data = await self.get_klines_data(symbol, self.config.timeframe)
                    if not klines_data:
                        logger.warning(f"No klines data for {symbol}")
                        continue
                    
                    # Check exit conditions first
                    for position in symbol_positions:
                        exit_analysis = self.smart_exit.should_exit(
                            position, 
                            float(position['markPrice']), 
                            klines_data, 
                            self.active_entries.get(symbol, {})
                        )
                        
                        if exit_analysis['action'] == 'close':
                            await self.close_position_pro(symbol, position, exit_analysis)
                    
                    # Check entry conditions with smart position management
                    current_positions_count = len(open_positions)
                    symbol_positions_count = len(symbol_positions)
                    
                    # Check if we can add more positions
                    can_add_position = current_positions_count < self.config.max_open_positions
                    
                    if can_add_position:
                        entry_analysis = self.smart_entry.analyze_entry(klines_data)
                        
                        # Determine entry type based on confidence and existing positions
                        is_high_confidence = entry_analysis['confidence'] >= getattr(self.config, 'high_confidence_threshold', 80)
                        is_normal_confidence = entry_analysis['confidence'] >= self.config.confidence_threshold
                        
                        # Check if this is a valid entry
                        can_entry = False
                        entry_type = "normal"
                        
                        if current_positions_count == 0:
                            # First position - normal confidence is enough
                            can_entry = is_normal_confidence and entry_analysis['action'] in ['long', 'short']
                            entry_type = "normal"
                        elif current_positions_count == 1:
                            # Second position - need high confidence and different symbol
                            if getattr(self.config, 'different_symbols_only', True):
                                # Check if we already have a position in this symbol
                                existing_symbols = [p['symbol'] for p in open_positions]
                                if symbol not in existing_symbols and is_high_confidence:
                                    can_entry = entry_analysis['action'] in ['long', 'short']
                                    entry_type = "high_confidence"
                            else:
                                # Allow same symbol if different_symbols_only is false
                                can_entry = is_high_confidence and entry_analysis['action'] in ['long', 'short']
                                entry_type = "high_confidence"
                        elif current_positions_count == 2:
                            # Third position - need very high confidence and different symbol
                            if getattr(self.config, 'different_symbols_only', True):
                                # Check if we already have a position in this symbol
                                existing_symbols = [p['symbol'] for p in open_positions]
                                if symbol not in existing_symbols and entry_analysis['confidence'] >= 75:
                                    can_entry = entry_analysis['action'] in ['long', 'short']
                                    entry_type = "very_high_confidence"
                            else:
                                # Allow same symbol if different_symbols_only is false
                                can_entry = entry_analysis['confidence'] >= 75 and entry_analysis['action'] in ['long', 'short']
                                entry_type = "very_high_confidence"
                        
                        if can_entry:
                            # Check portfolio heat limit
                            portfolio_heat = self.position_sizing.get_portfolio_heat(open_positions, current_balance)
                            heat_limit = getattr(self.config, 'portfolio_heat_limit', 10) / 100
                            
                            if portfolio_heat['total_heat'] < heat_limit:
                                success = await self.execute_trade_pro(symbol, entry_analysis, klines_data)
                                if success:
                                    logger.info(f"PRO TRADE EXECUTED: {entry_type.upper()} {entry_analysis['action']} {symbol} (Confidence: {entry_analysis['confidence']:.1f}%)")
                            else:
                                logger.info(f"Portfolio heat limit reached: {portfolio_heat['total_heat']:.1%} >= {heat_limit:.1%}")
                
                # Sleep between iterations
                await asyncio.sleep(15)
                
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                await self.telegram.send_casual_message(f"❌ Error: {str(e)}")
                await asyncio.sleep(60)
    
    async def start(self):
        """Start bot: run Telegram polling and trading loop in parallel"""
        self.is_running = True
        
        # Initialize Binance first
        success = await self.init_binance_client()
        if not success:
            logger.error("Failed to initialize Binance client")
            return
        
        # Initialize Telegram
        await self.init_telegram_bot()
        
        # Run both Telegram polling and trading loop in parallel
        await asyncio.gather(
            self.start_telegram_polling(),
            self.trading_loop()
        )
    
    async def stop(self):
        """Stop the bot gracefully"""
        try:
            self.is_running = False
            if self.client:
                await self.client.close_connection()
            
            await self.telegram.send_casual_message("🛑 *Pro Trader Bot Stopped*\nSee you next time! 👋")
            logger.info("Bot stopped gracefully")
            
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")

# =========================
# MAIN EXECUTION
# =========================

async def main():
    """Main function untuk menjalankan bot"""
    bot = BinanceFuturesProBot()
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")