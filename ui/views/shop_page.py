# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGridLayout, QPushButton
from PySide6.QtCore import Qt
from ui_components import ItemCard
from game.game import get_shop_items

class ShopPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_cards = []  # Store item cards for later connection
        self.sell_btn = None
        self.leave_btn = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with title and gold
        header_layout = QHBoxLayout()

        title = QLabel("\U0001f3ea Merchant's Emporium")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #e5c07b;
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.shop_gold_label = QLabel("\U0001f4b0 Gold: 0")
        self.shop_gold_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #e5c07b;
            background-color: #21252b;
            padding: 8px 15px;
            border-radius: 6px;
            border: 1px solid #3e4452;
        """)
        header_layout.addWidget(self.shop_gold_label)

        layout.addLayout(header_layout)

        # Welcome message
        welcome = QLabel("Welcome, traveler! Browse my finest wares!")
        welcome.setStyleSheet("""
            font-size: 14px;
            color: #abb2bf;
            padding: 10px;
            background-color: #21252b;
            border-radius: 6px;
            border: 1px solid #3e4452;
        """)
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)

        # Scroll area for shop items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #21252b;
                border-radius: 8px;
            }
        """)

        scroll_widget = QWidget()
        shop_grid = QGridLayout(scroll_widget)
        shop_grid.setSpacing(15)
        shop_grid.setContentsMargins(15, 15, 15, 15)

        # Get shop items and create cards
        shop_items = get_shop_items()
        row = 0
        col = 0
        max_cols = 4

        for item_name, item in shop_items.items():
            card = ItemCard(item, action_text="Buy", show_price=True)
            self.item_cards.append(card)  # Store for later connection
            shop_grid.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        shop_grid.setRowStretch(row + 1, 1)  # Add stretch at the bottom

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.sell_btn = QPushButton("\U0001f4b0 Sell Items")
        self.sell_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                color: #98c379;
                border: 1px solid #98c379;
                padding: 10px 25px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3e4452;
            }
        """)
        self.sell_btn.setMinimumHeight(45)

        self.leave_btn = QPushButton("\U0001f6aa Leave Shop")
        self.leave_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                color: #abb2bf;
                border: 1px solid #3e4452;
                padding: 10px 25px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3e4452;
            }
        """)
        self.leave_btn.setMinimumHeight(45)

        button_layout.addWidget(self.sell_btn)
        button_layout.addWidget(self.leave_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)