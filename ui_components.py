"""
UI Components for PyRPG - Modern interface elements
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QGridLayout, QFrame, QScrollArea, QSizePolicy, QLineEdit)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor


class ItemCard(QFrame):
    """A card widget displaying an item with visual flair"""
    clicked = Signal(object)  # Emits the item when clicked
    action_clicked = Signal(object, str)  # Emits (item, action) e.g., ("item", "buy")

    def __init__(self, item, action_text="Select", show_price=False, parent=None):
        super().__init__(parent)
        self.item = item
        self.action_text = action_text
        self.show_price = show_price

        self.setup_ui()

    def setup_ui(self):
        """Setup the card UI"""
        self.setFrameShape(QFrame.Box)
        self.setMinimumSize(180, 200)
        self.setMaximumSize(200, 220)

        # Styling based on rarity
        rarity_colors = {
            'common': '#abb2bf',
            'uncommon': '#98c379',
            'rare': '#61afef',
            'epic': '#c678dd',
            'legendary': '#e5c07b'
        }

        border_color = rarity_colors.get(self.item.rarity, '#abb2bf')

        self.setStyleSheet(f"""
            ItemCard {{
                background-color: #21252b;
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 10px;
            }}
            ItemCard:hover {{
                background-color: #282c34;
                border-color: {border_color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Item icon/emoji
        icon_label = QLabel(self.get_item_icon())
        icon_label.setStyleSheet("font-size: 32px; border: none;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Item name
        name_label = QLabel(self.item.name)
        name_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 600;
            color: {border_color};
            border: none;
        """)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)

        # Item stats/description
        stats_text = self.get_stats_text()
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet("""
            font-size: 11px;
            color: #abb2bf;
            border: none;
        """)
        stats_label.setAlignment(Qt.AlignCenter)
        stats_label.setWordWrap(True)
        layout.addWidget(stats_label)

        # Rarity badge
        rarity_label = QLabel(self.item.rarity.title())
        rarity_label.setStyleSheet(f"""
            font-size: 10px;
            color: {border_color};
            background-color: rgba(0, 0, 0, 0.3);
            padding: 3px 8px;
            border-radius: 3px;
            border: none;
        """)
        rarity_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(rarity_label)

        layout.addStretch()

        # Price/Value
        if self.show_price:
            price_label = QLabel(f"{self.item.value} gold")
            price_label.setStyleSheet("""
                font-size: 12px;
                font-weight: 600;
                color: #e5c07b;
                border: none;
            """)
            price_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(price_label)

        # Action button
        action_btn = QPushButton(self.action_text)
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                color: #61afef;
                border: 1px solid #61afef;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)
        action_btn.clicked.connect(lambda: self.action_clicked.emit(self.item, self.action_text.lower()))
        layout.addWidget(action_btn)

        self.setCursor(Qt.PointingHandCursor)

    def get_item_icon(self):
        """Get emoji icon for item type"""
        icons = {
            'weapon': '⚔️',
            'armor': '🛡️',
            'accessory': '💍',
            'consumable': '🧪'
        }
        return icons.get(self.item.item_type, '📦')

    def get_stats_text(self):
        """Get stats text for the item"""
        stats = []
        if self.item.attack_bonus > 0:
            stats.append(f"+{self.item.attack_bonus} ATK")
        if self.item.defense_bonus > 0:
            stats.append(f"+{self.item.defense_bonus} DEF")
        if self.item.effect:
            if self.item.effect == 'heal':
                stats.append(f"Heals {self.item.power} HP")
            elif self.item.effect == 'restore_mana':
                stats.append(f"Restores {self.item.power} MP")

        return " | ".join(stats) if stats else self.item.description[:30] if self.item.description else "No special stats"

    def mousePressEvent(self, event):
        """Handle mouse press for card selection"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.item)
        super().mousePressEvent(event)


class ItemSelectionOverlay(QWidget):
    """Modal overlay for selecting items from inventory"""
    item_selected = Signal(object)  # Emits selected item
    closed = Signal()  # Emits when overlay is closed

    def __init__(self, items, title="Select Item", action_text="Use", show_price=False, parent=None):
        super().__init__(parent)
        self.items = items
        self.title = title
        self.action_text = action_text
        self.show_price = show_price

        # Make overlay fill parent
        if parent:
            self.setGeometry(parent.rect())

        self.setup_ui()
        self.animate_in()

    def setup_ui(self):
        """Setup overlay UI"""
        # Semi-transparent background
        self.setStyleSheet("""
            ItemSelectionOverlay {
                background-color: rgba(0, 0, 0, 180);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setAlignment(Qt.AlignCenter)

        # Content panel
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #282c34;
                border: 2px solid #61afef;
                border-radius: 12px;
            }
        """)
        panel.setMaximumSize(900, 600)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(15)

        # Title bar with close button
        title_layout = QHBoxLayout()
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #61afef;
        """)
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e06c75;
                border: none;
                font-size: 24px;
                font-weight: bold;
                padding: 0;
                min-width: 30px;
                min-height: 30px;
            }
            QPushButton:hover {
                color: #ff6b6b;
            }
        """)
        close_btn.clicked.connect(self.close_overlay)
        title_layout.addWidget(close_btn)

        panel_layout.addLayout(title_layout)

        # Scroll area for items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #21252b;
                border-radius: 8px;
            }
        """)

        # Grid of item cards
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)
        grid_layout.setSpacing(15)

        # Create item cards
        if not self.items:
            no_items_label = QLabel("No items available")
            no_items_label.setStyleSheet("""
                font-size: 14px;
                color: #abb2bf;
                padding: 40px;
            """)
            no_items_label.setAlignment(Qt.AlignCenter)
            grid_layout.addWidget(no_items_label, 0, 0)
        else:
            row = 0
            col = 0
            max_cols = 4

            for item in self.items:
                card = ItemCard(item, self.action_text, self.show_price)
                card.action_clicked.connect(self.on_item_action)
                grid_layout.addWidget(card, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

        scroll.setWidget(scroll_widget)
        panel_layout.addWidget(scroll)

        layout.addWidget(panel)

    def on_item_action(self, item, action):
        """Handle item action button click"""
        self.item_selected.emit(item)
        self.close_overlay()

    def close_overlay(self):
        """Close the overlay with animation"""
        self.animate_out()

    def animate_in(self):
        """Animate overlay appearing"""
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def animate_out(self):
        """Animate overlay disappearing"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(150)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.deleteLater)
        self.animation.finished.connect(self.closed.emit)
        self.animation.start()

    def mousePressEvent(self, event):
        """Close overlay when clicking outside the panel"""
        # Check if click is on the background (not the panel)
        child = self.childAt(event.pos())
        if child == self or child is None:
            self.close_overlay()
        super().mousePressEvent(event)


class CharacterCreationOverlay(QWidget):
    """Overlay for character creation"""
    character_created = Signal(str)  # Emits hero name

    def __init__(self, parent=None):
        super().__init__(parent)

        if parent:
            self.setGeometry(parent.rect())

        self.setup_ui()
        self.animate_in()

    def setup_ui(self):
        """Setup character creation UI"""
        self.setStyleSheet("""
            CharacterCreationOverlay {
                background-color: rgba(0, 0, 0, 180);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Content panel
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #282c34;
                border: 2px solid #61afef;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        panel.setMaximumSize(500, 300)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(20)

        # Title
        title = QLabel("⚔️ Create Your Hero ⚔️")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #61afef;
        """)
        title.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(title)

        # Name input
        name_label = QLabel("Enter your hero's name:")
        name_label.setStyleSheet("font-size: 14px; color: #abb2bf;")
        panel_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Hero")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #21252b;
                color: #abb2bf;
                border: 1px solid #3e4452;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #61afef;
            }
        """)
        self.name_input.returnPressed.connect(self.create_character)
        panel_layout.addWidget(self.name_input)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        create_btn = QPushButton("Create Hero")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                color: #61afef;
                border: 2px solid #61afef;
                border-radius: 6px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)
        create_btn.clicked.connect(self.create_character)
        button_layout.addWidget(create_btn)

        button_layout.addStretch()
        panel_layout.addLayout(button_layout)

        layout.addWidget(panel)

        # Focus the input
        self.name_input.setFocus()

    def create_character(self):
        """Emit character name and close"""
        name = self.name_input.text().strip()
        if not name:
            name = "Hero"

        self.character_created.emit(name)
        self.animate_out()

    def animate_in(self):
        """Animate overlay appearing"""
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def animate_out(self):
        """Animate overlay disappearing"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(150)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()
