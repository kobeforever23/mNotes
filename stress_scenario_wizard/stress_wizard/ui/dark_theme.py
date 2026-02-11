from __future__ import annotations


DARK_STYLESHEET = """
QWidget {
    background-color: #0f1724;
    color: #d7deee;
    font-family: "Segoe UI";
    font-size: 11px;
}
QMainWindow, QDialog {
    background-color: #0b1220;
}
QTabWidget::pane {
    border: 1px solid #233047;
    background: #111a2a;
}
QTabBar::tab {
    background: #142238;
    color: #a9b4c7;
    padding: 6px 12px;
    margin-right: 2px;
    border: 1px solid #20324f;
}
QTabBar::tab:selected {
    background: #1d3454;
    color: #f4f8ff;
}
QGroupBox {
    border: 1px solid #2b3f61;
    margin-top: 8px;
    padding-top: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
    color: #90caf9;
}
QPushButton {
    background-color: #1f3557;
    border: 1px solid #2f4f7e;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #28456f;
}
QPushButton:pressed {
    background-color: #19324f;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateTimeEdit {
    background-color: #0d1727;
    border: 1px solid #2b3f61;
    border-radius: 4px;
    padding: 4px;
}
QTableView {
    gridline-color: #1f2c45;
    selection-background-color: #275b8f;
    selection-color: #ffffff;
    alternate-background-color: #121f33;
}
QHeaderView::section {
    background-color: #1b2f4a;
    color: #d7deee;
    border: 1px solid #223956;
    padding: 4px;
}
QStatusBar {
    background: #101a2a;
    color: #a8c0de;
}
QProgressBar {
    border: 1px solid #2b3f61;
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #2c9f77;
}
"""
