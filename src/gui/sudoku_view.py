from __future__ import annotations

import copy
from typing import Callable, List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator

from src.config import Difficulty, SUDOKU_SIZE
from src.gui._worker import Worker
from src.puzzles.sudoku import SudokuGenerator, SudokuSolver

Board = List[List[int]]


class SudokuView(QWidget):
    def __init__(self, back: Callable[[], None]) -> None:
        super().__init__()
        self._back = back
        self._entries: List[List[QLineEdit]] = []
        self._original: Board = []
        self._worker: Optional[Worker] = None
        self._build_ui()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        root.setSpacing(10)
        root.setContentsMargins(20, 20, 20, 20)

        # Title + difficulty
        top = QHBoxLayout()
        title = QLabel("Sudoku")
        title.setFont(QFont("Helvetica Neue", 22, QFont.Weight.Bold))
        top.addWidget(title)
        top.addStretch()

        self._difficulty = QComboBox()
        self._difficulty.addItems(["Easy", "Medium", "Hard"])
        self._difficulty.setCurrentText("Medium")
        self._difficulty.currentTextChanged.connect(lambda _: self._new_game())
        top.addWidget(self._difficulty)
        root.addLayout(top)

        # Grid
        self._grid_frame = QFrame()
        self._grid_frame.setFrameShape(QFrame.Shape.StyledPanel)
        root.addWidget(self._grid_frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        for text, slot in [("New Game", self._new_game), ("Solve", self._solve), ("Back", self._back)]:
            btn = QPushButton(text)
            btn.setFixedWidth(130)
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)
        root.addLayout(btn_row)

        # Status
        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._status)

        self._new_game()

    # ------------------------------------------------------------------
    # Game logic
    # ------------------------------------------------------------------

    def _new_game(self) -> None:
        removals = Difficulty[self._difficulty.currentText().upper()].value
        board = SudokuGenerator(SUDOKU_SIZE, removals).generate()
        self._original = [row[:] for row in board]
        self._render_board(board)
        self._status.setText("")

    def _render_board(self, board: Board) -> None:
        # Remove old grid layout
        old_layout = self._grid_frame.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            old_layout.deleteLater()

        self._entries = []
        grid = QGridLayout(self._grid_frame)
        grid.setSpacing(0)
        grid.setContentsMargins(4, 4, 4, 4)

        size = len(board)
        box = int(size ** 0.5)

        for i in range(size):
            row_entries: List[QLineEdit] = []
            for j in range(size):
                entry = QLineEdit()
                entry.setFixedSize(44, 44)
                entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
                entry.setFont(QFont("Helvetica Neue", 16))
                entry.setStyleSheet(self._cell_style(i, j, board[i][j] != 0))

                if board[i][j] != 0:
                    entry.setText(str(board[i][j]))
                    entry.setEnabled(False)
                else:
                    entry.setValidator(QIntValidator(1, 9, entry))

                # extra spacing between 3×3 boxes
                right  = 6 if (j + 1) % box == 0 and j + 1 < size else 1
                bottom = 6 if (i + 1) % box == 0 and i + 1 < size else 1
                grid.addWidget(entry, i * 2, j * 2)

                if j < size - 1:
                    vsep = QFrame()
                    vsep.setFixedWidth(right)
                    vsep.setStyleSheet("background: #555;" if right == 1 else "background: #aaa;")
                    grid.addWidget(vsep, i * 2, j * 2 + 1)

                row_entries.append(entry)

            if i < size - 1:
                height = bottom
                for j in range(size):
                    hsep = QFrame()
                    hsep.setFixedHeight(height)
                    hsep.setStyleSheet("background: #555;" if height == 1 else "background: #aaa;")
                    grid.addWidget(hsep, i * 2 + 1, j * 2)

            self._entries.append(row_entries)

    @staticmethod
    def _cell_style(row: int, col: int, is_given: bool) -> str:
        bg = "#1a1a2e" if is_given else "#2d2d3e"
        fg = "#888888" if is_given else "#ffffff"
        return (
            f"QLineEdit {{ background-color: {bg}; color: {fg}; "
            f"border: none; }}"
        )

    def _solve(self) -> None:
        if self._worker and self._worker.isRunning():
            return
        self._status.setText("Solving…")
        board = copy.deepcopy(self._original)

        self._worker = Worker(lambda: SudokuSolver(board).solve())
        self._worker.finished.connect(self._apply_solution)
        self._worker.start()

    def _apply_solution(self, solution: Optional[Board]) -> None:
        if solution is None:
            QMessageBox.critical(self, "Sudoku", "No solution found.")
            self._status.setText("")
            return
        size = len(solution)
        for i in range(size):
            for j in range(size):
                entry = self._entries[i][j]
                entry.setEnabled(True)
                entry.setText(str(solution[i][j]))
                was_blank = self._original[i][j] == 0
                entry.setStyleSheet(
                    f"QLineEdit {{ background-color: {'#1a3a1a' if was_blank else '#1a1a2e'}; "
                    f"color: {'#4CAF50' if was_blank else '#888888'}; border: none; }}"
                )
                entry.setEnabled(False)
        self._status.setText("Solved!")
