# Puzzle Game GUI

A Python desktop application with three classic logic puzzles in a modern dark-mode interface built on **PyQt6**.

## Puzzles

| Puzzle | Generation | Solving | Guarantee |
|--------|------------|---------|-----------|
| **Sudoku** | Backtracking fill + per-cell uniqueness check | Backtracking DFS | Unique solution |
| **Maze** | DFS carving (perfect maze) | BFS | Shortest path |
| **Word Ladder** | Single-letter mutation chain | BFS | Shortest path |

## Quick Start — Docker (recommended)

No Python or Qt installation needed. Runs in any browser.

```bash
docker compose up --build
```

Then open **http://localhost:6080/vnc.html** in your browser.

> The container streams the GUI over noVNC (browser-based VNC).  
> Closing the app window stops the container automatically.

### Docker fixes (applied)

Earlier builds had three silent failures on first run:

| Issue | Root cause | Fix |
|-------|-----------|-----|
| Xvfb readiness check did nothing | `xdpyinfo` (from `x11-utils`) was not installed | Added `x11-utils` to `apt-get install` |
| `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"` | `libxcb-util1` and `libxcb-xfixes0` missing | Added both packages to `apt-get install` |
| x11vnc connected before Xvfb was ready | Wait loop exited too early with no working probe | Extended loop to 30 iterations + added `sleep 0.5` guard |

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
Dockerfile                       — two-stage build; Python + Qt system libs
docker-compose.yml               — port 6080 → noVNC web UI
docker/entrypoint.sh             — starts Xvfb → x11vnc → noVNC → app
src/
├── config.py                    — app-wide constants, Difficulty enum
├── puzzles/
│   ├── base.py                  — PuzzleGenerator / PuzzleSolver abstract contracts
│   ├── sudoku.py                — generator + backtracking solver
│   ├── maze.py                  — DFS generator + BFS solver
│   └── word_ladder.py           — chain generator + BFS solver
└── gui/
    ├── _worker.py               — QThread wrapper for non-blocking solvers
    ├── app.py                   — QMainWindow, navigation
    ├── sudoku_view.py           — 9×9 grid, difficulty selector, threaded solve
    ├── maze_view.py             — custom QPainter canvas, threaded BFS solve
    └── word_ladder_view.py      — word info panel, threaded BFS solve
tests/
├── test_sudoku.py
├── test_maze.py
└── test_word_ladder.py
```

## Design Decisions

- **Abstract base classes** (`PuzzleGenerator`, `PuzzleSolver`) define a uniform contract — adding a new game means implementing two methods.
- **Separation of concerns** — puzzle logic in `src/puzzles/` knows nothing about Qt; the GUI only calls `generate()` and `solve()`.
- **QThread + pyqtSignal** — solve operations run on a background thread; results are delivered to the UI thread via signals, keeping the window fully responsive.
- **BFS for maze and word ladder** — guarantees the *shortest* path, not merely *a* path.
- **Sudoku uniqueness** — each cell removal is validated by a solution counter capped at 2, so every generated puzzle has exactly one solution.
- **Difficulty levels** map directly to removed-cell counts (Easy: 30, Medium: 40, Hard: 50).
- **Docker / noVNC** — Xvfb provides a virtual display inside the container; x11vnc streams it over VNC; noVNC proxies VNC to WebSockets so any browser can view the GUI with zero client installation.
