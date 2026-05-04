from __future__ import annotations

import copy

import pytest

from src.puzzles.sudoku import (
    SudokuGenerator,
    SudokuSolver,
    _count_solutions,
    _is_valid,
)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class TestSudokuGenerator:
    def test_board_is_9x9(self):
        board = SudokuGenerator(9, 30).generate()
        assert len(board) == 9
        assert all(len(row) == 9 for row in board)

    def test_blanks_do_not_exceed_removals(self):
        removals = 35
        board = SudokuGenerator(9, removals).generate()
        blanks = sum(cell == 0 for row in board for cell in row)
        assert blanks <= removals

    def test_pre_filled_cells_are_valid(self):
        gen = SudokuGenerator(9, 30)
        board = gen.generate()
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    continue
                val = board[r][c]
                board[r][c] = 0
                assert _is_valid(board, r, c, val, gen.box_size), (
                    f"Pre-filled cell ({r},{c})={val} violates constraints"
                )
                board[r][c] = val

    def test_generated_puzzle_has_unique_solution(self):
        board = SudokuGenerator(9, 35).generate()
        assert _count_solutions(copy.deepcopy(board), 3) == 1


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

class TestSudokuSolver:
    def _make_puzzle(self, removals: int = 40) -> list:
        return SudokuGenerator(9, removals).generate()

    def test_solver_returns_complete_board(self):
        puzzle = self._make_puzzle()
        solution = SudokuSolver(puzzle).solve()
        assert solution is not None
        assert all(1 <= cell <= 9 for row in solution for cell in row)

    def test_solver_does_not_mutate_input(self):
        puzzle = self._make_puzzle(30)
        original = copy.deepcopy(puzzle)
        SudokuSolver(puzzle).solve()
        assert puzzle == original

    def test_solver_returns_none_for_unsolvable_board(self):
        # Row 0 has 1-8 pre-filled → only 9 can go in (0,8).
        # Column 8 already has 9 at row 1 → (0,8) cannot be filled → no solution.
        board = [[0] * 9 for _ in range(9)]
        for j in range(8):
            board[0][j] = j + 1  # row 0 = [1,2,3,4,5,6,7,8,_]
        board[1][8] = 9           # col 8 now has 9; (0,8) must be 9 but can't be
        assert SudokuSolver(board).solve() is None

    def test_solved_board_passes_constraints(self):
        puzzle = self._make_puzzle()
        solution = SudokuSolver(puzzle).solve()
        assert solution is not None
        box = 3
        for r in range(9):
            assert sorted(solution[r]) == list(range(1, 10)), f"Row {r} invalid"
        for c in range(9):
            col_vals = [solution[r][c] for r in range(9)]
            assert sorted(col_vals) == list(range(1, 10)), f"Col {c} invalid"
        for br in range(3):
            for bc in range(3):
                box_vals = [
                    solution[br * box + dr][bc * box + dc]
                    for dr in range(box)
                    for dc in range(box)
                ]
                assert sorted(box_vals) == list(range(1, 10)), f"Box ({br},{bc}) invalid"
