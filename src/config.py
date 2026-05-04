from __future__ import annotations

from enum import Enum


class Difficulty(Enum):
    EASY = 30
    MEDIUM = 40
    HARD = 50


SUDOKU_SIZE = 9

# Must be odd — DFS maze carving works on odd-dimensioned grids
MAZE_ROWS = 11
MAZE_COLS = 21

WORD_LADDER_NUM_WORDS = 20
WORD_LADDER_WORD_LENGTH = 5

APP_TITLE = "Puzzle Game"
