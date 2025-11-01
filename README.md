# 🧩 Puzzle Game GUI

A Python desktop app that brings together **three classic logic puzzles** — Sudoku, Maze Solver, and Word Ladder — into a clean and modern graphical interface built with **CustomTkinter**.

---

## 🚀 Features

✅ **Sudoku Generator & Solver**  
- Generates valid Sudoku boards  
- Solves them using **backtracking**  
- Clean, interactive grid interface  

✅ **Maze Generator & Solver**  
- Generates random mazes using **DFS**  
- Solves them step by step  
- Visually displays the solution path  

✅ **Word Ladder Puzzle**  
- Generates random words  
- Finds the **shortest transformation path** between words using **BFS**  
- Displays all steps in a clear format  

---

## 🧠 Algorithms Used

| Puzzle | Algorithm | Description |
|--------|------------|-------------|
| Sudoku | Backtracking | Systematically fills grid while checking validity |
| Maze | Depth-First Search (DFS) | Carves maze paths and finds route from start to end |
| Word Ladder | Breadth-First Search (BFS) | Finds shortest transformation between words |

---

## 🖥️ Tech Stack
- **Python 3.x**
- **CustomTkinter**
- **Tkinter**
- **collections**, **random**, **string**

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/AhmedAbdelghani28/puzzle-game-gui.git

# Go to the project directory
cd puzzle-game-gui

# Install dependencies
pip install customtkinter
