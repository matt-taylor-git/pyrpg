# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton)
from PySide6.QtCore import Qt
from ..widgets import StyledButton
from ..theme import Theme

class AdventurePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Theme.MARGIN_XL, Theme.MARGIN_XL, Theme.MARGIN_XL, Theme.MARGIN_XL)
        layout.setSpacing(Theme.SPACING_LG)
        layout.setAlignment(Qt.AlignCenter)

        # Action buttons
        self.explore_btn = StyledButton("Explore", variant="primary", size="lg")
        self.explore_btn.setMinimumHeight(60)
        
        self.rest_btn = StyledButton("Rest", variant="secondary", size="lg")
        self.rest_btn.setMinimumHeight(60)

        self.quit_btn = StyledButton("Quit Game", variant="destructive", size="lg")
        self.quit_btn.setMinimumHeight(60)

        layout.addWidget(self.explore_btn)
        layout.addWidget(self.rest_btn)
        layout.addWidget(self.quit_btn)
