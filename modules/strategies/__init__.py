"""Strategies sub‑package.

For now, re‑export `SmartEntry` and `SmartExit` from the existing
`modules.smart_trading` module so current logic keeps working.
New strategies can live in this folder.
"""
from ..smart_trading import SmartEntry, SmartExit

__all__ = ["SmartEntry", "SmartExit"]
