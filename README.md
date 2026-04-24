# Python_gui_codex

A final Py GUI, user friendly.

This project ships with a polished desktop application built with PySide6 that
showcases many of the widgets, layouts, and interaction patterns you can use to
assemble a production-ready Python interface. The dashboard demonstrates
responsive layouts, a menu bar, and live previews to highlight modern GUI
practices.

## Features

- **Comprehensive widget selection** – Includes line edits, combo boxes,
  check boxes, radio buttons, sliders, and rich text areas to demonstrate core
  PySide6 widgets working together.
- **Event-driven updates** – Form submissions trigger a live summary panel while
  slider changes update helper labels instantly so users see immediate feedback.
- **Theming and polish** – Custom styling mimics a contemporary product surface,
  covering group boxes, buttons, and status bars for a cohesive look.
- **Menu actions and dialogs** – File/Help menus include reset, exit, and about
  actions to illustrate application-level event handling.

## Requirements

- Python 3.9 or newer
- [PySide6](https://doc.qt.io/qtforpython/) (Qt for Python)

Install dependencies with pip:

```bash
python -m pip install --upgrade pip
python -m pip install PySide6
```

## Running the application

Launch the dashboard with Python:

```bash
python main.py
```

The `run()` function in `main.py` is also import-safe, allowing the GUI to be
embedded in larger applications:

```python
from main import run

run()
```

## Using the dashboard

1. Populate the **User Information** section with a name, email, and preferred
   contact method.
2. Adjust the **Preferences** to pick a category, opt into updates, and select a
   priority with the slider.
3. Add optional context inside the **Notes** area.
4. Click **Submit Interaction** to preview a formatted summary in the right-hand
   panel. Use **Reset Form** or the **File → Reset Form** menu option to start
   over.

## Customizing the UI

- Tweak the color palette or typography by editing `_apply_theme()` inside
  `DashboardWindow`.
- Extend `FormPanel` to capture additional fields, and update
  `PreviewPanel.update_preview()` to render them.
- Integrate backend services by connecting to the `FormPanel.submitted` signal
  to persist or route the captured data.

Feel free to use this project as a template for building more specialized
PySide6 applications.
