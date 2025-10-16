# -*- coding: utf-8 -*-
"""
Custom, reusable UI widgets for the PyRPG application, styled to match the
modern look and feel of the React reference UI.
"""
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QProgressBar, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal
from .theme import Theme

class Card(QFrame):
    """A customizable card widget, serving as a base container for UI sections."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            Card {{
                background-color: {Theme.CARD.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 8px;
            }}
            Card:hover {{
                background-color: {Theme.MUTED.name()};
            }}
        """)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        self.main_layout.setSpacing(Theme.SPACING_MD)

    def setLayout(self, layout):
        # This is a convenience method to allow setting the layout directly on the card
        # while preserving the main_layout that holds the styling.
        content_widget = QWidget()
        content_widget.setLayout(layout)
        self.main_layout.addWidget(content_widget)

class StyledButton(QPushButton):
    """A button with variants for different actions (primary, destructive, etc.)."""
    def __init__(self, text, variant="default", size="default", parent=None):
        super().__init__(text, parent)
        self.set_variant(variant)
        self.set_size(size)
        self.setCursor(Qt.PointingHandCursor)

    def set_variant(self, variant):
        """Sets the button's visual style (e.g., 'primary', 'destructive')."""
        self.setObjectName(variant)  # Use object name for QSS targeting

    def enterEvent(self, event):
        """Handle mouse entering button for enhanced hover effects"""
        super().enterEvent(event)
        # You can add custom hover animations here in the future

    def leaveEvent(self, event):
        """Handle mouse leaving button"""
        super().leaveEvent(event)
        # Reset any hover effects here in the future

    def set_size(self, size):
        """Sets the button's padding and font size."""
        if size == "sm":
            self.setStyleSheet("padding: 5px 10px; font-size: 12px;")
        elif size == "lg":
            self.setStyleSheet("padding: 12px 24px; font-size: 16px;")
        else: # default
            self.setStyleSheet("padding: 8px 16px; font-size: 14px;")


class Badge(QLabel):
    """A small label for displaying status or rarity."""
    def __init__(self, text, variant="default", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.set_variant(variant)

    def set_variant(self, variant):
        """Sets the badge's color scheme."""
        color_map = {
            "common": (Theme.MUTED, Theme.MUTED_FOREGROUND),
            "rare": (Theme.ACCENT, Theme.ACCENT_FOREGROUND),
            "epic": (Theme.PRIMARY, Theme.PRIMARY_FOREGROUND),
            "legendary": (Theme.PRIMARY, Theme.PRIMARY_FOREGROUND), # Same as epic for now
            "default": (Theme.SECONDARY, Theme.SECONDARY_FOREGROUND)
        }
        bg_color, fg_color = color_map.get(variant, color_map["default"])

        self.setStyleSheet(f"""
            Badge {{
                background-color: {bg_color.name()};
                color: {fg_color.name()};
                border-radius: 10px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)

class StyledProgressBar(QProgressBar):
    """A progress bar styled to match the React UI's aesthetic."""
    def __init__(self, variant="health", parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setTextVisible(True)
        self.set_variant(variant)

    def set_variant(self, variant):
        """Sets the color of the progress bar chunk."""
        chunk_color = Theme.PRIMARY.name()
        if variant == "mana":
            chunk_color = Theme.ACCENT.name()
        elif variant == "experience":
            chunk_color = Theme.MUTED_FOREGROUND.name()

        self.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 12px;
                background-color: {Theme.MUTED.name()};
                color: {Theme.FOREGROUND.name()};
                height: 24px;
            }}
            QProgressBar::chunk {{
                background-color: {chunk_color};
                border-radius: 7px;
            }}
        """)
