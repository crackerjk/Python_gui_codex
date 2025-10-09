"""Customer interaction dashboard implemented with PySide6.

The application demonstrates how common Qt widgets, layouts, and events can be
combined to deliver a polished desktop experience. It is intentionally
self-contained so it can act as a reference implementation when starting new
projects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction, QCloseEvent
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


@dataclass(slots=True)
class InteractionData:
    """Container for the values captured by the form widget."""

    name: str
    email: str
    category: str
    contact_method: str
    subscribe: bool
    priority: int
    notes: str

    def to_display_text(self) -> str:
        subscribe_text = "Yes" if self.subscribe else "No"
        notes_text = self.notes or "(No additional notes provided.)"
        return (
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Category: {self.category}\n"
            f"Preferred Contact: {self.contact_method}\n"
            f"Priority: {self.priority} / 10\n"
            f"Subscribed to Updates: {subscribe_text}\n\n"
            f"Notes:\n{notes_text}"
        )


class InteractionForm(QWidget):
    """Collects user input and communicates changes through Qt signals."""

    submitted: Signal = Signal(dict)
    cleared: Signal = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Full name")

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

        self.email_radio = QRadioButton("Email")
        self.phone_radio = QRadioButton("Phone")
        self.chat_radio = QRadioButton("Live Chat")

        self.contact_group = QButtonGroup(self)
        for button in (self.email_radio, self.phone_radio, self.chat_radio):
            self.contact_group.addButton(button)
        self.email_radio.setChecked(True)

        self.subscribe_checkbox = QCheckBox("Subscribe to updates")
        self.subscribe_checkbox.setChecked(True)

        self.priority_slider = QSlider(Qt.Horizontal)
        self.priority_slider.setRange(1, 10)
        self.priority_slider.setValue(5)
        self.priority_value_label = QLabel(str(self.priority_slider.value()))
        self.priority_value_label.setObjectName("PriorityValue")

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Add any additional context here…")

        self.submit_button = QPushButton("Submit Interaction")
        self.reset_button = QPushButton("Reset Form")
        self.reset_button.setObjectName("secondaryButton")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(14)

        info_group = QGroupBox("User Information")
        info_layout = QGridLayout()
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
        contact_row.addStretch(1)
        info_layout.addLayout(contact_row, 2, 1)

        preferences_group = QGroupBox("Preferences")
        preferences_layout = QGridLayout()
        preferences_group.setLayout(preferences_layout)
        preferences_layout.addWidget(QLabel("Category"), 0, 0)
        preferences_layout.addWidget(self.category_combo, 0, 1)
        preferences_layout.addWidget(self.subscribe_checkbox, 1, 0, 1, 2)
        preferences_layout.addWidget(QLabel("Priority"), 2, 0)
        slider_row = QHBoxLayout()
        slider_row.addWidget(self.priority_slider, stretch=1)
        slider_row.addWidget(self.priority_value_label)
        preferences_layout.addLayout(slider_row, 2, 1)

        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(self.notes_edit)
        notes_group.setLayout(notes_layout)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        button_row.addWidget(self.reset_button)
        button_row.addWidget(self.submit_button)

        main_layout.addWidget(info_group)
        main_layout.addWidget(preferences_group)
        main_layout.addWidget(notes_group)
        main_layout.addLayout(button_row)

    def _connect_signals(self) -> None:
        self.priority_slider.valueChanged.connect(self._update_priority_label)
        self.submit_button.clicked.connect(self._handle_submit)
        self.reset_button.clicked.connect(self._handle_reset)

    @Slot(int)
    def _update_priority_label(self, value: int) -> None:
        self.priority_value_label.setText(str(value))

    @Slot()
    def _handle_submit(self) -> None:
        data = self._collect_data()
        if not data["name"]:
            self._show_validation_error("Please provide a name before submitting.")
            return
        if not data["email"]:
            self._show_validation_error("Please provide an email address.")
            return
        self.submitted.emit(data)

    @Slot()
    def _handle_reset(self) -> None:
        self.clear()
        self.cleared.emit()

    def _collect_data(self) -> Dict[str, str | int | bool]:
        checked_button = self.contact_group.checkedButton()
        contact_method = checked_button.text() if checked_button else "Email"
        return {
            "name": self.name_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "category": self.category_combo.currentText(),
            "contact_method": contact_method,
            "subscribe": self.subscribe_checkbox.isChecked(),
            "priority": self.priority_slider.value(),
            "notes": self.notes_edit.toPlainText().strip(),
        }

    def _show_validation_error(self, message: str) -> None:
        QMessageBox.warning(self, "Missing Information", message)

    def clear(self) -> None:
        self.name_edit.clear()
        self.email_edit.clear()
        self.category_combo.setCurrentIndex(0)
        self.email_radio.setChecked(True)
        self.subscribe_checkbox.setChecked(True)
        self.priority_slider.setValue(5)
        self.notes_edit.clear()
        self.priority_value_label.setText(str(self.priority_slider.value()))


class SummaryPanel(QWidget):
    """Displays a formatted representation of submitted data."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._empty_text = (
            "Complete the form to preview a summary of the interaction. "
            "Submitted details appear here."
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
        self.summary_display.setPlainText(self._empty_text)

        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_display)

    def update_summary(self, data: InteractionData) -> None:
        self.summary_display.setPlainText(data.to_display_text())

    def clear(self) -> None:
        self.summary_display.setPlainText(self._empty_text)


class DashboardWindow(QMainWindow):
    """Main window that hosts the form and summary panels."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Customer Interaction Dashboard")
        self.resize(960, 640)

        self.form_panel = InteractionForm()
        self.summary_panel = SummaryPanel()

        self._build_ui()
        self._create_menus()
        self._create_status_bar()
        self._connect_signals()
        self._apply_styles()

    def _build_ui(self) -> None:
        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(18)
        layout.addWidget(self.form_panel, stretch=3)
        layout.addWidget(self.summary_panel, stretch=4)
        self.setCentralWidget(central)

    def _create_menus(self) -> None:
        menu_bar: QMenuBar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        self.reset_action = QAction("Reset Form", self)
        self.reset_action.setShortcut("Ctrl+R")
        file_menu.addAction(self.reset_action)
        file_menu.addSeparator()
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(self.exit_action)

        help_menu = menu_bar.addMenu("&Help")
        self.about_action = QAction("About", self)
        help_menu.addAction(self.about_action)

    def _create_status_bar(self) -> None:
        status = QStatusBar(self)
        status.showMessage("Ready")
        self.setStatusBar(status)

    def _connect_signals(self) -> None:
        self.form_panel.submitted.connect(self._handle_submission)
        self.form_panel.cleared.connect(self._handle_cleared)
        self.reset_action.triggered.connect(self._trigger_reset)
        self.exit_action.triggered.connect(self.close)
        self.about_action.triggered.connect(self._show_about_dialog)

    def _apply_styles(self) -> None:
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
        interaction = InteractionData(**data)
        self.summary_panel.update_summary(interaction)
        self.statusBar().showMessage("Interaction submitted successfully.", 4000)

    @Slot()
    def _handle_cleared(self) -> None:
        self.summary_panel.clear()
        self.statusBar().showMessage("Form reset.", 3000)

    @Slot()
    def _trigger_reset(self) -> None:
        self.form_panel.clear()
        self.summary_panel.clear()
        self.statusBar().showMessage("Form reset.", 3000)

    @Slot()
    def _show_about_dialog(self) -> None:
        QMessageBox.information(
            self,
            "About",
            (
                "This dashboard showcases how to combine widgets, layouts, and "
                "Qt signals in a PySide6 application."
            ),
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.statusBar().showMessage("Closing application…", 1000)
        super().closeEvent(event)


def run() -> None:
    """Launch the dashboard."""
    app = QApplication([])
    window = DashboardWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
