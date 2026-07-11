"""Тёмная тема приложения (QSS)."""

STYLE = """
QMainWindow, #root {
    background-color: #0f1117;
}

QLabel {
    color: #e6e9ef;
    font-family: 'Segoe UI';
}

#appTitle {
    font-size: 20px;
    font-weight: 700;
    color: #f2f4f8;
}

#accentDot {
    color: #4dd0e1;
    font-size: 22px;
    font-weight: 700;
}

#subLabel {
    color: #8b93a7;
    font-size: 12px;
}

#uptimeValue {
    color: #4dd0e1;
    font-size: 13px;
    font-weight: 600;
}

#header {
    background-color: #161923;
    border-radius: 14px;
}

#sectionCard {
    background-color: #161923;
    border-radius: 14px;
}

#sectionTitle {
    color: #aab2c5;
    font-size: 12px;
    font-weight: 600;
    padding: 2px;
}

QTableWidget {
    background-color: transparent;
    color: #d4d9e4;
    border: none;
    gridline-color: transparent;
    font-family: 'Segoe UI';
    font-size: 12px;
    outline: none;
}

QTableWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid #20242f;
}

QTableWidget::item:selected {
    background-color: #22303c;
    color: #ffffff;
}

QHeaderView::section {
    background-color: transparent;
    color: #6b7385;
    border: none;
    border-bottom: 1px solid #2a2f3d;
    padding: 6px 8px;
    font-weight: 600;
    text-align: left;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #2a2f3d;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #3a4152;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}
"""
