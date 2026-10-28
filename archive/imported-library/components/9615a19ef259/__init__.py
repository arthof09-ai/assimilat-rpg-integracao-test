"""VLAB gateway R04 experimental reference implementation.

IMPORTANT: Controls only its own SQLite simulated write sink. It has no
Notion permissions, cannot allocate a live CM-000006-I0001, and cannot fence
older clients with direct Notion access. Never mistake local PASS for GREEN.
"""
from .core import Gateway, Rejected, UncertainEffect, DOMAIN

__all__ = ['Gateway', 'Rejected', 'UncertainEffect', 'DOMAIN']
