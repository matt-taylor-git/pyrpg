# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGridLayout
from PySide6.QtCore import Qt

class InventoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with title and gold
        header_layout = QHBoxLayout()

        title = QLabel("\U0001f392 Inventory")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #61afef;
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.inventory_gold_label = QLabel("\U0001f4b0 Gold: 0")
        self.inventory_gold_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #e5c07b;
            background-color: #21252b;
            padding: 8px 15px;
            border-radius: 6px;
            border: 1px solid #3e4452;
        """)
        header_layout.addWidget(self.inventory_gold_label)

        layout.addLayout(header_layout)

        # Scroll area for inventory grid
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
        self.inventory_grid_layout = QGridLayout(scroll_widget)
        self.inventory_grid_layout.setSpacing(15)
        self.inventory_grid_layout.setContentsMargins(15, 15, 15, 15)

        # Empty state label
        self.inventory_empty_label = QLabel("No items in inventory\n\nDefeat enemies and visit the shop to collect items!")
        self.inventory_empty_label.setStyleSheet("""
            font-size: 14px;
            color: #abb2bf;
            padding: 40px;
        """)
        self.inventory_empty_label.setAlignment(Qt.AlignCenter)
        self.inventory_grid_layout.addWidget(self.inventory_empty_label, 0, 0, Qt.AlignCenter)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)