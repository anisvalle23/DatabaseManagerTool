import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLibraryInfo
from ui.login_window import LoginWindow

app = QApplication(sys.argv)

translator = QTranslator()
translator.load("qt_es", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath))
app.installTranslator(translator)

app.setStyleSheet("""
    QWidget {
        background-color: #F5EFE6;
        color: #3B1A1A;
        font-family: Arial;
        font-size: 13px;
    }

    QMainWindow {
        background-color: #F5EFE6;
    }

    QLabel {
        color: #3B1A1A;
        font-weight: bold;
    }

    QLineEdit, QTextEdit {
        background-color: #FDF8F2;
        border: 1px solid #C9A84C;
        border-radius: 4px;
        padding: 5px;
        color: #3B1A1A;
    }

    QLineEdit:focus, QTextEdit:focus {
        border: 2px solid #722F37;
    }

    QPushButton {
        background-color: #722F37;
        color: #F5EFE6;
        border: none;
        border-radius: 4px;
        padding: 7px 14px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #8B3A45;
    }

    QPushButton:pressed {
        background-color: #4F1F25;
    }

    QTreeWidget {
        background-color: #FDF8F2;
        border: 1px solid #C9A84C;
        border-radius: 4px;
    }

    QTreeWidget::item:selected {
        background-color: #722F37;
        color: #F5EFE6;
    }

    QTreeWidget::item:hover {
        background-color: #EDD9A3;
    }

    QTreeWidget QHeaderView::section {
        background-color: #722F37;
        color: #F5EFE6;
        font-weight: bold;
        padding: 4px;
        border: none;
    }

    QTabWidget::pane {
        border: 1px solid #C9A84C;
        border-radius: 4px;
        background-color: #FDF8F2;
    }

    QTabBar::tab {
        background-color: #EDD9A3;
        color: #3B1A1A;
        padding: 6px 18px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        margin-right: 2px;
        font-weight: bold;
    }

    QTabBar::tab:selected {
        background-color: #722F37;
        color: #F5EFE6;
    }

    QTabBar::tab:hover {
        background-color: #C9A84C;
        color: #FDF8F2;
    }

    QTableWidget {
        background-color: #FDF8F2;
        border: 1px solid #C9A84C;
        gridline-color: #EDD9A3;
    }

    QTableWidget::item:selected {
        background-color: #722F37;
        color: #F5EFE6;
    }

    QHeaderView::section {
        background-color: #722F37;
        color: #F5EFE6;
        font-weight: bold;
        padding: 5px;
        border: none;
    }

    QListWidget {
        background-color: #FDF8F2;
        border: 1px solid #C9A84C;
        border-radius: 4px;
    }

    QListWidget::item:selected {
        background-color: #722F37;
        color: #F5EFE6;
    }

    QListWidget::item:hover {
        background-color: #EDD9A3;
    }

    QComboBox {
        background-color: #FDF8F2;
        border: 1px solid #C9A84C;
        border-radius: 4px;
        padding: 4px;
        color: #3B1A1A;
    }

    QComboBox:focus {
        border: 2px solid #722F37;
    }

    QComboBox QAbstractItemView {
        background-color: #FDF8F2;
        selection-background-color: #722F37;
        selection-color: #F5EFE6;
    }

    QScrollBar:vertical {
        background: #EDD9A3;
        width: 10px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical {
        background: #722F37;
        border-radius: 5px;
    }

    QScrollBar:horizontal {
        background: #EDD9A3;
        height: 10px;
        border-radius: 5px;
    }

    QScrollBar::handle:horizontal {
        background: #722F37;
        border-radius: 5px;
    }

    QMessageBox {
        background-color: #F5EFE6;
    }

    QSplitter::handle {
        background-color: #C9A84C;
        width: 2px;
    }
""")

window = LoginWindow()
window.show()
sys.exit(app.exec())
