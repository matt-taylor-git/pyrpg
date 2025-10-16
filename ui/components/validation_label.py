# -*- coding: utf-8 -*-
"""
Validation label component for inline error/success feedback
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from ..theme import Theme


class ValidationLabel(QLabel):
    """Label that displays validation feedback with appropriate styling"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setWordWrap(True)
        self.clear_validation()

    def show_error(self, message):
        """Show error feedback"""
        self.setText(f"❌ {message}")
        self.setStyleSheet(f"""
            color: {Theme.DESTRUCTIVE.name()};
            font-size: {Theme.FONT_SIZE_SM}px;
            background-color: rgba(210, 58, 26, 0.1);
            padding: {Theme.SPACING_XS}px;
            border-radius: {Theme.BORDER_RADIUS_SM}px;
            border: 1px solid {Theme.DESTRUCTIVE.name()};
        """)
        self.show()

    def show_success(self, message):
        """Show success feedback"""
        self.setText(f"✓ {message}")
        self.setStyleSheet(f"""
            color: #28a745;
            font-size: {Theme.FONT_SIZE_SM}px;
            background-color: rgba(40, 167, 69, 0.1);
            padding: {Theme.SPACING_XS}px;
            border-radius: {Theme.BORDER_RADIUS_SM}px;
            border: 1px solid #28a745;
        """)
        self.show()

    def show_warning(self, message):
        """Show warning feedback"""
        self.setText(f"⚠️ {message}")
        self.setStyleSheet(f"""
            color: #ffc107;
            font-size: {Theme.FONT_SIZE_SM}px;
            background-color: rgba(255, 193, 7, 0.1);
            padding: {Theme.SPACING_XS}px;
            border-radius: {Theme.BORDER_RADIUS_SM}px;
            border: 1px solid #ffc107;
        """)
        self.show()

    def clear_validation(self):
        """Clear and hide validation feedback"""
        self.setText("")
        self.hide()
