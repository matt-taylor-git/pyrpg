# -*- coding: utf-8 -*-
"""
Modern log display component replacing QTextEdit for better performance and UX.
Uses QLabel with rich text formatting instead of QTextEdit for logs.
"""
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt
from ..theme import Theme


class LogEntry:
    """Represents a single log entry with formatting and timestamp"""

    def __init__(self, message, message_type="info", timestamp=None):
        self.message = message
        self.message_type = message_type  # "info", "success", "warning", "error", "combat"
        self.timestamp = timestamp

    def get_border_color(self):
        """Get the border color for this message type"""
        type_colors = {
            "info": Theme.MUTED_FOREGROUND.name(),
            "success": "#28a745",
            "warning": "#ffc107",
            "error": Theme.DESTRUCTIVE.name(),
            "combat": Theme.PRIMARY.name()
        }
        return type_colors.get(self.message_type, Theme.MUTED_FOREGROUND.name())


class LogDisplay(QWidget):
    """Modern log display using QLabel instead of QTextEdit for better performance"""

    def __init__(self, max_entries=20, parent=None):
        super().__init__(parent)
        self.log_entries = []
        self.max_entries = max_entries
        self.init_ui()

    def init_ui(self):
        """Initialize the log display UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Scroll area for log entries
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setMinimumHeight(150)
        self.scroll_area.setMaximumHeight(400)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Container for log entries
        self.entries_container = QWidget()
        self.entries_layout = QVBoxLayout(self.entries_container)
        self.entries_layout.setContentsMargins(10, 10, 10, 10)
        self.entries_layout.setSpacing(8)
        self.entries_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.entries_layout.addStretch()  # Push entries to top

        self.scroll_area.setWidget(self.entries_container)
        layout.addWidget(self.scroll_area)

        # Apply theme-consistent styling
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 2px solid {Theme.BORDER};
                border-radius: {Theme.BORDER_RADIUS_MD}px;
                background-color: {Theme.CARD};
            }}
            QScrollBar:vertical {{
                width: {Theme.SCROLLBAR_WIDTH}px;
                background: {Theme.CARD};
            }}
            QScrollBar::handle:vertical {{
                background: {Theme.BORDER};
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Theme.MUTED_FOREGROUND};
            }}
        """)

    def add_entry(self, message, message_type="info"):
        """Add a new log entry"""
        # Create entry and add to collection
        entry = LogEntry(message, message_type)
        self.log_entries.append(entry)

        # Maintain max entries limit
        if len(self.log_entries) > self.max_entries:
            # Remove oldest entries
            entries_to_remove = len(self.log_entries) - self.max_entries
            for _ in range(entries_to_remove):
                old_entry = self.log_entries.pop(0)
                # Remove from layout if widget exists
                if hasattr(old_entry, '_widget'):
                    old_entry._widget.setParent(None)
                    old_entry._widget.deleteLater()

        # Create and add visual widget for this entry
        self._add_entry_widget(entry)

        # Scroll to bottom to show newest entries
        self._scroll_to_bottom()

    def _add_entry_widget(self, entry):
        """Add a visual widget for the log entry"""
        # Create label for this entry
        entry_label = QLabel()
        entry_label.setTextFormat(Qt.TextFormat.RichText)
        entry_label.setWordWrap(True)
        entry_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Format the entry with CSS styling
        border_color = entry.get_border_color()
        formatted_text = f"""
        <div style='
            border-left: 3px solid {border_color};
            padding-left: 8px;
            margin: 4px 0;
            color: {Theme.FOREGROUND.name()};
            font-size: 13px;
            line-height: 1.5;
            background-color: transparent;
        '>
            {entry.message}
        </div>
        """

        entry_label.setText(formatted_text)

        # Store reference to widget for cleanup
        entry._widget = entry_label

        # Add to layout (insert before the stretch)
        self.entries_layout.insertWidget(self.entries_layout.count() - 1, entry_label)

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the log to show newest entries"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_entries(self):
        """Clear all log entries"""
        # Remove all entry widgets
        for i in range(self.entries_layout.count() - 1, -1, -1):  # Skip stretch item
            item = self.entries_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()

        # Clear entries list
        self.log_entries.clear()

    def get_entry_count(self):
        """Get current number of log entries"""
        return len(self.log_entries)
