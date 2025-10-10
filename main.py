import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTextEdit,
                               QGridLayout, QGroupBox, QInputDialog, QMessageBox,
                               QProgressBar, QListWidget, QListWidgetItem, QGraphicsDropShadowEffect,
                               QStackedWidget, QScrollArea, QFrame, QLineEdit, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPropertyAnimation, QEasingCurve, QPoint, Property
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap
import random
import time
from models import Hero, Enemy
from game import random_encounter, get_shop_items, apply_item_effects, handle_player_turn, handle_enemy_turn
from ui_components import ItemCard, ItemSelectionOverlay, CharacterCreationOverlay

class GameState:
    """Manages the current state of the game"""
    MENU = "menu"
    ADVENTURE = "adventure"
    COMBAT = "combat"
    SHOP = "shop"
    STATS = "stats"

class PageIndex:
    """Page indices for QStackedWidget"""
    ADVENTURE = 0
    STATS = 1
    INVENTORY = 2
    SHOP = 3
    COMBAT = 4

class AnimatedProgressBar(QProgressBar):
    """Progress bar with smooth animation"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = None

    def setValue(self, value):
        """Override setValue to add smooth animation"""
        if self._animation:
            self._animation.stop()

        self._animation = QPropertyAnimation(self, b"value")
        self._animation.setDuration(500)  # 500ms animation
        self._animation.setStartValue(self.value())
        self._animation.setEndValue(value)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.start()

class ShadowedProgressBar(AnimatedProgressBar):
    """A progress bar that draws text with a shadow for better contrast."""
    def paintEvent(self, event):
        # First, draw the progress bar as usual but without the text
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        text = self.text()
        text_rect = self.rect()

        # Draw the shadow/outline
        painter.setPen(QColor('#1e2228'))
        painter.drawText(text_rect.translated(1, 1), Qt.AlignCenter, text)

        # Draw the main text
        painter.setPen(QColor('#ffffff'))
        painter.drawText(text_rect, Qt.AlignCenter, text)

class ScalablePixmapLabel(QLabel):
    """A QLabel that scales its pixmap while maintaining aspect ratio."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._original_pixmap = None
        self.setMinimumSize(150, 150) # Set a minimum size for the sprite
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setOriginalPixmap(self, pixmap):
        """Set the original, full-resolution pixmap."""
        self._original_pixmap = pixmap
        self.update_pixmap(self.size())

    def resizeEvent(self, event):
        """Handle the widget being resized by rescaling the pixmap."""
        if self._original_pixmap:
            self.update_pixmap(event.size())
        super().resizeEvent(event)

    def update_pixmap(self, size):
        """Scale the original pixmap to fit the new size and set it."""
        if not self._original_pixmap:
            return
        scaled_pixmap = self._original_pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)

class RPGGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.hero = None
        self.current_state = GameState.MENU
        self.current_enemy = None
        self.game_log = []
        self.animations = []  # Store active animations
        self.init_ui()

    def shake_widget(self, widget, duration=200, magnitude=10):
        """Create a shake animation for a widget"""
        original_pos = widget.pos()

        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setLoopCount(2)

        # Create shake effect by moving left and right
        animation.setKeyValueAt(0, original_pos)
        animation.setKeyValueAt(0.25, original_pos + QPoint(magnitude, 0))
        animation.setKeyValueAt(0.5, original_pos - QPoint(magnitude, 0))
        animation.setKeyValueAt(0.75, original_pos + QPoint(magnitude // 2, 0))
        animation.setKeyValueAt(1, original_pos)

        animation.start()
        self.animations.append(animation)  # Keep reference to prevent garbage collection

    def flash_widget(self, widget, color, duration=300):
        """Create a flash effect on a widget by temporarily changing background"""
        original_style = widget.styleSheet()

        # Flash color
        flash_style = original_style + f"\nbackground-color: {color};"
        widget.setStyleSheet(flash_style)

        # Restore original style after duration
        QTimer.singleShot(duration, lambda: widget.setStyleSheet(original_style))

    def resizeEvent(self, event):
        """Handle window resize to scale font size."""
        super().resizeEvent(event)
        # Scale font size of the log display based on window height
        font_size = max(8, min(18, int(self.height() / 50)))
        font = self.log_display.font()
        font.setPointSize(font_size)
        self.log_display.setFont(font)


    def init_ui(self):
        """Initialize the enhanced user interface with modern design"""
        self.setWindowTitle("PyRPG Adventure")
        self.resize(1200, 750)
        self.setMinimumSize(800, 600)

        # Modern dark theme inspired by professional applications
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282c34;
                color: #abb2bf;
                font-family: 'Inter', 'SF Pro Display', 'Segoe UI', sans-serif;
            }

            /* Professional Button Styling */
            QPushButton {
                color: #abb2bf;
                background-color: #282c34;
                border: 1px solid #3e4452;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3e4452;
            }
            QPushButton:pressed {
                background-color: #4b5263;
            }

            /* Primary Action Buttons */
            QPushButton#explore_btn,
            QPushButton#shop_btn,
            QPushButton#stats_btn,
            QPushButton#rest_btn {
                background-color: #282c34;
                border: 1px solid #61afef;
                color: #61afef;
                padding: 10px 24px;
                font-weight: 500;
            }
            QPushButton#explore_btn:hover,
            QPushButton#shop_btn:hover,
            QPushButton#stats_btn:hover,
            QPushButton#rest_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }

            QPushButton#quit_btn {
                background-color: #282c34;
                border: 1px solid #e06c75;
                color: #e06c75;
            }
            QPushButton#quit_btn:hover {
                background-color: #3e4452;
            }

            /* Combat Buttons */
            QPushButton#attack_btn {
                background-color: #282c34;
                color: #e06c75;
                font-size: 15px;
                font-weight: 600;
                padding: 12px 28px;
                border: 1px solid #e06c75;
                border-radius: 4px;
            }
            QPushButton#attack_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }

            QPushButton#run_btn {
                background-color: #282c34;
                color: #abb2bf;
                border: 1px solid #3e4452;
            }
            QPushButton#run_btn:hover {
                background-color: #3e4452;
            }

            /* Professional GroupBox */
            QGroupBox {
                color: #98c379;
                border: 1px solid #3e4452;
                border-radius: 5px;
                margin-top: 1ex;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                padding-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #98c379;
            }

            /* Text Display */
            QTextEdit {
                background-color: #21252b;
                color: #abb2bf;
                border: 1px solid #3e4452;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Inter', 'SF Pro Display', 'Segoe UI', sans-serif;
                selection-background-color: #3e4452;
            }

            /* Progress Bars */
            QProgressBar {
                border: 1px solid #3e4452;
                border-radius: 5px;
                text-align: center;
                font-weight: 600;
                font-size: 11px;
                background-color: #21252b;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: #61afef;
            }

            /* Label Styling */
            QLabel {
                color: #abb2bf;
                font-size: 13px;
            }

            /* Sidebar Navigation */
            QListWidget {
                background-color: #21252b;
                color: #abb2bf;
                border: none;
                border-right: 1px solid #3e4452;
                font-size: 15px;
                padding: 10px 0;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-left: 3px solid transparent;
            }
            QListWidget::item:hover {
                background-color: #282c34;
            }
            QListWidget::item:selected {
                background-color: #282c34;
                color: #61afef;
                border-left-color: #61afef;
            }

            /* Combat Info Card */
            QLabel#combat_info {
                background-color: #21252b;
                border: 1px solid #3e4452;
                border-radius: 5px;
                padding: 15px;
                font-size: 13px;
                color: #abb2bf;
            }

            /* Stats Labels */
            QLabel#health_label,
            QLabel#mana_label {
                color: #abb2bf;
                font-weight: 600;
                font-size: 13px;
            }
            QLabel#attack_label {
                color: #e06c75;
                font-weight: 600;
                font-size: 12px;
            }
            QLabel#defense_label {
                color: #61afef;
                font-weight: 600;
                font-size: 12px;
            }
            QLabel#gold_label {
                color: #e5c07b;
                font-weight: 600;
                font-size: 12px;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Game log (top section) - Enhanced with better styling
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        welcome_msg = """
        <div style='text-align: center; padding: 10px; font-size: 14px;'>
            <span style='color: #61afef; font-weight: bold; font-size: 16px;'>⚔️ Welcome to PyRPG Adventure! ⚔️</span><br>
            <span style='color: #abb2bf; font-size: 11px;'>Embark on an epic quest filled with danger and glory!</span>
        </div>
        """
        self.log_display.setHtml(welcome_msg)
        self.main_layout.addWidget(self.log_display, 1) # Add with stretch factor

        # Main content area: Sidebar + Stacked Widget
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar navigation
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setFocusPolicy(Qt.NoFocus)
        content_layout.addWidget(self.sidebar)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget, 1)  # Stretch factor 1

        self.main_layout.addLayout(content_layout, 4)  # Add with stretch factor

        # Create all pages
        self.create_adventure_page()
        self.create_stats_page()
        self.create_inventory_page()
        self.create_shop_page()
        self.create_combat_page()

        # Setup sidebar items
        self.sidebar.addItem("🏠 Adventure")
        self.sidebar.addItem("📊 Stats")
        self.sidebar.addItem("🎒 Inventory")
        self.sidebar.addItem("🏪 Shop")

        # Connect sidebar to page switching
        self.sidebar.currentRowChanged.connect(self.on_sidebar_changed)

        # Start with adventure page selected
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)

        self.show_menu()

    def on_sidebar_changed(self, index):
        """Handle sidebar selection changes"""
        # Only allow navigation if hero exists (except for adventure page which shows menu)
        if not self.hero and index != PageIndex.ADVENTURE:
            self.sidebar.setCurrentRow(PageIndex.ADVENTURE)
            return

        # Update the stacked widget
        self.stacked_widget.setCurrentIndex(index)

        # Update stats display when switching pages
        if self.hero:
            self.update_stats_display()

    def create_adventure_page(self):
        """Create the adventure page with hero stats and action buttons"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Enhanced Stats Panel with Progress Bars
        self.stats_group = QGroupBox("⚔️ Hero Status")
        self.stats_group.setMinimumWidth(300)
        self.stats_layout = QVBoxLayout()

        # Hero name and level - Enhanced typography
        name_layout = QHBoxLayout()
        self.name_label = QLabel("Name: Not created")
        self.name_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #61afef;
        """)
        self.level_label = QLabel("Level: -")
        self.level_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #98c379;
            background-color: #21252b;
            padding: 4px 10px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        name_layout.addWidget(self.name_label)
        name_layout.addStretch()
        name_layout.addWidget(self.level_label)
        self.stats_layout.addLayout(name_layout)

        # Health bar - Professional styling
        health_layout = QHBoxLayout()
        health_label = QLabel("❤️ Health:")
        health_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #abb2bf;")
        health_layout.addWidget(health_label)
        self.health_bar = AnimatedProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(100)
        self.health_bar.setFormat("100/100 HP")
        self.health_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e4452;
                border-radius: 5px;
                height: 26px;
                background-color: #21252b;
                color: #ffffff;
                font-weight: 600;
                font-size: 12px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #98c379;
                width: 10px;
                margin: 0.5px;
            }
        """)
        health_layout.addWidget(self.health_bar)
        self.stats_layout.addLayout(health_layout)

        # Experience bar - Professional blue theme
        exp_layout = QHBoxLayout()
        exp_label = QLabel("⭐ Experience:")
        exp_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #abb2bf;")
        exp_layout.addWidget(exp_label)
        self.exp_bar = AnimatedProgressBar()
        self.exp_bar.setRange(0, 100)
        self.exp_bar.setValue(0)
        self.exp_bar.setFormat("0/100 XP")
        self.exp_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3e4452;
                border-radius: 5px;
                height: 26px;
                background-color: #21252b;
                color: #ffffff;
                font-weight: 600;
                font-size: 12px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #61afef;
                width: 10px;
                margin: 0.5px;
            }
        """)
        exp_layout.addWidget(self.exp_bar)
        self.stats_layout.addLayout(exp_layout)

        # Combat stats grid - Enhanced styling
        combat_stats_layout = QGridLayout()
        combat_stats_layout.setSpacing(8)

        self.attack_label = QLabel("⚔️ Attack: -")
        self.attack_label.setObjectName("attack_label")
        self.attack_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        combat_stats_layout.addWidget(self.attack_label, 0, 0)

        self.defense_label = QLabel("🛡️ Defense: -")
        self.defense_label.setObjectName("defense_label")
        self.defense_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        combat_stats_layout.addWidget(self.defense_label, 0, 1)

        self.gold_label = QLabel("💰 Gold: -")
        self.gold_label.setObjectName("gold_label")
        self.gold_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
        """)
        combat_stats_layout.addWidget(self.gold_label, 1, 0)

        self.inventory_label = QLabel("🎒 Inventory: Empty")
        self.inventory_label.setStyleSheet("""
            background-color: #21252b;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #3e4452;
            color: #abb2bf;
        """)
        combat_stats_layout.addWidget(self.inventory_label, 1, 1)

        self.stats_layout.addLayout(combat_stats_layout)

        # Equipment display - Professional card
        equipment_group = QGroupBox("⚔️ Equipment")
        equipment_layout = QVBoxLayout()

        self.weapon_label = QLabel("🗡️ Weapon: None")
        self.weapon_label.setStyleSheet("font-size: 12px; color: #e06c75; padding: 4px;")
        self.armor_label = QLabel("🛡️ Armor: None")
        self.armor_label.setStyleSheet("font-size: 12px; color: #61afef; padding: 4px;")
        self.accessory_label = QLabel("💍 Accessory: None")
        self.accessory_label.setStyleSheet("font-size: 12px; color: #c678dd; padding: 4px;")

        equipment_layout.addWidget(self.weapon_label)
        equipment_layout.addWidget(self.armor_label)
        equipment_layout.addWidget(self.accessory_label)

        equipment_group.setLayout(equipment_layout)
        self.stats_layout.addWidget(equipment_group)

        self.stats_group.setLayout(self.stats_layout)
        layout.addWidget(self.stats_group)

        layout.addStretch()

        # Action buttons
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(10)

        self.explore_btn = QPushButton("🔍 Explore")
        self.explore_btn.setObjectName("explore_btn")
        self.explore_btn.setToolTip("Explore the wilderness and encounter enemies!")
        self.explore_btn.setMinimumHeight(50)

        self.rest_btn = QPushButton("😴 Rest")
        self.rest_btn.setObjectName("rest_btn")
        self.rest_btn.setToolTip("Rest to fully recover your health")
        self.rest_btn.setMinimumHeight(50)

        self.quit_btn = QPushButton("❌ Quit")
        self.quit_btn.setObjectName("quit_btn")
        self.quit_btn.setToolTip("Exit the game")
        self.quit_btn.setMinimumHeight(50)

        self.explore_btn.clicked.connect(self.explore)
        self.rest_btn.clicked.connect(self.rest)
        self.quit_btn.clicked.connect(self.quit_game)

        # Add shadow effects to action buttons for depth
        for btn in [self.explore_btn, self.rest_btn, self.quit_btn]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 0, 0, 120))
            btn.setGraphicsEffect(shadow)

        self.button_layout.addWidget(self.explore_btn, 0, 0)
        self.button_layout.addWidget(self.rest_btn, 0, 1)
        self.button_layout.addWidget(self.quit_btn, 1, 0, 1, 2)

        layout.addLayout(self.button_layout)

        self.stacked_widget.addWidget(page)

    def create_stats_page(self):
        """Create the detailed stats page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("📊 Hero Statistics")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #61afef;
            padding: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scroll area for stats
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)

        # Create stats display label
        self.detailed_stats_label = QLabel("No character created yet")
        self.detailed_stats_label.setStyleSheet("""
            background-color: #21252b;
            color: #abb2bf;
            border: 1px solid #3e4452;
            border-radius: 8px;
            padding: 20px;
            font-size: 13px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        """)
        self.detailed_stats_label.setWordWrap(True)
        self.detailed_stats_label.setTextFormat(Qt.RichText)
        scroll_layout.addWidget(self.detailed_stats_label)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        self.stacked_widget.addWidget(page)

    def create_inventory_page(self):
        """Create the inventory page with item grid"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with title and gold
        header_layout = QHBoxLayout()

        title = QLabel("🎒 Inventory")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #61afef;
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.inventory_gold_label = QLabel("💰 Gold: 0")
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

        self.stacked_widget.addWidget(page)

    def create_shop_page(self):
        """Create the shop page with item grid"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with title and gold
        header_layout = QHBoxLayout()

        title = QLabel("🏪 Merchant's Emporium")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #e5c07b;
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.shop_gold_label = QLabel("💰 Gold: 0")
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
            card.action_clicked.connect(self.on_shop_item_clicked)
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

        sell_btn = QPushButton("💰 Sell Items")
        sell_btn.setStyleSheet("""
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
        sell_btn.setMinimumHeight(45)
        sell_btn.clicked.connect(self.sell_items)

        leave_btn = QPushButton("🚪 Leave Shop")
        leave_btn.setStyleSheet("""
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
        leave_btn.setMinimumHeight(45)
        leave_btn.clicked.connect(self.leave_shop)

        button_layout.addWidget(sell_btn)
        button_layout.addWidget(leave_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.stacked_widget.addWidget(page)

    def create_placeholder_pixmap(self, color, size=150):
        """Creates a QPixmap of a given color and size."""
        pixmap = QPixmap(size, size)
        pixmap.fill(color)
        return pixmap

    def create_combat_page(self):
        """Create the visual combat page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Top section for combatants
        combatants_layout = QHBoxLayout()

        # Hero Side
        hero_combat_layout = QVBoxLayout()
        hero_combat_layout.setAlignment(Qt.AlignCenter)
        
        self.hero_combat_name = QLabel("Hero")
        self.hero_combat_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #61afef;")
        self.hero_combat_name.setAlignment(Qt.AlignCenter)
        
        self.hero_sprite_label = ScalablePixmapLabel()
        self.hero_sprite_label.setAlignment(Qt.AlignCenter)
        
        self.hero_combat_health_bar = AnimatedProgressBar()
        self.hero_combat_health_bar.setMaximumHeight(20)
        self.hero_combat_health_bar.setStyleSheet("""
            QProgressBar::chunk { background-color: #98c379; }
        """)

        self.hero_combat_mana_bar = AnimatedProgressBar()
        self.hero_combat_mana_bar.setMaximumHeight(20)
        self.hero_combat_mana_bar.setStyleSheet("""
            QProgressBar::chunk { background-color: #61afef; }
        """)

        hero_combat_layout.addWidget(self.hero_combat_name)
        hero_combat_layout.addWidget(self.hero_sprite_label)
        hero_combat_layout.addWidget(self.hero_combat_health_bar)
        hero_combat_layout.addWidget(self.hero_combat_mana_bar)
        combatants_layout.addLayout(hero_combat_layout)

        # VS Label
        vs_label = QLabel("VS")
        vs_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e5c07b;")
        vs_label.setAlignment(Qt.AlignCenter)
        combatants_layout.addWidget(vs_label)

        # Enemy Side
        enemy_combat_layout = QVBoxLayout()
        enemy_combat_layout.setAlignment(Qt.AlignCenter)

        self.enemy_combat_name = QLabel("Enemy")
        self.enemy_combat_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #e06c75;")
        self.enemy_combat_name.setAlignment(Qt.AlignCenter)

        self.enemy_sprite_label = ScalablePixmapLabel()
        self.enemy_sprite_label.setAlignment(Qt.AlignCenter)

        self.enemy_combat_health_bar = AnimatedProgressBar()
        self.enemy_combat_health_bar.setMaximumHeight(20)
        self.enemy_combat_health_bar.setStyleSheet("""
            QProgressBar::chunk { background-color: #e06c75; }
        """)

        enemy_combat_layout.addWidget(self.enemy_combat_name)
        enemy_combat_layout.addWidget(self.enemy_sprite_label)
        enemy_combat_layout.addWidget(self.enemy_combat_health_bar)
        combatants_layout.addLayout(enemy_combat_layout)

        layout.addLayout(combatants_layout)
        layout.addStretch()

        # Combat buttons
        combat_buttons_layout = QGridLayout()
        combat_buttons_layout.setSpacing(10)

        self.attack_btn = QPushButton("⚔️ Attack")
        self.attack_btn.setObjectName("attack_btn")
        self.attack_btn.setToolTip("Strike the enemy with your weapon!")
        self.attack_btn.setMinimumHeight(60)

        self.use_skill_btn = QPushButton("✨ Use Skill")
        self.use_skill_btn.setObjectName("use_skill_btn")
        self.use_skill_btn.setToolTip("Use a special skill or magic spell")
        self.use_skill_btn.setMinimumHeight(60)
        self.use_skill_btn.setStyleSheet("""
            QPushButton#use_skill_btn {
                background-color: #282c34;
                color: #c678dd;
                border: 1px solid #c678dd;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton#use_skill_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)

        self.use_item_btn = QPushButton("🧪 Use Item")
        self.use_item_btn.setObjectName("use_item_btn")
        self.use_item_btn.setToolTip("Use a consumable item from your inventory")
        self.use_item_btn.setMinimumHeight(60)
        self.use_item_btn.setStyleSheet("""
            QPushButton#use_item_btn {
                background-color: #282c34;
                color: #98c379;
                border: 1px solid #98c379;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton#use_item_btn:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)

        self.run_btn = QPushButton("🏃 Run")
        self.run_btn.setObjectName("run_btn")
        self.run_btn.setToolTip("Attempt to escape the battle")
        self.run_btn.setMinimumHeight(60)

        self.attack_btn.clicked.connect(self.combat_attack)
        self.use_skill_btn.clicked.connect(self.combat_use_skill)
        self.use_item_btn.clicked.connect(self.combat_use_item)
        self.run_btn.clicked.connect(self.combat_run)

        for btn in [self.attack_btn, self.use_skill_btn, self.use_item_btn, self.run_btn]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setXOffset(0)
            shadow.setYOffset(5)
            shadow.setColor(QColor(0, 0, 0, 150))
            btn.setGraphicsEffect(shadow)

        combat_buttons_layout.addWidget(self.attack_btn, 0, 0)
        combat_buttons_layout.addWidget(self.use_skill_btn, 0, 1)
        combat_buttons_layout.addWidget(self.use_item_btn, 1, 0)
        combat_buttons_layout.addWidget(self.run_btn, 1, 1)

        layout.addLayout(combat_buttons_layout)
        self.stacked_widget.addWidget(page)

    def log_message(self, message):
        """Add a message to the game log with color coding"""
        self.game_log.append(message)
        # Keep only last 20 messages
        if len(self.game_log) > 20:
            self.game_log = self.game_log[-20:]

        # Build HTML with color-coded messages (newest at bottom)
        log_html = "<div style='padding: 5px; line-height: 1.6;'>"
        for msg in self.game_log[-10:]:  # Show last 10 messages in correct order
            # Color code based on message content
            color = "#e8e8e8"  # default

            if "damage" in msg.lower() or "defeated" in msg.lower() or "💥" in msg or "⚔️" in msg:
                color = "#e06c75"  # red for damage/combat
            elif "gold" in msg.lower() or "💰" in msg:
                color = "#e5c07b"  # gold/yellow color
            elif "experience" in msg.lower() or "level" in msg.lower() or "⭐" in msg or "🎉" in msg:
                color = "#c678dd"  # purple for XP/level
            elif "heal" in msg.lower() or "restored" in msg.lower() or "rest" in msg.lower():
                color = "#98c379"  # green for healing
            elif "found" in msg.lower() or "📦" in msg:
                color = "#61afef"  # blue for items
            elif "welcome" in msg.lower() or "===" in msg:
                color = "#61afef"  # blue for welcome messages
            elif "failed" in msg.lower() or "❌" in msg or "💀" in msg:
                color = "#e06c75"  # red for failures
            elif "escape" in msg.lower() or "🏃" in msg:
                color = "#abb2bf"  # gray for escape

            log_html += f"<div style='color: {color}; margin: 2px 0;'>{msg}</div>"
        log_html += "</div>"

        self.log_display.setHtml(log_html)
        # Scroll to bottom to show newest messages
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def handle_event(self, event):
        """Processes a game event and logs a message."""
        event_type = event.get('type')
        params = event
        
        message = ""
        if event_type == 'critical_hit':
            message = "💥 Critical hit!"
        elif event_type == 'player_damage':
            message = f"⚔️ You deal {params['damage']} damage to {params['target']}!"
            self.shake_widget(self.enemy_sprite_label)
        elif event_type == 'player_miss':
            message = f"🛡️ {params['target']} dodges your attack!"
        elif event_type == 'enemy_defeated':
            message = f"🎉 You defeated the {params['enemy_name']}!"
        elif event_type == 'gain_experience':
            message = f"⭐ Gained {params['amount']} experience!"
        elif event_type == 'gain_gold':
            message = f"💰 Gained {params['amount']} gold!"
        elif event_type == 'level_up':
            message = params['message']
        elif event_type == 'item_drop':
            message = f"📦 Found {params['item_name']} ({params['rarity']})!"
        elif event_type == 'escape_success':
            message = "🏃 You successfully escaped!"
        elif event_type == 'escape_fail':
            message = "❌ Failed to escape!"
        elif event_type == 'enemy_miss':
            message = f"🛡️ {params['enemy_name']} attacks, but you dodge!"
        elif event_type == 'enemy_damage':
            message = f"💥 {params['enemy_name']} deals {params['damage']} damage to you!"
            self.shake_widget(self.hero_sprite_label)
        elif event_type == 'player_defeated':
            message = "💀 You have been defeated..."
        elif event_type == 'status_effect_damage':
            message = f"☠️ You take {params['damage']} damage from status effects!"
        elif event_type == 'use_skill':
            message = f"✨ You used {params['skill_name']}!"

        if message:
            self.log_message(message)

    def show_menu(self):
        """Show the main menu"""
        self.current_state = GameState.MENU
        self.log_message("=== Welcome to PyRPG Adventure! ===")
        self.log_message("Click 'New Game' to start your adventure!")

        # Ensure we're on adventure page
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)

        # Hide existing game buttons
        self.explore_btn.hide()
        self.rest_btn.hide()

        # Show new game button with professional styling
        self.new_game_btn = QPushButton("🎮 New Game")
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #282c34;
                border: 2px solid #61afef;
                color: #61afef;
                font-size: 18px;
                font-weight: 600;
                padding: 20px 40px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3e4452;
                color: #ffffff;
            }
        """)
        self.new_game_btn.clicked.connect(self.new_game)

        # Add shadow to new game button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.new_game_btn.setGraphicsEffect(shadow)

        # Replace explore button with new game button
        self.button_layout.addWidget(self.new_game_btn, 0, 0, 1, 2)

    def new_game(self):
        """Start a new game using character creation overlay"""
        # Create character creation overlay
        overlay = CharacterCreationOverlay(self)
        overlay.character_created.connect(self.on_character_created)
        overlay.show()

    def on_character_created(self, hero_name):
        """Handle character creation completion"""
        self.hero = Hero(hero_name)
        self.current_state = GameState.ADVENTURE

        # Remove new game button and show game buttons
        self.new_game_btn.hide()
        self.button_layout.removeWidget(self.new_game_btn)
        self.new_game_btn.deleteLater()

        self.explore_btn.show()
        self.rest_btn.show()

        self.update_stats_display()
        self.log_message(f"Welcome, {hero_name}!")
        self.log_message("Your adventure begins now!")

    def update_stats_display(self):
        """Update the stats display with current hero stats"""
        if not self.hero:
            return

        # Update adventure page stats
        self.name_label.setText(f"Name: {self.hero.name}")
        self.level_label.setText(f"Level: {self.hero.level}")
        self.attack_label.setText(f"⚔️ Attack: {self.hero.attack_power}")
        self.defense_label.setText(f"🛡️ Defense: {self.hero.defense}")
        self.gold_label.setText(f"💰 Gold: {self.hero.gold}")

        # Update progress bars
        health_percent = int((self.hero.health / self.hero.max_health) * 100)
        self.health_bar.setValue(health_percent)
        self.health_bar.setFormat(f"{self.hero.health}/{self.hero.max_health} HP")

        exp_percent = int((self.hero.experience / self.hero.experience_to_level) * 100)
        self.exp_bar.setValue(exp_percent)
        self.exp_bar.setFormat(f"{self.hero.experience}/{self.hero.experience_to_level} XP")

        # Update equipment labels
        self.weapon_label.setText(f"🗡️ Weapon: {self.hero.equipment['weapon'].name if self.hero.equipment['weapon'] else 'None'}")
        self.armor_label.setText(f"🛡️ Armor: {self.hero.equipment['armor'].name if self.hero.equipment['armor'] else 'None'}")
        self.accessory_label.setText(f"💍 Accessory: {self.hero.equipment['accessory'].name if self.hero.equipment['accessory'] else 'None'}")

        # Show inventory
        if self.hero.inventory:
            inv_items = [item.name for item in self.hero.inventory[:3]]
            inventory_text = f"🎒 Inventory: {', '.join(inv_items)}"
            if len(self.hero.inventory) > 3:
                inventory_text += f" (+{len(self.hero.inventory) - 3} more)"
        else:
            inventory_text = "🎒 Inventory: Empty"

        self.inventory_label.setText(inventory_text)

        # Update detailed stats page
        stats_html = self.format_stats_html()
        self.detailed_stats_label.setText(stats_html)

        # Update gold labels on other pages
        self.shop_gold_label.setText(f"💰 Gold: {self.hero.gold}")
        self.inventory_gold_label.setText(f"💰 Gold: {self.hero.gold}")

        # Update inventory grid
        self.update_inventory_grid()

        # Color code progress bars based on health percentage
        if health_percent > 60:
            self.health_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #3e4452;
                    border-radius: 5px;
                    height: 26px;
                    background-color: #21252b;
                    color: #ffffff;
                    font-weight: 600;
                    font-size: 12px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #98c379;
                    width: 10px;
                    margin: 0.5px;
                }
            """)
        elif health_percent > 25:
            self.health_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #3e4452;
                    border-radius: 5px;
                    height: 26px;
                    background-color: #21252b;
                    color: #ffffff;
                    font-weight: 600;
                    font-size: 12px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #e5c07b;
                    width: 10px;
                    margin: 0.5px;
                }
            """)
        else:
            self.health_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #3e4452;
                    border-radius: 5px;
                    height: 26px;
                    background-color: #21252b;
                    color: #ffffff;
                    font-weight: 600;
                    font-size: 12px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #e06c75;
                    width: 10px;
                    margin: 0.5px;
                }
            """)

    def format_stats_html(self):
        """Format hero stats as HTML for detailed stats page"""
        if not self.hero:
            return "No character created yet"

        return f"""
<div style='line-height: 1.6;'>
    <h2 style='color: #61afef; border-bottom: 2px solid #3e4452; padding-bottom: 10px;'>⚔️ {self.hero.name}</h2>

    <h3 style='color: #98c379; margin-top: 20px;'>📊 Core Stats</h3>
    <div style='margin-left: 15px;'>
        <p><b>Level:</b> {self.hero.level}</p>
        <p><b>Experience:</b> {self.hero.experience} / {self.hero.experience_to_level}</p>
        <p><b>Health:</b> {self.hero.health} / {self.hero.max_health}</p>
        <p><b>Mana:</b> {self.hero.mana} / {self.hero.max_mana}</p>
        <p><b>Gold:</b> <span style='color: #e5c07b;'>{self.hero.gold}</span></p>
    </div>

    <h3 style='color: #e06c75; margin-top: 20px;'>⚡ Attributes</h3>
    <div style='margin-left: 15px;'>
        <p><b>Strength:</b> {self.hero.strength} (Physical damage)</p>
        <p><b>Dexterity:</b> {self.hero.dexterity} (Crit: {self.hero.crit_chance:.1f}%, Dodge: {self.hero.dodge_chance:.1f}%)</p>
        <p><b>Intelligence:</b> {self.hero.intelligence} (Magic power)</p>
        <p><b>Vitality:</b> {self.hero.vitality} (Defense)</p>
    </div>

    <h3 style='color: #61afef; margin-top: 20px;'>⚔️ Combat Stats</h3>
    <div style='margin-left: 15px;'>
        <p><b>Attack Power:</b> <span style='color: #e06c75;'>{self.hero.attack_power}</span></p>
        <p><b>Magic Power:</b> <span style='color: #c678dd;'>{self.hero.magic_power:.1f}</span></p>
        <p><b>Defense:</b> <span style='color: #61afef;'>{self.hero.defense}</span></p>
        <p><b>Critical Chance:</b> {self.hero.crit_chance:.1f}%</p>
        <p><b>Dodge Chance:</b> {self.hero.dodge_chance:.1f}%</p>
    </div>

    <h3 style='color: #c678dd; margin-top: 20px;'>🎒 Equipment</h3>
    <div style='margin-left: 15px;'>
        <p><b>Weapon:</b> {self.hero.equipment['weapon'].name if self.hero.equipment['weapon'] else 'None'}</p>
        <p><b>Armor:</b> {self.hero.equipment['armor'].name if self.hero.equipment['armor'] else 'None'}</p>
        <p><b>Accessory:</b> {self.hero.equipment['accessory'].name if self.hero.equipment['accessory'] else 'None'}</p>
    </div>

    <h3 style='color: #98c379; margin-top: 20px;'>📦 Inventory</h3>
    <div style='margin-left: 15px;'>
        <p><b>Items:</b> {len(self.hero.inventory)}</p>
        {''.join([f"<p style='margin-left: 15px;'>• {item.name} ({item.rarity})</p>" for item in self.hero.inventory]) if self.hero.inventory else '<p style="margin-left: 15px;">No items</p>'}
    </div>

    <h3 style='color: #e5c07b; margin-top: 20px;'>⭐ Progression</h3>
    <div style='margin-left: 15px;'>
        <p><b>Stat Points:</b> {self.hero.stat_points}</p>
        <p><b>Skill Points:</b> {self.hero.skill_points}</p>
    </div>
</div>
"""

    def update_inventory_grid(self):
        """Update the inventory grid with current items"""
        # Clear existing items
        while self.inventory_grid_layout.count():
            item = self.inventory_grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.hero or not self.hero.inventory:
            # Show empty state
            self.inventory_empty_label = QLabel("No items in inventory\n\nDefeat enemies and visit the shop to collect items!")
            self.inventory_empty_label.setStyleSheet("""
                font-size: 14px;
                color: #abb2bf;
                padding: 40px;
            """)
            self.inventory_empty_label.setAlignment(Qt.AlignCenter)
            self.inventory_grid_layout.addWidget(self.inventory_empty_label, 0, 0, Qt.AlignCenter)
            return

        # Create item cards
        row = 0
        col = 0
        max_cols = 4

        for item in self.hero.inventory:
            # Determine action based on item type
            if item.item_type == 'consumable':
                action_text = "Use"
            else:
                action_text = "Equip"

            card = ItemCard(item, action_text=action_text, show_price=False)
            card.action_clicked.connect(self.on_inventory_item_clicked)
            self.inventory_grid_layout.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def on_shop_item_clicked(self, item, action):
        """Handle shop item card clicks"""
        if action.lower() == "buy":
            self.buy_item(item.name, item.value)

    def on_inventory_item_clicked(self, item, action):
        """Handle inventory item card clicks"""
        if action.lower() == "use" and item.item_type == 'consumable':
            # Use consumable
            message = self.hero.use_item(item)
            if message:
                self.log_message(f"🧪 {message}")
                self.hero.remove_item(item)
                self.update_stats_display()
        elif action.lower() == "equip" and item.item_type in ['weapon', 'armor', 'accessory']:
            # Equip item
            self.hero.equip_item(item)
            self.hero.remove_item(item)
            self.log_message(f"⚔️ Equipped {item.name}!")
            self.update_stats_display()

    def explore(self):
        """Handle exploration and random encounters"""
        if not self.hero:
            return

        self.log_message("You venture into the wilderness...")
        QApplication.processEvents()

        # Simulate exploration delay
        QTimer.singleShot(1000, self.trigger_random_encounter)

    def trigger_random_encounter(self):
        """Trigger a random enemy encounter"""
        # Get a random enemy for this encounter
        from game import get_random_enemy
        self.current_enemy = get_random_enemy(self.hero.level)

        # Show combat interface
        self.show_combat_interface()

    def show_combat_interface(self):
        """Show the combat interface with current enemy - Enhanced formatting"""
        if not self.hero or not self.current_enemy:
            return

        self.current_state = GameState.COMBAT
        self.stacked_widget.setCurrentIndex(PageIndex.COMBAT)

        # Update names
        self.hero_combat_name.setText(f"{self.hero.name} (Lv.{self.hero.level})")
        self.enemy_combat_name.setText(f"{self.current_enemy.name} (Lv.{self.current_enemy.level})")

        # Update sprites
        hero_sprite = QPixmap("assets/Hero.png")
        
        enemy_sprite_map = {
            'warrior': "assets/Orc.png",
            'mage': "assets/mage.png",
            'rogue': "assets/rogue.png",
            'tank': "assets/golem.png"
        }
        enemy_sprite_path = enemy_sprite_map.get(self.current_enemy.enemy_type, "assets/Orc.png")
        enemy_sprite = QPixmap(enemy_sprite_path)

        self.hero_sprite_label.setOriginalPixmap(hero_sprite)
        self.enemy_sprite_label.setOriginalPixmap(enemy_sprite)

        # Update health bars
        self.hero_combat_health_bar.setRange(0, self.hero.max_health)
        self.hero_combat_health_bar.setValue(self.hero.health)
        self.hero_combat_health_bar.setFormat(f"{self.hero.health} / {self.hero.max_health}")

        self.hero_combat_mana_bar.setRange(0, self.hero.max_mana)
        self.hero_combat_mana_bar.setValue(self.hero.mana)
        self.hero_combat_mana_bar.setFormat(f"{self.hero.mana} / {self.hero.max_mana}")

        self.enemy_combat_health_bar.setRange(0, self.current_enemy.max_health)
        self.enemy_combat_health_bar.setValue(self.current_enemy.health)
        self.enemy_combat_health_bar.setFormat(f"{self.current_enemy.health} / {self.current_enemy.max_health}")

        self.log_message(f"A wild {self.current_enemy.name} (Lv.{self.current_enemy.level}) appears!")

    def hide_combat_interface(self):
        """Hide combat interface and return to adventure"""
        self.stacked_widget.setCurrentIndex(PageIndex.ADVENTURE)
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)
        self.current_state = GameState.ADVENTURE
        self.current_enemy = None

    def process_combat_round(self, action):
        """Process the player's turn and schedule the enemy's turn."""
        if not self.hero or not self.current_enemy:
            return

        # Disable combat buttons during the turn
        self.set_combat_buttons_enabled(False)

        events, combat_over = handle_player_turn(self.hero, self.current_enemy, action)
        for event in events:
            self.handle_event(event)

        self.update_combat_ui()

        if combat_over:
            QTimer.singleShot(1500, self.hide_combat_interface)
            self.update_stats_display()
            return

        # Schedule the enemy's turn after a delay
        QTimer.singleShot(1000, self.execute_enemy_turn)

    def execute_enemy_turn(self):
        """Process the enemy's turn after a delay."""
        if not self.hero or not self.current_enemy:
            return

        events, combat_over = handle_enemy_turn(self.hero, self.current_enemy)
        for event in events:
            self.handle_event(event)

        self.update_combat_ui()

        if combat_over:
            if not self.hero.is_alive():
                QMessageBox.critical(self, "Defeat", "You have been defeated! Game Over.")
                self.quit_game()
            return
        
        # Re-enable combat buttons for the next player turn
        self.set_combat_buttons_enabled(True)

    def update_combat_ui(self):
        """Update all combat UI elements."""
        self.hero_combat_health_bar.setValue(self.hero.health)
        self.hero_combat_health_bar.setFormat(f"{self.hero.health} / {self.hero.max_health}")
        self.hero_combat_mana_bar.setValue(self.hero.mana)
        self.hero_combat_mana_bar.setFormat(f"{self.hero.mana} / {self.hero.max_mana}")
        self.enemy_combat_health_bar.setValue(self.current_enemy.health)
        self.enemy_combat_health_bar.setFormat(f"{self.current_enemy.health} / {self.current_enemy.max_health}")
        self.update_stats_display()

    def set_combat_buttons_enabled(self, enabled):
        """Enable or disable all combat action buttons."""
        self.attack_btn.setEnabled(enabled)
        self.use_skill_btn.setEnabled(enabled)
        self.use_item_btn.setEnabled(enabled)
        self.run_btn.setEnabled(enabled)

    def open_shop(self):
        """Open the shop interface"""
        if not self.hero:
            return

        self.current_state = GameState.SHOP
        self.stacked_widget.setCurrentIndex(PageIndex.SHOP)
        self.sidebar.setCurrentRow(PageIndex.SHOP)

        self.log_message(f"You have {self.hero.gold} gold to spend!")

    def leave_shop(self):
        """Leave the shop"""
        self.current_state = GameState.ADVENTURE
        self.stacked_widget.setCurrentIndex(PageIndex.ADVENTURE)
        self.sidebar.setCurrentRow(PageIndex.ADVENTURE)
        self.log_message("You leave the shop.")

    def buy_item(self, item_name, price):
        """Buy an item from the shop"""
        if not self.hero:
            return

        # Get the actual Item object from the shop
        shop_items = get_shop_items()
        if item_name in shop_items:
            item = shop_items[item_name]

            if self.hero.gold >= item.value:
                self.hero.gold -= item.value
                self.hero.add_item(item)

                # Apply item effects
                message = apply_item_effects(self.hero, item)
                if message:
                    self.log_message(message)

                self.update_stats_display()
                self.log_message(f"Purchased {item.name}!")
            else:
                QMessageBox.warning(self, "Not Enough Gold",
                                  f"You need {item.value} gold to buy {item.name}. You have {self.hero.gold} gold.")
        else:
            QMessageBox.warning(self, "Item Not Found", f"Could not find item: {item_name}")

    def sell_items(self):
        """Sell items from inventory using overlay"""
        if not self.hero or not self.hero.inventory:
            self.log_message("You have no items to sell!")
            return

        # Create item selection overlay
        overlay = ItemSelectionOverlay(
            self.hero.inventory,
            title="Sell Item",
            action_text="Sell",
            show_price=True,
            parent=self
        )
        overlay.item_selected.connect(self.on_item_sold)
        overlay.show()

    def on_item_sold(self, item):
        """Handle item being sold"""
        sell_value = item.value // 2  # Sell for half price
        self.hero.inventory.remove(item)
        self.hero.gold += sell_value
        self.update_stats_display()
        self.log_message(f"Sold {item.name} for {sell_value} gold!")

    def show_stats(self):
        """Show detailed stats"""
        if not self.hero:
            return

        # Navigate to stats page
        self.stacked_widget.setCurrentIndex(PageIndex.STATS)
        self.sidebar.setCurrentRow(PageIndex.STATS)

        # Update GUI display
        self.update_stats_display()

    def rest(self):
        """Rest to restore health"""
        if not self.hero:
            return

        self.hero.health = self.hero.max_health
        self.update_stats_display()
        self.log_message("You rest and restore your health!")

    def quit_game(self):
        """Quit the game"""
        reply = QMessageBox.question(self, "Quit Game",
                                   "Are you sure you want to quit?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()

    def combat_attack(self):
        """Handle combat attack action"""
        self.process_combat_round("attack")


    def combat_run(self):
        """Handle combat run action"""
        self.process_combat_round("run")

    def combat_use_skill(self):
        """Handle using a skill during combat using overlay"""
        if not self.hero or not self.current_enemy:
            return

        if not self.hero.unlocked_skills:
            self.log_message("You have no skills to use!")
            return

        # Create skill selection overlay
        # Note: We need a way to display skills in an overlay. For now, we'll just use the first skill.
        # This should be replaced with a proper skill selection overlay.
        skill_to_use = self.hero.unlocked_skills[0]
        self.on_combat_skill_used(skill_to_use)

    def on_combat_skill_used(self, skill):
        """Handle skill being used in combat"""
        if self.hero.mana >= skill.mana_cost:
            self.hero.mana -= skill.mana_cost
            self.process_combat_round(('use_skill', skill))
        else:
            self.log_message(f"Not enough mana to use {skill.name}!")

    def combat_use_item(self):
        """Handle using an item during combat using overlay"""
        if not self.hero or not self.current_enemy:
            return

        # Filter for consumable items only
        consumables = [item for item in self.hero.inventory if item.item_type == 'consumable']

        if not consumables:
            self.log_message("You have no consumable items to use!")
            return

        # Create item selection overlay
        overlay = ItemSelectionOverlay(
            consumables,
            title="Use Item in Combat",
            action_text="Use",
            show_price=False,
            parent=self
        )
        overlay.item_selected.connect(self.on_combat_item_used)
        overlay.show()

    def on_combat_item_used(self, item):
        """Handle item being used in combat"""
        # Use the item
        message = self.hero.use_item(item)
        self.hero.inventory.remove(item)

        # Log the action
        if message:
            self.log_message(f"🧪 {message}")
            # Flash green for healing
            QTimer.singleShot(100, lambda: self.flash_widget(self.combat_info, "rgba(46, 204, 113, 0.3)", 200))

        # Update stats display
        self.update_stats_display()

        # Enemy gets a turn after using item
        self.process_combat_round("use_item")

def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("PyRPG Adventure")
    app.setApplicationVersion("1.0")

    # Create and show the game window
    game = RPGGame()
    game.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
