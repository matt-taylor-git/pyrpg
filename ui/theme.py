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
    MARGIN_XS = 4       # Extra small margins (tight layouts)
    MARGIN_SM = 8       # Small margins (control spacing)
    MARGIN_MD = 15      # Medium margins (cards, groups)
    MARGIN_LG = 20      # Large margins (main containers)
    MARGIN_XL = 30      # Extra large margins (page containers)

    # Layout Policy Factors (responsive sizing)
    SIZE_FACTOR_XS = 0.6    # 60% of standard size
    SIZE_FACTOR_SM = 0.8    # 80% of standard size
    SIZE_FACTOR_MD = 1.0    # Standard size (100%)
    SIZE_FACTOR_LG = 1.2    # 120% of standard size
    SIZE_FACTOR_XL = 1.5    # 150% of standard size

    # Widget Size Constraints
    MIN_BUTTON_WIDTH = 80     # Minimum button width
    MIN_BUTTON_HEIGHT = 32    # Minimum button height
    PREFERRED_BUTTON_WIDTH = 120  # Preferred button width
    PREFERRED_BUTTON_HEIGHT = 40  # Preferred button height

    MAX_CARD_WIDTH = 300      # Maximum card width
    MIN_CARD_HEIGHT = 150     # Minimum card height

    SCROLLBAR_WIDTH = 12      # Standard scrollbar width

    # Border and Radius Standards
    BORDER_RADIUS_SM = 4      # Small border radius (buttons, inputs)
    BORDER_RADIUS_MD = 6      # Medium border radius (cards, dialogs)
    BORDER_RADIUS_LG = 8      # Large border radius (panels, windows)
    BORDER_RADIUS_XL = 12     # Extra large border radius (overlays)

    BORDER_WIDTH_THIN = 1         # Thin borders
    BORDER_WIDTH_MEDIUM = 2       # Medium borders (cards, focus)
    BORDER_WIDTH_THICK = 3        # Thick borders (accents, selections)

    # Fonts and Typography
    FONT_FAMILY = "Inter, Segoe UI, sans-serif"
    FONT_SIZE_XS = 10         # Extra small (labels, badges)
    FONT_SIZE_SM = 12         # Small (secondary text)
    FONT_SIZE_MD = 14         # Medium (body text, buttons)
    FONT_SIZE_LG = 16         # Large (headers, important buttons)
    FONT_SIZE_XL = 18         # Extra large (titles)
    FONT_SIZE_XXL = 24        # Double extra large (main titles)
    FONT_SIZE_XXXL = 36       # Triple extra large (hero titles)

    FONT_WEIGHT_NORMAL = 400    # Normal weight
    FONT_WEIGHT_MEDIUM = 500    # Medium weight (buttons, emphasis)
    FONT_WEIGHT_SEMIBOLD = 600  # Semibold (headers)
    FONT_WEIGHT_BOLD = 700      # Bold (strong emphasis)

    # Animation Standards
    ANIMATION_DURATION_FAST = 150    # Fast animations (150ms)
    ANIMATION_DURATION_NORMAL = 300  # Normal animations (300ms)
    ANIMATION_DURATION_SLOW = 500    # Slow animations (500ms)

    # Z-Index Layers (for stacking context)
    Z_LAYER_BASE = 0         # Base content layer
    Z_LAYER_OVERLAY = 10     # Modal overlays, tooltips
    Z_LAYER_POPUP = 20       # Dropdowns, context menus
    Z_LAYER_MODAL = 30       # Modal dialogs
    Z_LAYER_TOAST = 40       # Toast notifications
