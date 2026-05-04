from __future__ import annotations

import random
from collections import deque
from typing import List, Optional, Tuple

from src.puzzles.base import PuzzleGenerator, PuzzleSolver

Grid = List[List[str]]
Cell = Tuple[int, int]
Path = List[Cell]

WALL = "#"
OPEN = " "
START = "S"
END = "E"

_DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


# ---------------------------------------------------------------------------
# Generator — DFS carving produces a perfect maze (exactly one path between
# any two cells), so the solver is always guaranteed to find a path.
# ---------------------------------------------------------------------------

class MazeGenerator(PuzzleGenerator[Grid]):
    def __init__(self, rows: int = 11, cols: int = 21) -> None:
        if rows % 2 == 0 or cols % 2 == 0:
            raise ValueError("rows and cols must be odd for DFS maze carving")
        self.rows = rows
        self.cols = cols

    def generate(self) -> Grid:
        maze: Grid = [[WALL] * self.cols for _ in range(self.rows)]

        # Border openings — row 0 and row rows-1 stay walls except these gaps
        start: Cell = (0, 1)
        end: Cell = (self.rows - 1, self.cols - 2)
        maze[start[0]][start[1]] = START
        maze[end[0]][end[1]] = END

        # DFS carving must start from an interior odd-indexed cell so that it
        # visits all (odd_row, odd_col) positions and never touches the border.
        # (1,1) is the first such cell and is adjacent to START, so connectivity
        # is guaranteed: START → (1,1) → … → (rows-2, cols-2) → END.
        interior_start: Cell = (1, 1)
        maze[interior_start[0]][interior_start[1]] = OPEN
        self._carve(maze, interior_start[0], interior_start[1])
        return maze

    def _carve(self, maze: Grid, row: int, col: int) -> None:
        dirs = list(_DIRS)
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = row + 2 * dr, col + 2 * dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and maze[nr][nc] == WALL:
                maze[row + dr][col + dc] = OPEN
                maze[nr][nc] = OPEN
                self._carve(maze, nr, nc)


# ---------------------------------------------------------------------------
# Solver — BFS guarantees the shortest path (unlike DFS which finds *a* path)
# ---------------------------------------------------------------------------

class MazeSolver(PuzzleSolver[Grid, Path]):
    """BFS solver — always returns the shortest path from S to E."""

    def __init__(self, maze: Grid) -> None:
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def solve(self) -> Optional[Path]:
        start = self._find(START)
        if start is None:
            return None

        queue: deque[Tuple[Cell, Path]] = deque([(start, [start])])
        visited: set[Cell] = {start}

        while queue:
            (row, col), path = queue.popleft()
            if self.maze[row][col] == END:
                return path
            for dr, dc in _DIRS:
                nr, nc = row + dr, col + dc
                if (
                    0 <= nr < self.rows
                    and 0 <= nc < self.cols
                    and (nr, nc) not in visited
                    and self.maze[nr][nc] != WALL
                ):
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
        return None

    def _find(self, marker: str) -> Optional[Cell]:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == marker:
                    return r, c
        return None
