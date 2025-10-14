# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

class StatsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("\U0001f4ca Hero Statistics")
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