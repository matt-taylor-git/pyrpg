# -*- coding: utf-8 -*-
"""
Centralized theme definitions for the PyRPG application.
Colors are derived from the React sample UI's dark theme.
"""
from PySide6.QtGui import QColor

class Theme:
    """Holds the color palette and font definitions for the application."""
    # Color Palette (from OKLCH in globals.css, converted to HEX)
    BACKGROUND = QColor("#1a1826")
    FOREGROUND = QColor("#f1f0f2")
    CARD = QColor("#221e30")
    CARD_FOREGROUND = QColor("#f1f0f2")

    PRIMARY = QColor("#dc3545")  # Crimson Red
    PRIMARY_FOREGROUND = QColor("#f9f8fa")

    SECONDARY = QColor("#352e4d")
    SECONDARY_FOREGROUND = QColor("#f1f0f2")

    MUTED = QColor("#2d283d")
    MUTED_FOREGROUND = QColor("#9a96a5")

    ACCENT = QColor("#8c52ff")
    ACCENT_FOREGROUND = QColor("#f1f0f2")

    DESTRUCTIVE = QColor("#d23a1a")
    DESTRUCTIVE_FOREGROUND = QColor("#f1f0f2")

    BORDER = QColor("#3e3754")
    INPUT = QColor("#3e3754")
    RING = QColor("#dc3545")

    # Standard Spacing Values (in pixels)
    SPACING_XS = 4      # Extra small spacing
    SPACING_SM = 8      # Small spacing (small buttons, tight spacing)
    SPACING_MD = 15     # Medium spacing (default content margins)
    SPACING_LG = 20     # Large spacing (standard container margins)
    SPACING_XL = 30     # Extra large spacing

    # Standard Margin Values
    MARGIN_XS = 5       # Extra small margins
    MARGIN_SM = 8       # Small margins
    MARGIN_MD = 15      # Medium margins (cards, groups)
    MARGIN_LG = 20      # Large margins (main containers)
    MARGIN_XL = 50      # Extra large margins (page containers)

    # Fonts
    FONT_FAMILY = "Inter, Segoe UI, sans-serif"
