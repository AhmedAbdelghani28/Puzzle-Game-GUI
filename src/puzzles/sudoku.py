from __future__ import annotations

import copy
import random
from typing import List, Optional, Tuple

from src.puzzles.base import PuzzleGenerator, PuzzleSolver

Board = List[List[int]]


# ---------------------------------------------------------------------------
# Shared constraint logic (eliminates duplication between generator/solver)
# ---------------------------------------------------------------------------

def _is_valid(board: Board, row: int, col: int, num: int, box_size: int) -> bool:
    size = len(board)
    if num in board[row]:
        return False
    if any(board[r][col] == num for r in range(size)):
        return False
    sr, sc = row - row % box_size, col - col % box_size
    return not any(
        board[sr + dr][sc + dc] == num
        for dr in range(box_size)
        for dc in range(box_size)
    )


def _count_solutions(board: Board, box_size: int, limit: int = 2) -> int:
    """Count solutions up to *limit*, stopping early once reached."""
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] != 0:
                continue
            count = 0
            for num in range(1, size + 1):
                if _is_valid(board, r, c, num, box_size):
                    board[r][c] = num
                    count += _count_solutions(board, box_size, limit)
                    board[r][c] = 0  # always restore before checking limit
                    if count >= limit:
                        return count
            return count
    return 1  # no empty cells — complete solution


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class SudokuGenerator(PuzzleGenerator[Board]):
    """Generates a valid Sudoku puzzle with a guaranteed unique solution."""

    def __init__(self, size: int = 9, removals: int = 40) -> None:
        self.size = size
        self.box_size = int(size ** 0.5)
        self.removals = removals

    def generate(self) -> Board:
        board: Board = [[0] * self.size for _ in range(self.size)]
        self._fill(board)
        self._remove_numbers(board)
        return board

    def _fill(self, board: Board) -> bool:
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] != 0:
                    continue
                nums = random.sample(range(1, self.size + 1), self.size)
                for num in nums:
                    if _is_valid(board, row, col, num, self.box_size):
                        board[row][col] = num
                        if self._fill(board):
                            return True
                        board[row][col] = 0
                return False
        return True

    def _remove_numbers(self, board: Board) -> None:
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        removed = 0
        for row, col in cells:
            if removed >= self.removals:
                break
            backup = board[row][col]
            board[row][col] = 0
            # deepcopy so _count_solutions can freely backtrack without
            # corrupting the board we are still iterating over
            if _count_solutions(copy.deepcopy(board), self.box_size) == 1:
                removed += 1
            else:
                board[row][col] = backup


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

class SudokuSolver(PuzzleSolver[Board, Board]):
    """Solves a Sudoku board via backtracking DFS."""

    def __init__(self, board: Board) -> None:
        self.board = [row[:] for row in board]  # defensive copy
        self.size = len(board)
        self.box_size = int(self.size ** 0.5)

    def solve(self) -> Optional[Board]:
        if self._backtrack():
            return self.board
        return None

    def _backtrack(self) -> bool:
        cell = self._next_empty()
        if cell is None:
            return True
        row, col = cell
        for num in range(1, self.size + 1):
            if _is_valid(self.board, row, col, num, self.box_size):
                self.board[row][col] = num
                if self._backtrack():
                    return True
                self.board[row][col] = 0
        return False

    def _next_empty(self) -> Optional[Tuple[int, int]]:
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c
        return None
