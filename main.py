import customtkinter as ctk
from tkinter import messagebox
from collections import deque
import random
import string

class SudokuGenerator:
    """
    A class to generate and manipulate Sudoku boards.
    """
    def __init__(self, size):
        """
        Initialize the SudokuGenerator with a specific board size.

        Args:
            size (int): The size of the Sudoku board (e.g., 9 for a 9x9 board).
        """
        self.size = size
        self.box_size = int(self.size ** 0.5)

    def generate_board(self):
        """
        Generate a Sudoku board with a valid solution and some numbers removed.

        Returns:
            list: A 2D list representing the generated Sudoku board.
        """
        board = [[0] * self.size for _ in range(self.size)]
        self.solve_board(board)
        self.remove_numbers(board)
        return board

    def is_valid_move(self, board, row, col, num):
        """
        Check if placing a number on the board is a valid move.

        Args:
            board (list): The current state of the Sudoku board.
            row (int): The row index to place the number.
            col (int): The column index to place the number.
            num (int): The number to be placed.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        for i in range(self.size):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row = row - row % self.box_size
        start_col = col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve_board(self, board):
        """
        Solve the Sudoku board using backtracking.

        Args:
            board (list): The current state of the Sudoku board.

        Returns:
            bool: True if the board is solvable, False otherwise.
        """
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid_move(board, row, col, num):
                            board[row][col] = num
                            if self.solve_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def remove_numbers(self, board):
        """
        Remove numbers from the Sudoku board to create a puzzle.

        Args:
            board (list): The current state of the Sudoku board.
        """
        num_to_remove = 40 if self.size == 9 else 4
        for _ in range(num_to_remove):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            while board[row][col] == 0:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
            temp = board[row][col]
            board[row][col] = 0
            temp_board = [row[:] for row in board]
            if not self.has_unique_solution(temp_board):
                board[row][col] = temp

    def has_unique_solution(self, board):
        """
        Check if the Sudoku board has a unique solution.

        Args:
            board (list): The current state of the Sudoku board.

        Returns:
            bool: True if the board has a unique solution, False otherwise.
        """
        solver = SudokuSolverDFS(board)
        solver.solve()
        return solver.num_solutions == 1

class SudokuSolverDFS:
    """
    A class to solve a Sudoku board using depth-first search (DFS).
    """
    def __init__(self, board):
        """
        Initialize the SudokuSolverDFS with a specific board.

        Args:
            board (list): The initial state of the Sudoku board.
        """
        self.board = board
        self.size = len(board)
        self.box_size = int(self.size ** 0.5)
        self.num_solutions = 0

    def is_valid_move(self, row, col, num):
        """
        Check if placing a number on the board is a valid move.

        Args:
            row (int): The row index to place the number.
            col (int): The column index to place the number.
            num (int): The number to be placed.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        for i in range(self.size):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row = row - row % self.box_size
        start_col = col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def find_empty_cell(self):
        """
        Find an empty cell in the Sudoku board.

        Returns:
            tuple: The row and column index of an empty cell, or (None, None) if the board is full.
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None, None

    def solve(self):
        """
        Solve the Sudoku board using depth-first search (DFS).

        Returns:
            bool: True if the board is solvable, False otherwise.
        """
        row, col = self.find_empty_cell()
        if row is None and col is None:
            self.num_solutions += 1
            return True

        for num in range(1, self.size + 1):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

    def display_board(self):
        """
        Display the Sudoku board in the console.
        """
        for row in self.board:
            print(" ".join(map(str, row)))

class MazeGenerator:
    """
    A class to generate and manipulate mazes.
    """
    def __init__(self, rows, cols):
        """
        Initialize the MazeGenerator with specific dimensions.

        Args:
            rows (int): The number of rows in the maze.
            cols (int): The number of columns in the maze.
        """
        self.rows = rows
        self.cols = cols
        self.maze = [['#'] * cols for _ in range(rows)]
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def is_valid_move(self, row, col):
        """
        Check if moving to a cell in the maze is valid.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols and self.maze[row][col] == '#'

    def generate_maze(self, start_row, start_col, end_row, end_col):
        """
        Generate a maze using depth-first search (DFS).

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The ending row index.
            end_col (int): The ending column index.
        """
        self.maze[start_row][start_col] = 'S'
        self.maze[end_row][end_col] = 'E'
        self.dfs(start_row, start_col)

    def dfs(self, row, col):
        """
        Depth-first search (DFS) to carve out the maze paths.

        Args:
            row (int): The current row index.
            col (int): The current column index.
        """
        random.shuffle(self.directions)
        for dr, dc in self.directions:
            new_row, new_col = row + 2 * dr, col + 2 * dc
            if self.is_valid_move(new_row, new_col):
                self.maze[row + dr][col + dc] = ' '
                self.maze[new_row][new_col] = ' '
                self.dfs(new_row, new_col)

    def display_maze(self):
        """
        Display the maze in the console.
        """
        for row in self.maze:
            print(''.join(row))

class MazeSolverDFS:
    """
    A class to solve a maze using depth-first search (DFS).
    """
    def __init__(self, maze):
        """
        Initialize the MazeSolverDFS with a specific maze.

        Args:
            maze (list): The maze to be solved.
        """
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = [[False] * self.cols for _ in range(self.rows)]
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.path = []

    def is_valid_move(self, row, col):
        """
        Check if moving to a cell in the maze is valid.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols and not self.visited[row][col] and self.maze[row][col] != '#'

    def dfs(self, row, col):
        """
        Depth-first search (DFS) to solve the maze.

        Args:
            row (int): The current row index.
            col (int): The current column index.

        Returns:
            bool: True if the end of the maze is reached, False otherwise.
        """
        if not self.is_valid_move(row, col):
            return False

        self.visited[row][col] = True
        self.path.append((row, col))

        if self.maze[row][col] == 'E':
            return True

        for dr, dc in self.directions:
            if self.dfs(row + dr, col + dc):
                return True

        self.path.pop()
        return False

    def solve(self, start_row, start_col):
        """
        Solve the maze starting from a specific position.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.

        Returns:
            list: The path from start to end, or None if no path is found.
        """
        if not self.is_valid_move(start_row, start_col):
            print("Invalid starting position")
            return None

        if self.dfs(start_row, start_col):
            return self.path
        else:
            print("No path found")
            return None

class WordLadderGame:
    """
    A class to create and solve Word Ladder puzzles.
    """
    def __init__(self, word_list):
        """
        Initialize the WordLadderGame with a specific word list.

        Args:
            word_list (list): The list of valid words for the game.
        """
        self.word_list = set(word_list)

    def generate_word_list(self, num_words, word_length):
        """
        Generate a list of words for the Word Ladder game.

        Args:
            num_words (int): The number of words to generate.
            word_length (int): The length of each word.

        Returns:
            list: A list of generated words.
        """
        word_list = []
        current_word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        word_list.append(current_word)
        for _ in range(num_words - 1):
            next_word = self.generate_next_word(current_word)
            word_list.append(next_word)
            current_word = next_word
        return word_list

    def generate_next_word(self, word):
        """
        Generate a new word by changing one character of the given word.

        Args:
            word (str): The current word.

        Returns:
            str: The generated new word.
        """
        word = list(word)
        index = random.randint(0, len(word) - 1)
        char = random.choice(string.ascii_lowercase)
        word[index] = char
        return ''.join(word)

    def get_neighbors(self, word):
        """
        Get all valid neighboring words that differ by one character.

        Args:
            word (str): The current word.

        Returns:
            list: A list of neighboring words.
        """
        neighbors = []
        for i in range(len(word)):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + char + word[i + 1:]
                if new_word != word and new_word in self.word_list:
                    neighbors.append(new_word)
        return neighbors

    def find_shortest_path(self, start_word, end_word):
        """
        Find the shortest transformation path from start_word to end_word.

        Args:
            start_word (str): The starting word.
            end_word (str): The ending word.

        Returns:
            list: The shortest path from start_word to end_word, or None if no path exists.
        """
        if start_word not in self.word_list or end_word not in self.word_list:
            return None

        queue = deque([(start_word, [start_word])])
        visited = set([start_word])

        while queue:
            current_word, path = queue.popleft()
            if current_word == end_word:
                return path
            for neighbor in self.get_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

class PuzzleGUI:
    """
    A class to create a GUI for different puzzle games using customtkinter.
    """
    def __init__(self, root):
        """
        Initialize the PuzzleGUI with a root window.

        Args:
            root (CTk): The root window for the GUI.
        """
        self.root = root
        self.root.title("Puzzle Game")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_main_menu()

    def create_main_menu(self):
        """
        Create the main menu of the puzzle game GUI.
        """
        self.clear_screen()

        title_label = ctk.CTkLabel(self.root, text="Choose a Puzzle", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=15)

        sudoku_button = ctk.CTkButton(self.root, text="Sudoku", command=self.play_sudoku, width=200)
        sudoku_button.pack(pady=15)

        maze_button = ctk.CTkButton(self.root, text="Maze", command=self.play_maze, width=200)
        maze_button.pack(pady=15)

        word_ladder_button = ctk.CTkButton(self.root, text="Word Ladder", command=self.play_word_ladder, width=200)
        word_ladder_button.pack(pady=15)

    def clear_screen(self):
        """
        Clear all widgets from the current screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def play_sudoku(self):
        """
        Display the Sudoku puzzle game.
        """
        self.clear_screen()

        size = 9
        sudoku_generator = SudokuGenerator(size)
        sudoku_board = sudoku_generator.generate_board()

        solver = SudokuSolverDFS(sudoku_board)

        board_frame = ctk.CTkFrame(self.root)
        board_frame.pack(pady=10)

        for i in range(size):
            for j in range(size):
                entry = ctk.CTkEntry(board_frame, width=30, font=ctk.CTkFont(size=16), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                if sudoku_board[i][j] != 0:
                    entry.insert(0, sudoku_board[i][j])
                    entry.configure(state='disabled')

        solve_button = ctk.CTkButton(self.root, text="Solve", command=lambda: self.solve_sudoku(solver, board_frame))
        solve_button.pack(pady=10)

        back_button = ctk.CTkButton(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

    def solve_sudoku(self, solver, board_frame):
        """
        Solve the Sudoku puzzle and display the solution.

        Args:
            solver (SudokuSolverDFS): The Sudoku solver object.
            board_frame (CTkFrame): The frame containing the Sudoku board.
        """
        solver.solve()
        steps = solver.size * solver.size  # Since we solved the board completely
        for i in range(solver.size):
            for j in range(solver.size):
                entry = board_frame.grid_slaves(row=i, column=j)[0]
                entry.configure(state='normal')
                entry.delete(0, ctk.END)
                entry.insert(0, solver.board[i][j])
                entry.configure(state='disabled')
        messagebox.showinfo("Sudoku Solver", f"Solved in {steps} steps")

    def play_maze(self):
        """
        Display the maze puzzle game.
        """
        self.clear_screen()

        rows, cols = 10, 20
        start_row, start_col = 0, 1
        end_row, end_col = rows - 1, cols - 2

        maze_generator = MazeGenerator(rows, cols)
        maze_generator.generate_maze(start_row, start_col, end_row, end_col)

        maze_frame = ctk.CTkFrame(self.root)
        maze_frame.pack(pady=10)

        self.maze_labels = []
        for i in range(rows):
            row_labels = []
            for j in range(cols):
                label = ctk.CTkLabel(maze_frame, text=maze_generator.maze[i][j], font=ctk.CTkFont(size=16), width=20, anchor='center')
                label.grid(row=i, column=j, padx=1, pady=1)
                row_labels.append(label)
            self.maze_labels.append(row_labels)

        solve_button = ctk.CTkButton(self.root, text="Solve", command=lambda: self.solve_maze(maze_generator.maze, start_row, start_col))
        solve_button.pack(pady=10)

        back_button = ctk.CTkButton(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

    def solve_maze(self, maze, start_row, start_col):
        """
        Solve the maze and display the solution path.

        Args:
            maze (list): The maze to be solved.
            start_row (int): The starting row index.
            start_col (int): The starting column index.
        """
        maze_solver = MazeSolverDFS(maze)
        path = maze_solver.solve(start_row, start_col)
        if path:
            for (row, col) in path:
                self.maze_labels[row][col].configure(bg_color='yellow')
            messagebox.showinfo("Maze Solver", f"Path found in {len(path)} steps:\n{path}")
        else:
            messagebox.showinfo("Maze Solver", "No path found")

    def play_word_ladder(self):
        """
        Display the Word Ladder puzzle game.
        """
        self.clear_screen()

        num_words = 20
        word_length = 5
        word_list = WordLadderGame([]).generate_word_list(num_words, word_length)
        start_word = word_list[0]
        end_word = word_list[-1]

        word_ladder_game = WordLadderGame(word_list)
        shortest_path = word_ladder_game.find_shortest_path(start_word, end_word)

        if shortest_path:
            word_list_label = ctk.CTkLabel(self.root, text=f"Word List: {word_list}", wraplength=400)
            word_list_label.pack(pady=5)

            start_label = ctk.CTkLabel(self.root, text=f"Start Word: {start_word}")
            start_label.pack(pady=5)

            end_label = ctk.CTkLabel(self.root, text=f"End Word: {end_word}")
            end_label.pack(pady=5)

            path_label = ctk.CTkLabel(self.root, text=f"Shortest Path: {' -> '.join(shortest_path)}\nSteps: {len(shortest_path) - 1}", wraplength=400)
            path_label.pack(pady=10)
        else:
            messagebox.showinfo("Word Ladder", "No transformation path exists between the given words.")

        back_button = ctk.CTkButton(self.root, text="Back", command=self.create_main_menu)
        back_button.pack(pady=5)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PuzzleGUI(root)
    root.mainloop()

