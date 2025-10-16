# -*- coding: utf-8 -*-
"""
Status effect visual indicators for combat
"""

from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QEasingCurve, Signal
from PySide6.QtGui import QFont


class StatusIndicator(QFrame):
    """Visual indicator for status effects like buffs/debuffs"""

    def __init__(self, effect_type, effect_name, duration=None, parent=None):
        super().__init__(parent)
        self.effect_type = effect_type
        self.effect_name = effect_name
        self.duration = duration
        self.remaining_time = duration

        self.init_ui()

        # Set up timer for duration countdown if applicable
        if duration and duration > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_duration)
            self.timer.start(1000)  # Update every second

    def init_ui(self):
        """Initialize the status indicator UI"""
        self.setFixedSize(60, 60)
        self.setFrameShape(QFrame.Box)

        # Get colors based on effect type
        colors = self.get_effect_colors()

        self.setStyleSheet(f"""
            StatusIndicator {{
                background-color: {colors['bg']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # Icon/emoji
        icon_label = QLabel(self.get_effect_icon())
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(icon_label)

        # Name (abbreviated if needed)
