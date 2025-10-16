# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ..widgets import StyledButton
from ..theme import Theme

class AdventurePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_accessibility()

    def setup_accessibility(self):
        """Set up accessibility features for the adventure page"""
        self.setAccessibleName("Adventure Page")
        self.setAccessibleDescription("Main adventure interface for exploring and resting")

        # Set accessibility names for buttons
        self.explore_btn.setAccessibleName("Explore wilderness button")
        self.explore_btn.setAccessibleDescription("Venture into the wilderness to find enemies and treasures")

        self.rest_btn.setAccessibleName("Rest button")
        self.rest_btn.setAccessibleDescription("Rest to restore all health points")

        self.quit_btn.setAccessibleName("Quit game button")
        self.quit_btn.setAccessibleDescription("Exit the game")

        # Enable keyboard navigation
        self.setFocusPolicy(Qt.StrongFocus)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Theme.MARGIN_XL, Theme.MARGIN_XL, Theme.MARGIN_XL, Theme.MARGIN_XL)
        layout.setSpacing(Theme.SPACING_LG)
        layout.setAlignment(Qt.AlignCenter)

        # Title section
        title_label = QLabel("Adventure awaits...")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {Theme.FOREGROUND.name()}; margin-bottom: {Theme.SPACING_MD}px;")
        title_label.setAccessibleName("Page Title")
        title_label.setAccessibleDescription("Adventure page header")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Button container for better layout
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(Theme.SPACING_MD)
        button_layout.setAlignment(Qt.AlignCenter)

        # Action buttons with improved styling and accessibility
        self.explore_btn = StyledButton("🏞️ Explore", variant="primary", size="lg")
        self.explore_btn.setMinimumHeight(60)
        self.explore_btn.setToolTip("Venture into the wilderness to find enemies and treasures (E)")

        self.rest_btn = StyledButton("😴 Rest", variant="secondary", size="lg")
        self.rest_btn.setMinimumHeight(60)
        self.rest_btn.setToolTip("Rest to restore all health points (T)")

        self.quit_btn = StyledButton("🚪 Quit Game", variant="destructive", size="lg")
        self.quit_btn.setMinimumHeight(60)
        self.quit_btn.setToolTip("Exit the game (Ctrl+Q)")

        button_layout.addWidget(self.explore_btn)
        button_layout.addWidget(self.rest_btn)
        button_layout.addWidget(self.quit_btn)

        layout.addWidget(button_container)

        # Create the grid layout for potential future use (keyboard shortcuts display)
        self.button_layout = QGridLayout()
        self.button_layout.addWidget(button_container, 0, 0, 1, 2)
