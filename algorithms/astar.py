from PIL import Image, ImageDraw
import heapq
import time

class MazeSolverAStar:
    def __init__(self, filename):
        self.load_maze(filename)
    
    def load_maze(self, filename):
        with open(filename) as f:
            self.maze = [list(line.strip()) for line in f.readlines()]
        self.start = self.find_position('A')
        self.goal = self.find_position('B')
    
    def find_position(self, char):
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if col == char:
                    return (y, x)
        return None

    def heuristic(self, a, b):
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, position):
        y, x = position
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]) and self.maze[ny][nx] != '#':
                result.append((ny, nx))
        return result

    def solve(self):
        start_time = time.perf_counter()
        frontier = [(0, self.start)]
        came_from = {self.start: None}
        cost_so_far = {self.start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == self.goal:
                break

            for neighbor in self.neighbors(current):
                new_cost = cost_so_far[current] + 1  # Each step has a cost of 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, self.goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        path = []
        current = self.goal
        while current:
            path.append(current)
            current = came_from.get(current)
        path.reverse()

        self.solution = path if path and path[0] == self.start else None
        end_time = time.perf_counter()
        print(f"Time taken by A*: {(end_time - start_time) * 1_000_000:.2f} µs")
        return self.solution

    def output_image(self, filename="astar_solution.png"):
        cell_size = 20
        img = Image.new("RGBA", (len(self.maze[0]) * cell_size, len(self.maze) * cell_size), "black")
        draw = ImageDraw.Draw(img)

        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                color = (255, 255, 255) if col == ' ' else (0, 0, 0)
                if (y, x) == self.start:
                    color = (255, 0, 0)
                elif (y, x) == self.goal:
                    color = (0, 255, 0)
                if self.solution and (y, x) in self.solution:
                    color = (255, 255, 0)
                draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill=color)

        img.save(filename)

if __name__ == "__main__":
    solver = MazeSolverAStar("complex_maze.txt")
    solver.solve()
    solver.output_image("astar_solution.png")