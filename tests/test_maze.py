from __future__ import annotations

import pytest

from src.puzzles.maze import END, START, WALL, MazeGenerator, MazeSolver


class TestMazeGenerator:
    def test_dimensions(self):
        maze = MazeGenerator(11, 21).generate()
        assert len(maze) == 11
        assert all(len(row) == 21 for row in maze)

    def test_contains_start_and_end(self):
        maze = MazeGenerator(11, 21).generate()
        flat = [cell for row in maze for cell in row]
        assert START in flat
        assert END in flat

    def test_even_dimensions_raise(self):
        with pytest.raises(ValueError):
            MazeGenerator(10, 21)
        with pytest.raises(ValueError):
            MazeGenerator(11, 20)

    def test_border_cells_are_walls(self):
        rows, cols = 11, 21
        maze = MazeGenerator(rows, cols).generate()
        for c in range(cols):
            assert maze[0][c] in (WALL, START, END)
            assert maze[rows - 1][c] in (WALL, START, END)
        for r in range(rows):
            assert maze[r][0] == WALL
            assert maze[r][cols - 1] == WALL


class TestMazeSolver:
    def test_finds_path(self):
        maze = MazeGenerator(11, 21).generate()
        path = MazeSolver(maze).solve()
        assert path is not None
        assert len(path) > 0

    def test_path_starts_at_start(self):
        maze = MazeGenerator(11, 21).generate()
        path = MazeSolver(maze).solve()
        assert path is not None
        sr, sc = path[0]
        assert maze[sr][sc] == START

    def test_path_ends_at_end(self):
        maze = MazeGenerator(11, 21).generate()
        path = MazeSolver(maze).solve()
        assert path is not None
        er, ec = path[-1]
        assert maze[er][ec] == END

    def test_path_is_contiguous(self):
        maze = MazeGenerator(11, 21).generate()
        path = MazeSolver(maze).solve()
        assert path is not None
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            assert abs(r1 - r2) + abs(c1 - c2) == 1, (
                f"Non-adjacent steps in path: ({r1},{c1}) → ({r2},{c2})"
            )

    def test_path_does_not_cross_walls(self):
        maze = MazeGenerator(11, 21).generate()
        path = MazeSolver(maze).solve()
        assert path is not None
        for r, c in path:
            assert maze[r][c] != WALL, f"Path crosses wall at ({r},{c})"
