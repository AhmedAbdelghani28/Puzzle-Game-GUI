import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from src.gui.app import App


def _dark_palette() -> QPalette:
    palette = QPalette()
    dark    = QColor(45,  45,  45)
    darker  = QColor(30,  30,  30)
    blue    = QColor(42,  130, 218)

    palette.setColor(QPalette.ColorRole.Window,          dark)
    palette.setColor(QPalette.ColorRole.WindowText,      Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base,            darker)
    palette.setColor(QPalette.ColorRole.AlternateBase,   dark)
    palette.setColor(QPalette.ColorRole.ToolTipBase,     darker)
    palette.setColor(QPalette.ColorRole.ToolTipText,     Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text,            Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button,          dark)
    palette.setColor(QPalette.ColorRole.ButtonText,      Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText,      Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link,            blue)
    palette.setColor(QPalette.ColorRole.Highlight,       blue)
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    return palette


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")          # consistent cross-platform look
    app.setPalette(_dark_palette())
    app.setStyleSheet("""
        QPushButton {
            background-color: #1f6aa5;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 14px;
            min-height: 34px;
        }
        QPushButton:hover   { background-color: #1a5a8f; }
        QPushButton:pressed { background-color: #144d7a; }
        QPushButton:disabled { background-color: #444; color: #888; }

        QComboBox {
            background-color: #1f6aa5;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 13px;
            min-height: 30px;
            min-width: 110px;
        }
        QComboBox::drop-down { border: none; }
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: white;
            selection-background-color: #1f6aa5;
            border: 1px solid #555;
        }

        QFrame[frameShape="1"] {
            border: 1px solid #444;
            border-radius: 6px;
        }
    """)

    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
