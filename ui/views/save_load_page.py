# -*- coding: utf-8 -*-
"""
Save/load game interface for PyRPG Adventure
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
                               QListWidgetItem, QPushButton, QFrame, QMessageBox,
                               QInputDialog, QGroupBox, QTextEdit, QDialog, QDialogButtonBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from ..theme import Theme
from ..widgets import Card, StyledButton
from datetime import datetime
import os


class SaveFileItem(QListWidgetItem):
    """Custom list item for save files with metadata"""

    def __init__(self, save_info):
        super().__init__()
        self.save_info = save_info
        self.update_display()

    def update_display(self):
        """Update the display text and formatting"""

        # Format last saved time
        last_saved = self.save_info.get('last_saved', 'Unknown')
        if last_saved != 'Unknown':
            try:
                # Parse ISO format and format nicely
                dt = datetime.fromisoformat(last_saved.replace('Z', '+00:00'))
                last_saved = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, AttributeError):
                pass

        # Create display text
        display_text = f"📁 {self.save_info.get('hero_name', 'Unknown')} - Lv.{self.save_info.get('hero_level', '?')} ({last_saved})"

        # Get subtitle info
        subtitle_info = []
        if self.save_info.get('hero_class'):
            subtitle_info.append(f"Class: {self.save_info.get('hero_class')}")
        if self.save_info.get('playtime', 0) > 0:
            play_hours = int(self.save_info.get('playtime', 0) / 3600)
            if play_hours > 0:
                subtitle_info.append(f"Playtime: {play_hours}h")
        if self.save_info.get('playtime', 0) < 3600:
            play_mins = int(self.save_info.get('playtime', 0) / 60)
            if play_mins > 0:
                subtitle_info.append(f"Playtime: {play_mins}m")

        subtitle = " | ".join(subtitle_info) if subtitle_info else "No additional info"

        # Set main text
        self.setText(display_text)

        # Set tooltip with additional info
        tooltip = f"""Slot: {self.save_info.get('slot', 'Unknown')}
Character: {self.save_info.get('hero_name', 'Unknown')}
Level: {self.save_info.get('hero_level', '1')}
{subtitle}
Last Saved: {last_saved}"""

        self.setToolTip(tooltip)

        # Style based on recent saves
        self.setForeground(Qt.white)

        # Mark as bold if this is a recent save (last 24 hours would be ideal, but we don't have creation time)


class SaveSlotDialog(QDialog):
    """Dialog for selecting new save slot name"""

    def __init__(self, existing_slots, parent=None):
        super().__init__(parent)
        self.existing_slots = existing_slots
        self.selected_slot = None
        self.init_ui()

    def init_ui(self):
        """Initialize the save slot dialog"""
        self.setWindowTitle("Create New Save")
        self.setModal(True)

        # Set fixed width
        self.setFixedWidth(400)
        self.setStyleSheet(f"background-color: {Theme.BACKGROUND}; color: {Theme.FOREGROUND};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)

        # Title
        title = QLabel("Enter Save Slot Name")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745;")
        layout.addWidget(title)

        # Info label
        info_label = QLabel("Choose a name for your save file. Use letters, numbers, spaces, hyphens, and underscores.")
        info_label.setStyleSheet(f"color: {Theme.FOREGROUND}; margin-bottom: 8px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Slot name input
        self.slot_input = QTextEdit()
        self.slot_input.setPlaceholderText("Enter slot name...")
        self.slot_input.setFixedHeight(60)
        self.slot_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Theme.CARD};
                border: 1px solid {Theme.BORDER};
                border-radius: 4px;
                padding: 8px;
                color: {Theme.FOREGROUND};
                font-size: 12px;
            }}
            QTextEdit:focus {{
                border-color: {Theme.PRIMARY};
            }}
        """)
        self.slot_input.textChanged.connect(self.validate_input)
        layout.addWidget(self.slot_input)

        # Validation label
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        layout.addWidget(self.validation_label)

        # Examples
        examples = QLabel("Examples: 'My Hero', 'Chapter 2', 'Boss Fight Pre'...")
        examples.setStyleSheet(f"color: {Theme.SECONDARY_TEXT}; font-size: 11px; font-style: italic;")
        layout.addWidget(examples)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_slot)
        button_box.rejected.connect(self.reject)

        # Customize button styles
        for button in button_box.buttons():
            button.setStyleSheet(StyledButton.get_button_style("primary" if button.text() == "OK" else "secondary"))

        layout.addWidget(button_box)

    def validate_input(self):
        """Validate the current input"""
        slot_name = self.slot_input.toPlainText().strip()

        # Check for existing slots
        if slot_name and slot_name in self.existing_slots:
            self.validation_label.setText("❌ Slot name already exists. Choose a different name.")
            return False

        # Check length
        if len(slot_name) > 50:
            self.validation_label.setText("❌ Slot name is too long (max 50 characters)")
            return False

        if len(slot_name) < 1:
            self.validation_label.setText("")
            return False

        # Check allowed characters
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
        if not all(c in valid_chars for c in slot_name):
            self.validation_label.setText("❌ Only letters, numbers, spaces, hyphens, and underscores allowed")
            return False

        self.validation_label.setText("✅ Valid slot name")
        return True

    def accept_slot(self):
        """Accept the dialog if validation passes"""
        if self.validate_input():
            self.selected_slot = self.slot_input.toPlainText().strip()
            self.accept()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid slot name.")


class OverwriteConfirmationDialog(QDialog):
    """Dialog to confirm overwriting an existing save"""

    def __init__(self, save_info, parent=None):
        super().__init__(parent)
        self.save_info = save_info
        self.confirmed = False
        self.init_ui()

    def init_ui(self):
        """Initialize the overwrite confirmation dialog"""
        self.setWindowTitle("Overwrite Save?")
        self.setModal(True)
        self.setFixedWidth(500)

        self.setStyleSheet(f"background-color: {Theme.BACKGROUND}; color: {Theme.FOREGROUND};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)

        # Warning icon and text
        warning_layout = QHBoxLayout()

        # Warning icon - text based since no image
        warning_label = QLabel("⚠️")
        warning_label.setStyleSheet("font-size: 48px;")
        warning_layout.addWidget(warning_label, alignment=Qt.AlignCenter)

        text_layout = QVBoxLayout()

        # Main warning text
        main_text = f"Are you sure you want to overwrite '{self.save_info.get('slot', 'Unknown')}'?"
        main_label = QLabel(main_text)
        main_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffc107; margin-bottom: 8px;")
        text_layout.addWidget(main_label)

        # Save info
        name_level = f"Character: {self.save_info.get('hero_name', 'Unknown')} (Level {self.save_info.get('hero_level', '1')})"
        save_info_label = QLabel(name_level)
        save_info_label.setStyleSheet(f"color: {Theme.FOREGROUND}; margin-bottom: 4px;")
        text_layout.addWidget(save_info_label)

        last_saved = self.save_info.get('last_saved', 'Unknown')
        if last_saved != 'Unknown':
            try:
                dt = datetime.fromisoformat(last_saved.replace('Z', '+00:00'))
                last_saved = dt.strftime("%A, %B %d, %Y at %I:%M %p")
            except (ValueError, AttributeError):
                pass

        last_saved_label = QLabel(f"Last saved: {last_saved}")
        last_saved_label.setStyleSheet(f"color: {Theme.SECONDARY_TEXT}; font-style: italic;")
        text_layout.addWidget(last_saved_label)

        warning_layout.addLayout(text_layout)
        layout.addLayout(warning_layout)

        # Instruction text
        instruction = QLabel("This action cannot be undone. Make sure you have a backup if needed.")
        instruction.setStyleSheet(f"color: {Theme.SECONDARY_TEXT}; font-style: italic; margin-top: 12px;")
        instruction.setWordWrap(True)
        layout.addWidget(instruction)

        # Buttons
        layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(Theme.SPACING_MD)

        cancel_btn = StyledButton("Cancel", variant="secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        overwrite_btn = StyledButton("🗑️ Overwrite", variant="danger")
        overwrite_btn.clicked.connect(self.confirm_overwrite)
        button_layout.addWidget(overwrite_btn)

        layout.addLayout(button_layout)

    def confirm_overwrite(self):
        """Confirm the overwrite action"""
        self.confirmed = True
        self.accept()


class SaveLoadPage(QWidget):
    """Main save/load interface page"""

    # Signals to controller
    save_requested = Signal(str)  # slot_name
    load_requested = Signal(str)  # slot_name
    delete_requested = Signal(str)  # slot_name

    def __init__(self, parent=None):
        super().__init__(parent)
        self.save_files = []
        self.init_ui()

    def init_ui(self):
        """Initialize the save/load page UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG, Theme.MARGIN_LG)
        main_layout.setSpacing(Theme.SPACING_LG)

        # Header
        header = Card()
        header_layout = QVBoxLayout()

        title = QLabel("💾 Save & Load Game")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #28a745;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)

        subtitle = QLabel("Manage your game progress and explore different paths")
        subtitle.setStyleSheet(f"color: {Theme.SECONDARY_TEXT}; font-style: italic;")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)

        header.main_layout.addLayout(header_layout)
        main_layout.addWidget(header)

        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(Theme.SPACING_LG)

        # Left side: Save files list
        saves_section = Card()
        saves_section.setFixedWidth(500)
        saves_layout = QVBoxLayout()

        saves_title = QLabel("📁 Save Files")
        saves_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #007bff;")
        saves_layout.addWidget(saves_title)

        # Save files list
        self.saves_list = QListWidget()
        self.saves_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Theme.CARD};
                border: 1px solid {Theme.BORDER};
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {Theme.BORDER};
                background-color: transparent;
            }}
            QListWidget::item:selected {{
                background-color: {Theme.PRIMARY};
            }}
            QListWidget::item:hover {{
                background-color: {Theme.HOVER};
            }}
        """)

        # Connect double-click to load
        self.saves_list.itemDoubleClicked.connect(self.on_save_double_clicked)

        saves_layout.addWidget(self.saves_list)

        # List controls
        list_controls = QHBoxLayout()
        list_controls.setSpacing(Theme.SPACING_MD)

        refresh_btn = StyledButton("🔄 Refresh", variant="secondary", size="small")
        refresh_btn.clicked.connect(lambda: self.refresh_requested.emit())
        list_controls.addWidget(refresh_btn)

        list_controls.addStretch()

        self.delete_btn = StyledButton("🗑️ Delete", variant="danger", size="small")
        self.delete_btn.clicked.connect(self.on_delete_requested)
        self.delete_btn.setEnabled(False)
        list_controls.addWidget(self.delete_btn)

        saves_layout.addLayout(list_controls)

        saves_section.main_layout.addLayout(saves_layout)
        content_layout.addWidget(saves_section)

        # Right side: Actions
        actions_section = Card()
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(Theme.SPACING_LG)

        actions_title = QLabel("🎮 Game Actions")
        actions_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #17a2b8;")
        actions_layout.addWidget(actions_title)

        # Quick save/load
        quick_actions = Card()
        qa_layout = QVBoxLayout()

        qa_title = QLabel("Quick Actions")
        qa_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffc107;")
        qa_layout.addWidget(qa_title)

        self.quick_save_btn = StyledButton("⚡ Quick Save", variant="primary")
        self.quick_save_btn.clicked.connect(self.on_quick_save)
        self.quick_save_btn.setToolTip("Save to 'quick' slot")
        qa_layout.addWidget(self.quick_save_btn)

        self.quick_load_btn = StyledButton("⚡ Quick Load", variant="primary")
        self.quick_load_btn.clicked.connect(self.on_quick_load)
        self.quick_load_btn.setToolTip("Load from 'quick' slot")
        qa_layout.addWidget(self.quick_load_btn)

        quick_actions.main_layout.addLayout(qa_layout)
        actions_layout.addWidget(quick_actions)

        # Selected save actions
        selected_actions = Card()
        sa_layout = QVBoxLayout()

        sa_title = QLabel("Selection Actions")
        sa_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #dc3545;")
        sa_layout.addWidget(sa_title)

        self.save_selected_btn = StyledButton("💾 Save Over Selection", variant="success")
        self.save_selected_btn.clicked.connect(self.on_save_selected)
        self.save_selected_btn.setEnabled(False)
        self.save_selected_btn.setToolTip("Overwrite the currently selected save file")
        sa_layout.addWidget(self.save_selected_btn)

        self.load_selected_btn = StyledButton("📁 Load Selection", variant="info")
        self.load_selected_btn.clicked.connect(self.on_load_selected)
        self.load_selected_btn.setEnabled(False)
        self.load_selected_btn.setToolTip("Load the currently selected save file")
        sa_layout.addWidget(self.load_selected_btn)

        selected_actions.main_layout.addLayout(sa_layout)
        actions_layout.addWidget(selected_actions)

        # New save
        new_save_actions = Card()
        ns_layout = QVBoxLayout()

        ns_title = QLabel("Create New Save")
        ns_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #6f42c1;")
        ns_layout.addWidget(ns_title)

        self.new_save_btn = StyledButton("🆕 New Save Slot", variant="primary", size="large")
        self.new_save_btn.clicked.connect(self.on_new_save)
        self.new_save_btn.setToolTip("Create a new save file with custom name")
        ns_layout.addWidget(self.new_save_btn)

        new_save_actions.main_layout.addLayout(ns_layout)
        actions_layout.addWidget(new_save_actions)

        actions_section.main_layout.addLayout(actions_layout)
        content_layout.addWidget(actions_section)

        main_layout.addLayout(content_layout)

        # Connect selection changes
        self.saves_list.itemSelectionChanged.connect(self.on_selection_changed)

        # Connect refresh signal (will be connected to controller)
        self.refresh_requested = Signal()  # Request to refresh save list

    def update_save_files(self, save_files):
        """Update the list of save files"""
        self.save_files = save_files
        self.saves_list.clear()

        for save_info in save_files:
            item = SaveFileItem(save_info)
            self.saves_list.addItem(item)

    def get_selected_save_info(self):
        """Get the currently selected save file info"""
        current_item = self.saves_list.currentItem()
        if current_item and hasattr(current_item, 'save_info'):
            return current_item.save_info
        return None

    def on_selection_changed(self):
        """Handle save file selection changes"""
        selected = self.get_selected_save_info()

        # Enable/disable buttons based on selection
        has_selection = selected is not None
        self.save_selected_btn.setEnabled(has_selection)
        self.load_selected_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def on_save_double_clicked(self, item):
        """Handle double-click on save file (load)"""
        if hasattr(item, 'save_info'):
            slot_name = item.save_info.get('slot')
            if slot_name:
                # Confirm load action
                result = QMessageBox.question(
                    self, "Load Game?",
                    f"Do you want to load '{slot_name}'?\n\nAny unsaved progress will be lost.",
                    QMessageBox.Yes | QMessageBox.No
                )

                if result == QMessageBox.Yes:
                    self.load_requested.emit(slot_name)

    def on_quick_save(self):
        """Handle quick save button"""
        # Ask for confirmation only if we're overwriting
        if self.has_quick_save():
            result = QMessageBox.question(
                self, "Overwrite Quick Save?",
                "A quick save already exists. Overwrite it?",
                QMessageBox.Yes | QMessageBox.No
            )
            if result != QMessageBox.Yes:
                return

        self.save_requested.emit("quick")

    def on_quick_load(self):
        """Handle quick load button"""
        if not self.has_quick_save():
            QMessageBox.information(self, "No Quick Save", "No quick save file found.")
            return

        result = QMessageBox.question(
            self, "Load Quick Save?",
            "Load from quick save?\n\nAny unsaved progress will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:
            self.load_requested.emit("quick")

    def on_save_selected(self):
        """Handle save over selected file"""
        save_info = self.get_selected_save_info()
        if not save_info:
            return

        # Confirm overwrite
        dialog = OverwriteConfirmationDialog(save_info, self)
        result = dialog.exec()
        if result == QDialog.Accepted and dialog.confirmed:
            self.save_requested.emit(save_info['slot'])

    def on_load_selected(self):
        """Handle load selected file"""
        save_info = self.get_selected_save_info()
        if not save_info:
            return

        # Confirm load action
        result = QMessageBox.question(
            self, "Load Game?",
            f"Do you want to load '{save_info['slot']}'?\n\nAny unsaved progress will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:
            self.load_requested.emit(save_info['slot'])

    def on_delete_requested(self):
        """Handle delete button"""
        save_info = self.get_selected_save_info()
        if not save_info:
            return

        # Confirm delete action
        result = QMessageBox.question(
            self, "Delete Save?",
            f"Are you sure you want to delete '{save_info['slot']}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Default to No for safety
        )

        if result == QMessageBox.Yes:
            self.delete_requested.emit(save_info['slot'])

    def on_new_save(self):
        """Handle create new save button"""
        # Get existing slot names
        existing_slots = [save['slot'] for save in self.save_files]

        dialog = SaveSlotDialog(existing_slots, self)
        result = dialog.exec()

        if result == QDialog.Accepted and dialog.selected_slot:
            self.save_requested.emit(dialog.selected_slot)

    def has_quick_save(self):
        """Check if a quick save exists"""
        quick_saves = [save for save in self.save_files if save.get('slot') == 'quick']
        return len(quick_saves) > 0

    def show_save_success(self, slot_name):
        """Show save success message"""
        QMessageBox.information(self, "Save Successful", f"Game saved successfully to slot '{slot_name}'!")

    def show_save_error(self, slot_name, error_msg):
        """Show save error message"""
        QMessageBox.critical(self, "Save Failed", f"Failed to save to slot '{slot_name}':\n\n{error_msg}")

    def show_load_success(self, slot_name):
        """Show load success message"""
        QMessageBox.information(self, "Load Successful", f"Game loaded successfully from slot '{slot_name}'!")

    def show_load_error(self, slot_name, error_msg):
        """Show load error message"""
        QMessageBox.critical(self, "Load Failed", f"Failed to load from slot '{slot_name}':\n\n{error_msg}")

    def show_delete_success(self, slot_name):
        """Show delete success message"""
        QMessageBox.information(self, "Delete Successful", f"Save slot '{slot_name}' deleted successfully!")

    def show_delete_error(self, slot_name, error_msg):
        """Show delete error message"""
        QMessageBox.critical(self, "Delete Failed", f"Failed to delete save slot '{slot_name}':\n\n{error_msg}")
