"""Interactive PySide6 GUI demonstrating common widgets and event handling.

This module defines a polished desktop application that showcases how to assemble
many of the core components that make up a modern Qt-based interface. The
window combines input widgets, menus, layouts, and styling so it can be used as
an approachable starting point for PySide6 projects.
"""

from __future__ import annotations

from typing import Dict

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QRadioButton,
    QSlider,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class FormPanel(QWidget):
    """Collects user input and exposes submission/reset signals."""

    submitted: Signal = Signal(dict)
    reset_requested: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        self.setObjectName("FormPanel")

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter the user's full name")

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("name@example.com")

        self.category_combo = QComboBox()
        self.category_combo.addItems(
            [
                "General Inquiry",
                "Technical Support",
                "Product Feedback",
                "Partnership Opportunity",
            ]
        )

        self.subscribe_checkbox = QCheckBox("Subscribe to updates")
        self.subscribe_checkbox.setChecked(True)

        self.email_radio = QRadioButton("Email")
        self.phone_radio = QRadioButton("Phone")
        self.chat_radio = QRadioButton("Live Chat")

        self.contact_group = QButtonGroup(self)
        for button in (self.email_radio, self.phone_radio, self.chat_radio):
            self.contact_group.addButton(button)
        self.email_radio.setChecked(True)

        self.priority_slider = QSlider(Qt.Horizontal)
        self.priority_slider.setRange(1, 10)
        self.priority_slider.setValue(5)
        self.priority_value_label = QLabel(str(self.priority_slider.value()))
        self.priority_value_label.setObjectName("PriorityValue")

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Add any additional notes or context here…")

        self.submit_button = QPushButton("Submit Interaction")
        self.reset_button = QPushButton("Reset Form")
        self.reset_button.setObjectName("secondaryButton")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(14)

        info_group = QGroupBox("User Information")
        info_layout = QGridLayout()
        info_layout.setHorizontalSpacing(10)
        info_layout.setVerticalSpacing(8)
        info_group.setLayout(info_layout)

        info_layout.addWidget(QLabel("Full Name"), 0, 0)
        info_layout.addWidget(self.name_edit, 0, 1)

        info_layout.addWidget(QLabel("Email"), 1, 0)
        info_layout.addWidget(self.email_edit, 1, 1)

        info_layout.addWidget(QLabel("Preferred Contact"), 2, 0)
        contact_row = QHBoxLayout()
        contact_row.addWidget(self.email_radio)
        contact_row.addWidget(self.phone_radio)
        contact_row.addWidget(self.chat_radio)
        contact_row.addStretch()
        info_layout.addLayout(contact_row, 2, 1)

        preferences_group = QGroupBox("Preferences")
        preferences_layout = QGridLayout()
        preferences_layout.setHorizontalSpacing(10)
        preferences_layout.setVerticalSpacing(8)
        preferences_group.setLayout(preferences_layout)

        preferences_layout.addWidget(QLabel("Category"), 0, 0)
        preferences_layout.addWidget(self.category_combo, 0, 1)

        preferences_layout.addWidget(self.subscribe_checkbox, 1, 0, 1, 2)

        preferences_layout.addWidget(QLabel("Priority"), 2, 0)
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(self.priority_slider, stretch=1)
        priority_layout.addWidget(self.priority_value_label)
        preferences_layout.addLayout(priority_layout, 2, 1)

        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout()
        notes_group.setLayout(notes_layout)
        notes_layout.addWidget(self.notes_edit)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.reset_button)
        button_row.addWidget(self.submit_button)

        main_layout.addWidget(info_group)
        main_layout.addWidget(preferences_group)
        main_layout.addWidget(notes_group)
        main_layout.addLayout(button_row)

    def _connect_signals(self) -> None:
        self.priority_slider.valueChanged.connect(self._on_priority_changed)
        self.submit_button.clicked.connect(self._on_submit_clicked)
        self.reset_button.clicked.connect(self._on_reset_clicked)

    @Slot(int)
    def _on_priority_changed(self, value: int) -> None:
        self.priority_value_label.setText(str(value))

    @Slot()
    def _on_submit_clicked(self) -> None:
        data = self._collect_form_data()
        if not data["name"]:
            self._show_validation_error("Please provide the contact's name.")
            return
        if not data["email"]:
            self._show_validation_error("Please provide an email address.")
            return
        self.submitted.emit(data)

    @Slot()
    def _on_reset_clicked(self) -> None:
        self.reset_requested.emit()

    def _collect_form_data(self) -> Dict[str, str | int | bool]:
        selected_button = self.contact_group.checkedButton()
        contact_method = selected_button.text() if selected_button else "Email"
        return {
            "name": self.name_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "category": self.category_combo.currentText(),
            "subscribe": self.subscribe_checkbox.isChecked(),
            "priority": self.priority_slider.value(),
            "contact_method": contact_method,
            "notes": self.notes_edit.toPlainText().strip(),
        }

    def _show_validation_error(self, message: str) -> None:
        QMessageBox.warning(self, "Missing Information", message)

    def clear(self) -> None:
        self.name_edit.clear()
        self.email_edit.clear()
        self.category_combo.setCurrentIndex(0)
        self.subscribe_checkbox.setChecked(True)
        self.priority_slider.setValue(5)
        self.notes_edit.clear()
        self.email_radio.setChecked(True)
        self.priority_value_label.setText(str(self.priority_slider.value()))


class PreviewPanel(QWidget):
    """Displays an at-a-glance summary of the collected data."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._intro_text = (
            "Complete the form to preview a summary of the interaction. "
            "Details will appear here once the submission succeeds."
        )
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.title_label = QLabel("Interaction Overview")
        self.title_label.setObjectName("PreviewTitle")

        self.summary_display = QPlainTextEdit()
        self.summary_display.setReadOnly(True)
        self.summary_display.setPlainText(self._intro_text)

        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_display)

    def update_preview(self, data: Dict[str, str | int | bool]) -> None:
        subscribe_text = "Yes" if data["subscribe"] else "No"
        notes_section = data["notes"] or "(No additional notes provided.)"
        summary = (
            f"Name: {data['name']}\n"
            f"Email: {data['email']}\n"
            f"Category: {data['category']}\n"
            f"Preferred Contact: {data['contact_method']}\n"
            f"Priority: {data['priority']} / 10\n"
            f"Subscribed to Updates: {subscribe_text}\n\n"
            f"Notes:\n{notes_section}"
        )
        self.summary_display.setPlainText(summary)

    def clear(self) -> None:
        self.summary_display.setPlainText(self._intro_text)


class DashboardWindow(QMainWindow):
    """Main application window combining the form and preview widgets."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Customer Interaction Dashboard")
        self.resize(960, 640)

        self.form_panel = FormPanel()
        self.preview_panel = PreviewPanel()

        self._build_ui()
        self._create_menus()
        self._create_status_bar()
        self._connect_signals()
        self._apply_theme()

    def _build_ui(self) -> None:
        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(18)

        layout.addWidget(self.form_panel, stretch=3)
        layout.addWidget(self.preview_panel, stretch=4)

        self.setCentralWidget(central)

    def _create_menus(self) -> None:
        menu_bar: QMenuBar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        self.reset_action = file_menu.addAction("Reset Form")
        self.reset_action.setShortcut("Ctrl+R")
        file_menu.addSeparator()
        self.exit_action = file_menu.addAction("Exit")
        self.exit_action.setShortcut("Ctrl+Q")

        help_menu = menu_bar.addMenu("&Help")
        self.about_action = help_menu.addAction("About")

    def _create_status_bar(self) -> None:
        status = QStatusBar(self)
        status.showMessage("Ready")
        self.setStatusBar(status)

    def _connect_signals(self) -> None:
        self.form_panel.submitted.connect(self._handle_submission)
        self.form_panel.reset_requested.connect(self._handle_form_reset)

        self.reset_action.triggered.connect(self._clear_form_and_preview)
        self.exit_action.triggered.connect(self.close)
        self.about_action.triggered.connect(self._show_about_dialog)

    def _apply_theme(self) -> None:
        self.setStyleSheet(
            """
            QWidget {
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                font-size: 11pt;
                color: #1f2933;
            }
            QMainWindow {
                background-color: #f6f7fb;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #d8dee9;
                border-radius: 10px;
                margin-top: 12px;
                padding: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #344054;
                font-weight: 600;
            }
            QLineEdit, QPlainTextEdit, QComboBox {
                border: 1px solid #cfd8e3;
                border-radius: 6px;
                padding: 6px 8px;
                background: #ffffff;
            }
            QLineEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
                border-color: #6366f1;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.18);
            }
            QPlainTextEdit {
                min-height: 160px;
            }
            QPushButton {
                background-color: #4f46e5;
                border-radius: 6px;
                padding: 8px 18px;
                color: #ffffff;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
            QPushButton#secondaryButton {
                background-color: #e4e7ec;
                color: #1f2933;
            }
            QPushButton#secondaryButton:hover {
                background-color: #d2d6dc;
            }
            QLabel#PreviewTitle {
                font-size: 18pt;
                font-weight: 700;
                color: #101828;
            }
            QLabel#PriorityValue {
                min-width: 24px;
                font-weight: 600;
                qproperty-alignment: AlignCenter;
            }
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #d8dee9;
            }
            """
        )

    @Slot(dict)
    def _handle_submission(self, data: Dict[str, str | int | bool]) -> None:
        self.preview_panel.update_preview(data)
        self.statusBar().showMessage("Interaction submitted successfully.", 4000)

    @Slot()
    def _handle_form_reset(self) -> None:
        self._clear_form_and_preview()

    @Slot()
    def _clear_form_and_preview(self) -> None:
        self.form_panel.clear()
        self.preview_panel.clear()
        self.statusBar().showMessage("Form reset.", 3000)

    @Slot()
    def _show_about_dialog(self) -> None:
        QMessageBox.information(
            self,
            "About",
            (
                "This sample dashboard demonstrates how to assemble a polished "
                "PySide6 interface with responsive layouts, menu actions, and "
                "event-driven updates."
            ),
        )


def run() -> None:
    """Entrypoint used by scripts or packaging systems."""
    app = QApplication([])
    window = DashboardWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
