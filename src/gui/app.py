from __future__ import annotations

from typing import Callable

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.config import APP_TITLE


class App(QMainWindow):
    """Root window — swaps its central widget to navigate between views."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(560, 480)
        self.setMinimumSize(420, 360)
        self._show_menu()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _show_menu(self) -> None:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(14)

        title = QLabel("Puzzle Game")
        title.setFont(QFont("Helvetica Neue", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(16)

        for text, view_fn in [
            ("Sudoku",      self._open_sudoku),
            ("Maze",        self._open_maze),
            ("Word Ladder", self._open_word_ladder),
        ]:
            btn = QPushButton(text)
            btn.setFixedWidth(220)
            btn.setFixedHeight(46)
            btn.clicked.connect(view_fn)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self._set_central(widget)

    def _open_sudoku(self) -> None:
        from src.gui.sudoku_view import SudokuView
        self._set_central(SudokuView(back=self._show_menu))

    def _open_maze(self) -> None:
        from src.gui.maze_view import MazeView
        self._set_central(MazeView(back=self._show_menu))

    def _open_word_ladder(self) -> None:
        from src.gui.word_ladder_view import WordLadderView
        self._set_central(WordLadderView(back=self._show_menu))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_central(self, widget: QWidget) -> None:
        old = self.centralWidget()
        self.setCentralWidget(widget)
        if old is not None:
            old.deleteLater()
