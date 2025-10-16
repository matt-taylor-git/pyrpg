# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGridLayout
from PySide6.QtCore import Qt
from ..widgets import Card
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

class InventoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        main_layout.setSpacing(Theme.SPACING_LG)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Inventory")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.gold_label = QLabel("Gold: 0")
        self.gold_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e5c07b;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.gold_label)
        main_layout.addLayout(header_layout)

        # Inventory Grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.inventory_grid_layout = QGridLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def update_inventory(self, hero):
        if not hero:
            return

        self.gold_label.setText(f"Gold: {hero.gold}")

        # Clear existing items properly
        clear_layout(self.inventory_grid_layout)

        if not hero.inventory:
            empty_label = QLabel("Your inventory is empty.")
            empty_label.setAlignment(Qt.AlignCenter)
            self.inventory_grid_layout.addWidget(empty_label, 0, 0, 1, 4)
            return

        row, col = 0, 0
        for item in hero.inventory:
            action = "Use" if item.item_type == 'consumable' else "Equip"
            item_card = ItemCard(item, action_text=action, show_price=False)
            # item_card.action_clicked.connect(self.on_item_action) # Connect this in main_window
            self.inventory_grid_layout.addWidget(item_card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1
