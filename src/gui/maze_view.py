from __future__ import annotations

from typing import Callable, List, Optional, Set, Tuple

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPaintEvent

from src.config import MAZE_COLS, MAZE_ROWS
from src.gui._worker import Worker
from src.puzzles.maze import END, OPEN, START, WALL, MazeGenerator, MazeSolver

Grid = List[List[str]]
Cell = Tuple[int, int]

_COLORS: dict[str, QColor] = {
    WALL:  QColor("#1a1a2e"),
    START: QColor("#4CAF50"),
    END:   QColor("#F44336"),
    OPEN:  QColor("#dde1e7"),
}
_PATH_COLOR = QColor("#FFC107")
_CELL_PX = 22  # pixel size of each maze cell


class _MazeCanvas(QWidget):
    """Custom widget that renders the maze grid with QPainter."""

    def __init__(self, maze: Grid) -> None:
        super().__init__()
        self._maze = maze
        self._path: Set[Cell] = set()
        rows, cols = len(maze), len(maze[0])
        self.setFixedSize(cols * _CELL_PX, rows * _CELL_PX)

    def show_path(self, path: List[Cell]) -> None:
        self._path = set(path)
        self.update()  # schedule repaint

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)
        cs = _CELL_PX
        for r, row in enumerate(self._maze):
            for c, cell in enumerate(row):
                if (r, c) in self._path and cell not in (START, END):
                    color = _PATH_COLOR
                else:
                    color = _COLORS.get(cell, _COLORS[OPEN])
                painter.fillRect(c * cs, r * cs, cs, cs, color)


class MazeView(QWidget):
    def __init__(self, back: Callable[[], None]) -> None:
        super().__init__()
        self._back = back
        self._maze: Grid = []
        self._canvas: Optional[_MazeCanvas] = None
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

        title = QLabel("Maze")
        title.setFont(QFont("Helvetica Neue", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        self._canvas_container = QVBoxLayout()
        self._canvas_container.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        root.addLayout(self._canvas_container)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        for text, slot in [("New Maze", self._new_maze), ("Solve", self._solve), ("Back", self._back)]:
            btn = QPushButton(text)
            btn.setFixedWidth(130)
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)
        root.addLayout(btn_row)

        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._status)

        self._new_maze()

    # ------------------------------------------------------------------
    # Game logic
    # ------------------------------------------------------------------

    def _new_maze(self) -> None:
        self._maze = MazeGenerator(MAZE_ROWS, MAZE_COLS).generate()
        if self._canvas is not None:
            self._canvas_container.removeWidget(self._canvas)
            self._canvas.deleteLater()
        self._canvas = _MazeCanvas(self._maze)
        self._canvas_container.addWidget(self._canvas)
        self._status.setText("")

    def _solve(self) -> None:
        if self._worker and self._worker.isRunning():
            return
        self._status.setText("Solving…")

        maze = self._maze
        self._worker = Worker(lambda: MazeSolver(maze).solve())
        self._worker.finished.connect(self._draw_path)
        self._worker.start()

    def _draw_path(self, path: Optional[List[Cell]]) -> None:
        if path is None:
            QMessageBox.information(self, "Maze", "No path found.")
            self._status.setText("")
            return
        if self._canvas is not None:
            self._canvas.show_path(path)
        self._status.setText(f"Shortest path — {len(path)} steps")
