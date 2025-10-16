# -*- coding: utf-8 -*-
"""
UI Components for PyRPG - Modern interface elements
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QGridLayout, QFrame, QScrollArea, QSizePolicy, QLineEdit, QDialog)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor, QPixmap
import os
from game.items import Item


class ItemCard(QFrame):
    """A card widget displaying an item with visual flair"""
    clicked = Signal(object)  # Emits the item when clicked
    action_clicked = Signal(object, str)  # Emits (item, action) e.g., ("item", "buy")

    def __init__(self, item, action_text="Select", show_price=False, parent=None):
        super().__init__(parent)
        self.item = item
        self.action_text = action_text
        self.show_price = show_price
        self.is_selected = False

        self.setup_ui()
        self.setup_drag_drop()

    def setup_ui(self):
        """Setup the card UI with Theme constants"""
        self.setFrameShape(QFrame.Box)
        self.setMinimumSize(180, 200)
        self.setMaximumSize(200, 220)

        # Styling based on rarity using Theme constants
        import os
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from ui.theme import Theme
        rarity_styles = {
            'common': {'color': Theme.MUTED_FOREGROUND, 'border': Theme.BORDER},
            'uncommon': {'color': Theme.ACCENT, 'border': Theme.ACCENT},
            'rare': {'color': Theme.PRIMARY, 'border': Theme.PRIMARY},
            'epic': {'color': Theme.SECONDARY, 'border': Theme.SECONDARY},  # Purple for epic
            'legendary': {'color': Theme.MUTED, 'border': Theme.MUTED}  # Gold for legendary
        }

        rarity_style = rarity_styles.get(self.item.rarity, rarity_styles['common'])
        border_color = rarity_style['border'].name()
        text_color = rarity_style['color'].name()

        self.setStyleSheet(f"""
            ItemCard {{
                background-color: {Theme.CARD.name()};
                border: 2px solid {border_color};
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                padding: {Theme.SPACING_SM}px;
            }}
            ItemCard:hover {{
                background-color: {Theme.MUTED.name()};
                border-color: {text_color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(Theme.SPACING_XS)
        layout.setContentsMargins(Theme.SPACING_SM, Theme.SPACING_SM, Theme.SPACING_SM, Theme.SPACING_SM)

        # Item icon/emoji with accessibility
        icon_result = self.get_item_icon()
        icon_label = QLabel()
        if isinstance(icon_result, str):
            # It's text/emoji
            icon_label.setText(icon_result)
            icon_label.setStyleSheet(f"font-size: 32px; background: transparent; border: none;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setAccessibleName(f"Icon for {self.item.name}")
            icon_label.setAccessibleDescription(f"Visual representation of {self.item.item_type}")
        else:
            # It's a QLabel with image already set up
            icon_label = icon_result
        layout.addWidget(icon_label)

        # Item name with better styling
        name_label = QLabel(self.item.name)
        name_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: {Theme.FONT_WEIGHT_BOLD};
            color: {text_color};
            background: transparent;
            border: none;
        """)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setAccessibleName("Item name")
        name_label.setAccessibleDescription(self.item.name)
        layout.addWidget(name_label)

        # Item stats/description with theme colors
        stats_text = self.get_stats_text()
        stats_label = QLabel(stats_text)
        stats_label.setStyleSheet(f"""
            font-size: 11px;
            color: {Theme.MUTED_FOREGROUND.name()};
            background: transparent;
            border: none;
        """)
        stats_label.setAlignment(Qt.AlignCenter)
        stats_label.setWordWrap(True)
        stats_label.setAccessibleName("Item stats")
        stats_label.setAccessibleDescription(stats_text if stats_text else "No special stats")
        layout.addWidget(stats_label)

        # Rarity badge with theme colors
        rarity_label = QLabel(self.item.rarity.title())
        rarity_label.setStyleSheet(f"""
            font-size: 10px;
            color: {text_color};
            background-color: rgba(0, 0, 0, 0.4);
            padding: {Theme.SPACING_XS}px {Theme.SPACING_SM}px;
            border-radius: {Theme.BORDER_RADIUS_SM}px;
            border: none;
            font-weight: {Theme.FONT_WEIGHT_MEDIUM};
        """)
        rarity_label.setAlignment(Qt.AlignCenter)
        rarity_label.setAccessibleName("Item rarity")
        rarity_label.setAccessibleDescription(f"This item is {self.item.rarity} rarity")
        layout.addWidget(rarity_label)

        layout.addStretch()

        # Price/Value with theme colors
        if self.show_price:
            price_label = QLabel(f"💰 {self.item.value} gold")
            price_label.setStyleSheet(f"""
                font-size: 12px;
                font-weight: {Theme.FONT_WEIGHT_SEMIBOLD};
                color: {Theme.ACCENT.name()};
                background: transparent;
                border: none;
            """)
            price_label.setAlignment(Qt.AlignCenter)
            price_label.setAccessibleName("Item price")
            price_label.setAccessibleDescription(f"Costs {self.item.value} gold coins")
            layout.addWidget(price_label)

        # Action button with theme colors
        self.action_btn = QPushButton(self.action_text)
        self.action_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.CARD.name()};
                color: {Theme.PRIMARY.name()};
                border: 1px solid {Theme.PRIMARY.name()};
                border-radius: {Theme.BORDER_RADIUS_SM}px;
                padding: {Theme.SPACING_XS}px {Theme.SPACING_SM}px;
                font-size: 11px;
                font-weight: {Theme.FONT_WEIGHT_MEDIUM};
            }}
            QPushButton:hover {{
                background-color: {Theme.SECONDARY.name()};
                color: {Theme.SECONDARY_FOREGROUND.name()};
            }}
            QPushButton:pressed {{
                background-color: {Theme.MUTED.name()};
            }}
            QPushButton:disabled {{
                background-color: {Theme.MUTED.name()};
                color: {Theme.MUTED_FOREGROUND.name()};
                border-color: {Theme.BORDER.name()};
            }}
        """)
        self.action_btn.setAccessibleName(f"{self.action_text} button for {self.item.name}")
        self.action_btn.setAccessibleDescription(f"Click to {self.action_text.lower()} {self.item.name}")
        self.action_btn.clicked.connect(lambda: self.action_clicked.emit(self.item, self.action_text.lower()))
        layout.addWidget(self.action_btn)

        # Set up full tooltip with detailed item information
        tooltip_text = self.get_tooltip_text()
        self.setToolTip(tooltip_text)

        # Make the entire card clickable and focusable
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAccessibleName(f"Item card for {self.item.name}")
        self.setAccessibleDescription(f"{self.item.item_type.title()} item: {self.item.description or 'No description available'}")

    def setup_drag_drop(self):
        """Set up drag and drop functionality for the item card"""
        # Enable drag and drop
        self.setAcceptDrops(True)
        # We could add drag functionality here if needed

    def dragEnterEvent(self, event):
        """Handle drag enter events"""
        if event.mimeData().hasText() and event.mimeData().text().startswith("item:"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop events for item rearrangement"""
        if event.mimeData().hasText() and event.mimeData().text().startswith("item:"):
            event.acceptProposedAction()

    def get_item_icon(self):
        """Get icon for item type - images for weapons, emojis for others"""
        if self.item.item_type == 'weapon':
            weapon_icon = self.get_weapon_icon()
            if weapon_icon:  # If we got an image, return it
                return weapon_icon
        # Default emoji icons
        icons = {
            'armor': '🛡️',
            'accessory': '💍',
            'consumable': '🧪'
        }
        return icons.get(self.item.item_type, '📦')

    def get_weapon_icon(self):
        """Get weapon icon as a QLabel with image, fallback to emoji"""
        # Map weapon names to icon files
        weapon_icons = {
            'Iron Sword': 'iron_sword.png',
            'Steel Sword': 'steel_sword.png',
            'Magic Sword': 'magic_sword.png'
        }

        icon_file = weapon_icons.get(self.item.name)

        if icon_file:
            # Try to load the icon file
            icon_path = os.path.join('assets', icon_file)
            if os.path.exists(icon_path):
                try:
                    pixmap = QPixmap(icon_path)
                    if not pixmap.isNull():
                        label = QLabel()
                        pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        label.setPixmap(pixmap)
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        return label
                    else:
                        print(f"Warning: Failed to load pixmap from {icon_path}")
                except Exception as e:
                    print(f"Warning: Error loading image from {icon_path}: {e}")
            else:
                print(f"Warning: Icon file not found: {icon_path}")

        # Fallback to emoji if image not found or not matched
        return '⚔️'

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

    def get_tooltip_text(self):
        """Generate detailed tooltip text for the item"""
        if not self.item:
            return ""

        tooltip_lines = []
        tooltip_lines.append(f"<b>{self.item.name}</b>")
        tooltip_lines.append("")  # Empty line for spacing

        # Type and rarity
        tooltip_lines.append(f"<i>{self.item.item_type.title()} - {self.item.rarity.title()}</i>")
        tooltip_lines.append("")  # Empty line for spacing

        # Stats section
        stats = []
        if hasattr(self.item, 'attack_bonus') and self.item.attack_bonus > 0:
            stats.append(f"⚔️ +{self.item.attack_bonus} Attack")
        if hasattr(self.item, 'defense_bonus') and self.item.defense_bonus > 0:
            stats.append(f"🛡️ +{self.item.defense_bonus} Defense")

        if stats:
            tooltip_lines.append("• Stats:")
            tooltip_lines.extend(f"  {stat}" for stat in stats)
            tooltip_lines.append("")

        # Effect section
        if hasattr(self.item, 'effect') and self.item.effect:
            effect_desc = self.get_effect_description()
            if effect_desc:
                tooltip_lines.append("• Effect:")
                tooltip_lines.append(f"  {effect_desc}")
                tooltip_lines.append("")

        # Description section
        if hasattr(self.item, 'description') and self.item.description:
            tooltip_lines.append("• Description:")
            tooltip_lines.append(f"  {self.item.description}")

        # Value section
        if hasattr(self.item, 'value') and self.item.value > 0:
            tooltip_lines.append(f"")
            tooltip_lines.append(f"<i>💰 Sell for: {self.item.value // 2} gold</i>")

        return '\n'.join(tooltip_lines)

    def get_effect_description(self):
        """Get human-readable effect description"""
        if not hasattr(self.item, 'effect') or not self.item.effect:
            return ""

        if self.item.effect == 'heal':
            return f"Heals {self.item.power} HP when used"
        elif self.item.effect == 'restore_mana':
            return f"Restores {self.item.power} MP when used"
        else:
            return f"Special effect: {self.item.effect.title()}"


class ItemSelectionOverlay(QDialog):
    """Modal dialog for selecting items from a list"""
    item_selected = Signal(object)  # Emits the selected Item object

    def __init__(self, items, title="Select Item", action_text="Select", show_price=False, parent=None):
        super().__init__(parent)
        self.items = items
        self.title_text = title
        self.action_text = action_text
        self.show_price = show_price
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        """Initialize the overlay UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #f1f0f2;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Scrollable grid of item cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(10)

        self.refresh_grid()

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Cancel button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d283d;
                color: #9a96a5;
                border: 1px solid #3e3754;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #352e4d;
                color: #f1f0f2;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def refresh_grid(self):
        """Refresh the item grid layout"""
        # Clear existing items
        self.clear_grid()

        if not self.items:
            empty_label = QLabel("No items available")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9a96a5; font-size: 16px;")
            self.grid_layout.addWidget(empty_label, 0, 0, 1, 4)
            return

        # Add items to grid (4 columns)
        row, col = 0, 0
        for item in self.items:
            card = ItemCard(item, self.action_text, self.show_price)
            card.setMaximumSize(180, 220)
            card.action_clicked.connect(self.on_item_selected)
            self.grid_layout.addWidget(card, row, col)

            col += 1
            if col >= 4:
                col = 0
                row += 1

        # Add stretch to push items to top
        self.grid_layout.setRowStretch(row + 1, 1)
        self.grid_layout.setColumnStretch(4, 1)

    def clear_grid(self):
        """Clear all widgets from the grid layout"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()

    def on_item_selected(self, item, action):
        """Handle item selection from card"""
        self.item_selected.emit(item)
        self.accept()

    def showEvent(self, event):
        """Refresh the grid when dialog is shown"""
        super().showEvent(event)
        self.refresh_grid()
