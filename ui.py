import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import time
import os
from PIL import Image, ImageTk

# Import maze solving algorithms
from algorithms.dfs import MazeSolverDFS
from algorithms.bfs import MazeSolverBFS
from algorithms.ucs import MazeSolverUCS
from algorithms.astar import MazeSolverAStar

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [['#' for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.start = (1, 1)
        self.goal = (height - 2, width - 2)
        random.seed(int(time.time()) + random.randint(0, 1000))
        self.maze[self.start[0]][self.start[1]] = 'A'
        self.visited[self.start[0]][self.start[1]] = True

    def generate(self):
        self.dfs(self.start[0], self.start[1])
        self.maze[self.goal[0]][self.goal[1]] = 'B'

    def dfs(self, x, y):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.height and 0 < ny < self.width and not self.visited[nx][ny]:
                self.maze[x + dx // 2][y + dy // 2] = ' '
                self.visited[nx][ny] = True
                self.maze[nx][ny] = ' '
                self.dfs(nx, ny)

    def save_maze(self, filename="generated_maze/m.txt"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            for row in self.maze:
                f.write(''.join(row) + '\n')
        return filename

    def display_maze(self):
        return self.maze


class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver Visualizer")
        self.root.geometry("1200x800")

        # Selected algorithm variables
        self.selected_left_algorithm = tk.StringVar(value="")
        self.selected_right_algorithm = tk.StringVar(value="")

        # Button tracking
        self.left_algorithm_buttons = {}
        self.right_algorithm_buttons = {}

        # Algorithm mapping
        self.algorithm_map = {
            "DFS": MazeSolverDFS,
            "BFS": MazeSolverBFS,
            "Dijkstra": MazeSolverUCS,
            "A*": MazeSolverAStar
        }

        self.setup_ui()

    def setup_ui(self):
        # Create left section (15% width)
        left_frame = tk.Frame(self.root, width=150, bg="#2c3e50")
        left_frame.pack(side="left", fill="y")

        # Create center section (70% width)
        center_frame = tk.Frame(self.root, bg="white")
        center_frame.pack(side="left", fill="both", expand=True)

        # Create right section (15% width)
        right_frame = tk.Frame(self.root, width=150, bg="#2c3e50")
        right_frame.pack(side="right", fill="y")

        # Canvas for drawing the maze
        self.canvas = tk.Canvas(center_frame, bg="white")
        self.canvas.pack(pady=20, fill="both", expand=True)

        # Solution image labels
        self.left_solution_label = tk.Label(center_frame, bg="white")
        self.left_solution_label.pack(side="left", padx=10)

        self.right_solution_label = tk.Label(center_frame, bg="white")
        self.right_solution_label.pack(side="right", padx=10)

        # Buttons
        self.setup_algorithm_buttons(left_frame, right_frame)
        self.setup_control_buttons(center_frame)

    def setup_algorithm_buttons(self, left_frame, right_frame):
        algorithms = ["BFS", "DFS", "Dijkstra", "A*"]

        # Left frame buttons
        for algo in algorithms:
            btn = self.create_curved_button(
                left_frame,
                algo,
                "#2980b9",
                lambda a=algo: self.on_left_algorithm_select(a),
                'left'
            )
            btn.pack(pady=10)
            self.left_algorithm_buttons[algo] = btn

        # Right frame buttons
        for algo in algorithms:
            btn = self.create_curved_button(
                right_frame,
                algo,
                "#2980b9",
                lambda a=algo: self.on_right_algorithm_select(a),
                'right'
            )
            btn.pack(pady=10)
            self.right_algorithm_buttons[algo] = btn

    def setup_control_buttons(self, center_frame):
        btn_frame = tk.Frame(center_frame, bg="white")
        btn_frame.pack(pady=10)

        generate_btn = self.create_curved_button(
            btn_frame,
            "Generate Maze",
            "#e74c3c",
            self.generate_maze,
            'center'
        )
        generate_btn.pack(side="left", padx=10)

        solve_btn = self.create_curved_button(
            btn_frame,
            "Solve Maze",
            "#3498db",
            self.solve_maze,
            'center'
        )
        solve_btn.pack(side="left", padx=10)

    def create_curved_button(self, parent, text, color, command=None, section='center'):
        # Create a custom style for the button
        style = ttk.Style()

        # Normal state
        style.configure(
            f"{text}_{section}.TButton",
            font=("Helvetica", 10, "bold"),
            background=color,
            foreground="black",  # Change font color to black
            borderwidth=1,
            relief="raised",
            padding=6
        )

        # Active (pressed) state
        style.map(
            f"{text}_{section}.TButton",
            background=[('pressed', '#27ae60'), ('active', '#2ecc71')],
            # Change active text color to black
            foreground=[('pressed', 'black'), ('active', 'black')]
        )

        btn = ttk.Button(
            parent,
            text=text,
            style=f"{text}_{section}.TButton",
            command=command
        )

        return btn

    def on_left_algorithm_select(self, algorithm):
        # Reset all left buttons
        for algo, btn in self.left_algorithm_buttons.items():
            btn.state(['!pressed'])

        # Set selected algorithm and mark button as pressed
        self.selected_left_algorithm.set(algorithm)
        self.left_algorithm_buttons[algorithm].state(['pressed'])
        print(f"Left algorithm selected: {algorithm}")

    def on_right_algorithm_select(self, algorithm):
        # Reset all right buttons
        for algo, btn in self.right_algorithm_buttons.items():
            btn.state(['!pressed'])

        # Set selected algorithm and mark button as pressed
        self.selected_right_algorithm.set(algorithm)
        self.right_algorithm_buttons[algorithm].state(['pressed'])
        print(f"Right algorithm selected: {algorithm}")

    def generate_maze(self):
        # Create maze generator and generate maze
        generator = MazeGenerator(35, 35)
        generator.generate()

        # Save maze to file
        maze_file = generator.save_maze("generated_maze/m.txt")

        # Draw maze on canvas
        self.draw_maze(generator.display_maze())

    def draw_maze(self, maze):
        # Clear previous drawings
        self.canvas.delete("all")

        cell_size = 10
        maze_width = len(maze[0]) * cell_size
        maze_height = len(maze) * cell_size

        # Get the current size of the canvas
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 600

        # Calculate offsets to center the maze
        x_offset = (canvas_width - maze_width) // 2
        y_offset = (canvas_height - maze_height) // 2

        # Ensure maze is fully visible
        y_offset = 50

        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == '#':
                    self.canvas.create_rectangle(
                        x_offset + x * cell_size,
                        y_offset + y * cell_size,
                        x_offset + (x + 1) * cell_size,
                        y_offset + (y + 1) * cell_size,
                        fill="black"
                    )
                elif maze[y][x] == 'A':
                    self.canvas.create_rectangle(
                        x_offset + x * cell_size,
                        y_offset + y * cell_size,
                        x_offset + (x + 1) * cell_size,
                        y_offset + (y + 1) * cell_size,
                        fill="red"
                    )
                elif maze[y][x] == 'B':
                    self.canvas.create_rectangle(
                        x_offset + x * cell_size,
                        y_offset + y * cell_size,
                        x_offset + (x + 1) * cell_size,
                        y_offset + (y + 1) * cell_size,
                        fill="green"
                    )
                else:
                    self.canvas.create_rectangle(
                        x_offset + x * cell_size,
                        y_offset + y * cell_size,
                        x_offset + (x + 1) * cell_size,
                        y_offset + (y + 1) * cell_size,
                        fill="white"
                    )

    def solve_maze(self):
        # Clear previous solution images
        self.left_solution_label.config(image='')
        self.right_solution_label.config(image='')

        # Get selected algorithms
        left_algo = self.selected_left_algorithm.get()
        right_algo = self.selected_right_algorithm.get()

        left_time = None
        right_time = None

        # Solve and visualize left algorithm
        if left_algo:
            solver_class = self.algorithm_map.get(left_algo)
            if solver_class:
                solver = solver_class("generated_maze/m.txt")
                start_time = time.perf_counter()  # Use perf_counter for better resolution
                solver.solve()
                left_time = time.perf_counter() - start_time  # Calculate elapsed time
                left_time_ns = left_time * 1e9  # Convert to nanoseconds
                if left_algo == "A*":
                    left_filename = f"generated_maze/a_star_solution.png"
                else:
                    left_filename = f"generated_maze/{left_algo.lower()}_solution.png"
                directory = os.path.dirname(left_filename)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                solver.output_image(left_filename)

                # Display solution image with resizing
                left_image = Image.open(left_filename)
                left_image = left_image.resize(
                    (left_image.width // 2, left_image.height // 2), Image.Resampling.LANCZOS)
                left_photo = ImageTk.PhotoImage(left_image)
                self.left_solution_label.config(image=left_photo)
                self.left_solution_label.image = left_photo

        # Solve and visualize right algorithm
        if right_algo:
            solver_class = self.algorithm_map.get(right_algo)
            if solver_class:
                solver = solver_class("generated_maze/m.txt")
                start_time = time.perf_counter()  # Use perf_counter for better resolution
                solver.solve()
                right_time = time.perf_counter() - start_time  # Calculate elapsed time
                right_time_ns = right_time * 1e9  # Convert to nanoseconds
                if right_algo == "A*":
                    right_filename = f"generated_maze/a_star_solution.png"
                else:
                    right_filename = f"generated_maze/{right_algo.lower()}_solution.png"
                directory = os.path.dirname(right_filename)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                solver.output_image(right_filename)

                # Display solution image with resizing
                right_image = Image.open(right_filename)
                right_image = right_image.resize(
                    (right_image.width // 2, right_image.height // 2), Image.Resampling.LANCZOS)
                right_photo = ImageTk.PhotoImage(right_image)
                self.right_solution_label.config(image=right_photo)
                self.right_solution_label.image = right_photo

        # Show timing dialog with results
        if left_time is not None and right_time is not None:
            self.show_timing_dialog(left_time_ns, right_time_ns)  # Pass the timings in ns

    def show_timing_dialog(self, left_algo_time, right_algo_time):
        # Determine the winner
        if left_algo_time < right_algo_time:
            winner_text = "Left Algorithm Wins!"
            winner_color = "green"
        elif right_algo_time < left_algo_time:
            winner_text = "Right Algorithm Wins!"
            winner_color = "blue"
        else:
            winner_text = "It's a Tie!"
            winner_color = "purple"

        # Create the dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Algorithm Timing Results")
        dialog.geometry("400x250")
        dialog.configure(bg="white")

        # Title label
        title_label = tk.Label(dialog, text="Algorithm Timing Results", font=("Helvetica", 16, "bold"), bg="white", fg="black")
        title_label.pack(pady=10)

        # Player timing labels
        player1_label = tk.Label(dialog, text=f"Left Algorithm Time: {left_algo_time:.2f} ns", font=("Helvetica", 12), bg="white", fg="green")
        player1_label.pack(pady=5)

        player2_label = tk.Label(dialog, text=f"Right Algorithm Time: {right_algo_time:.2f} ns", font=("Helvetica", 12), bg="white", fg="blue")
        player2_label.pack(pady=5)

        # Winner label
        winner_label = tk.Label(dialog, text=winner_text, font=("Helvetica", 14, "bold"), bg="white", fg=winner_color)
        winner_label.pack(pady=15)

        # Close button
        close_button = tk.Button(dialog, text="Close", command=dialog.destroy, bg="#e74c3c", fg="white", font=("Helvetica", 10, "bold"))
        close_button.pack(pady=10)

def main():
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()