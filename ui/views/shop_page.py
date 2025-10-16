# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGridLayout, QPushButton
from PySide6.QtCore import Qt
from ..widgets import Card, StyledButton
from ..theme import Theme
from ui_components import ItemCard


def clear_layout(layout):
    """Clear all widgets from a layout"""
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

class ShopPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_cards = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        main_layout.setSpacing(Theme.SPACING_LG)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Merchant Shop")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.gold_label = QLabel("Gold: 0")
        self.gold_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e5c07b;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.gold_label)
        main_layout.addLayout(header_layout)

        # Shop Grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.shop_grid_layout = QGridLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Bottom Buttons
        button_layout = QHBoxLayout()
        self.sell_btn = StyledButton("Sell Items", variant="secondary")
        self.leave_btn = StyledButton("Leave Shop", variant="destructive")
        button_layout.addStretch()
        button_layout.addWidget(self.sell_btn)
        button_layout.addWidget(self.leave_btn)
        main_layout.addLayout(button_layout)

    def update_shop(self, hero, shop_items):
        if not hero:
            return

        self.gold_label.setText(f"Gold: {hero.gold}")

        # Clear existing items properly
        clear_layout(self.shop_grid_layout)
        self.item_cards.clear()

        row, col = 0, 0
        for item_name, item in shop_items.items():
            item_card = ItemCard(item, action_text="Buy", show_price=True)
            self.item_cards.append(item_card)
            self.shop_grid_layout.addWidget(item_card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
