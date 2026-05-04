from __future__ import annotations

from typing import Callable, List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.config import WORD_LADDER_NUM_WORDS, WORD_LADDER_WORD_LENGTH
from src.gui._worker import Worker
from src.puzzles.word_ladder import WordLadderGenerator, WordLadderSolver


class WordLadderView(QWidget):
    def __init__(self, back: Callable[[], None]) -> None:
        super().__init__()
        self._back = back
        self._start = ""
        self._end = ""
        self._words: List[str] = []
        self._worker: Optional[Worker] = None
        self._build_ui()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        root.setSpacing(10)
        root.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Word Ladder")
        title.setFont(QFont("Helvetica Neue", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        # Info panel
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(6)

        self._start_lbl = QLabel("Start: —")
        self._start_lbl.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        panel_layout.addWidget(self._start_lbl)

        self._end_lbl = QLabel("End:   —")
        self._end_lbl.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        panel_layout.addWidget(self._end_lbl)

        self._words_lbl = QLabel("Words: —")
        self._words_lbl.setFont(QFont("Courier New", 11))
        self._words_lbl.setWordWrap(True)
        panel_layout.addWidget(self._words_lbl)

        root.addWidget(panel)

        # Path display
        self._path_lbl = QLabel("")
        self._path_lbl.setFont(QFont("Courier New", 13))
        self._path_lbl.setWordWrap(True)
        self._path_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._path_lbl)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        for text, slot in [("New Puzzle", self._new_puzzle), ("Solve", self._solve), ("Back", self._back)]:
            btn = QPushButton(text)
            btn.setFixedWidth(140)
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)
        root.addLayout(btn_row)

        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._status)

        self._new_puzzle()

    # ------------------------------------------------------------------
    # Game logic
    # ------------------------------------------------------------------

    def _new_puzzle(self) -> None:
        self._start, self._end, self._words = WordLadderGenerator(
            WORD_LADDER_NUM_WORDS, WORD_LADDER_WORD_LENGTH
        ).generate()
        self._start_lbl.setText(f"Start: {self._start}")
        self._end_lbl.setText(f"End:   {self._end}")
        self._words_lbl.setText("Words: " + "  ".join(self._words))
        self._path_lbl.setText("")
        self._status.setText("")

    def _solve(self) -> None:
        if self._worker and self._worker.isRunning():
            return
        self._status.setText("Solving…")
        start, end, words = self._start, self._end, list(self._words)

        self._worker = Worker(lambda: WordLadderSolver(start, end, words).solve())
        self._worker.finished.connect(self._show_result)
        self._worker.start()

    def _show_result(self, path: Optional[List[str]]) -> None:
        if path is None:
            QMessageBox.information(self, "Word Ladder", "No transformation path found.")
            self._status.setText("")
            return
        self._path_lbl.setText(" → ".join(path))
        self._status.setText(f"Shortest path — {len(path) - 1} step(s)")
