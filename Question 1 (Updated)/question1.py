import heapq  # priority queue for frontier
import itertools  # counter for tie-breaking in heap
import collections  # deque for BFS
import os  # file path handling
import time  # performance timing
from PIL import Image, ImageDraw, ImageFont  # image creation for visualization

# Drawing settings
CELL_SIZE      = 40
FONT           = ImageFont.load_default()
GRID_COLOR     = (50, 50, 50)
WALL_COLOR     = "grey"
EXPLORED_COLOR = "gold"
PATH_COLOR     = (0, 100, 0)
START_COLOR    = "red"
GOAL_COLOR     = "lightgreen"
TEXT_COLOR     = "white"

# ANSI codes for terminal display
ANSI_RESET       = "\033[0m"
ANSI_RED         = "\033[31m"
ANSI_LIGHT_GREEN = "\033[92m"
ANSI_YELLOW      = "\033[33m"
ANSI_GREEN       = "\033[32m"
ANSI_GREY        = "\033[90m"

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, priority=0):
        self.state = state          # (x, y) position
        self.parent = parent        # previous Node in path
        self.action = action        # move taken to reach this state
        self.cost = cost            # g(n): steps from start
        self.priority = priority    # f(n) or h(n): used by frontier

class Maze:
    def __init__(self, filepath):
        # Load maze from text file and pad rows to equal width
        raw = [list(line.rstrip("\n")) for line in open(filepath)]
        h, w = len(raw), max(len(r) for r in raw)
        for r in raw:
            if len(r) < w:
                r.extend('#' * (w - len(r)))

        # Remove full border if it's all walls
        if (all(c=='#' for c in raw[0]) and all(c=='#' for c in raw[-1]) and
            all(raw[y][0]=='#' for y in range(h)) and all(raw[y][-1]=='#' for y in range(h))):
            raw = [row[1:-1] for row in raw[1:-1]]
            h, w = h-2, w-2

        self.grid, self.walls = raw, set()
        self.height, self.width = h, w
        self.start = self.goal = None

        # Identify start (A), goal (B), and walls (#)
        for y, row in enumerate(raw):
            for x, ch in enumerate(row):
                if ch == 'A':
                    self.start = (x, y)
                    self.grid[y][x] = ' '
                elif ch == 'B':
                    self.goal = (x, y)
                    self.grid[y][x] = ' '
                elif ch == '#':
                    self.walls.add((x, y))

    def neighbours(self, s):
        # Yield adjacent non-wall cells
        x, y = s
        for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.walls:
                yield (nx, ny)

    def heuristic(self, s):
        # Manhattan distance to goal
        x1, y1 = s
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)

    def bfs_distances(self):
        # Precompute shortest-path distances from start with BFS
        dist = {self.start: 0}
        q = collections.deque([self.start])
        while q:
            u = q.popleft()
            for v in self.neighbours(u):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist

    def solve(self, algorithm="greedy"):
        # General search using Greedy Best-First or A*
        counter = itertools.count()  # tie-breaker for heap
        h0 = self.heuristic(self.start)
        start = Node(self.start, cost=0, priority=h0)
        frontier = [(h0, next(counter), start)]
        explored = set()
        dist_map = {}
        expanded = 0
        t0 = time.perf_counter()
        dir_map = {(0,-1):"up", (0,1):"down", (-1,0):"left", (1,0):"right"}

        while frontier:
            _, _, node = heapq.heappop(frontier)
            expanded += 1

            # Check goal
            if node.state == self.goal:
                dt = time.perf_counter() - t0
                states, actions = [], []
                cur = node
                while cur.parent:
                    states.append(cur.state)
                    actions.append(cur.action)
                    cur = cur.parent
                states.reverse(); actions.reverse()
                print(f"{algorithm.upper():6} ✔ expanded {expanded} in {dt:.3f}s, length={len(states)}")
                return states, explored, dist_map

            if node.state in explored:
                continue
            explored.add(node.state)
            dist_map[node.state] = node.priority
            x, y = node.state

            # Expand neighbours
            for nbr in self.neighbours(node.state):
                if nbr in explored:
                    continue
                dx, dy = nbr[0] - x, nbr[1] - y
                action = dir_map[(dx, dy)]
                g = node.cost + 1
                h = self.heuristic(nbr)
                if algorithm == "greedy":
                    pr = h
                elif algorithm == "astar":
                    pr = g + h
                else:
                    raise ValueError(f"Unknown algorithm: {algorithm}")
                child = Node(nbr, parent=node, action=action, cost=g, priority=pr)
                dist_map[nbr] = pr
                heapq.heappush(frontier, (pr, next(counter), child))

        raise ValueError(f"No path via {algorithm}")

    def draw(self, path, explored, dist_map, algorithm, label, out_png):
        # Visualize maze, explored states, and path to PNG
        values = {}
        if algorithm == "astar":
            gmap = self.bfs_distances()

        # Assign display values for each cell
        for y in range(self.height):
            for x in range(self.width):
                cell = (x, y)
                if cell in self.walls:
                    continue
                if cell in dist_map:
                    values[cell] = dist_map[cell]
                else:
                    if algorithm == "greedy":
                        values[cell] = self.heuristic(cell)
                    elif algorithm == "astar":
                        values[cell] = gmap.get(cell, 0) + self.heuristic(cell)

        # Create image canvas
        W, H = self.width * CELL_SIZE, self.height * CELL_SIZE + 30
        img = Image.new("RGB", (W, H), "black")
        d = ImageDraw.Draw(img)
        d.text((5, 5), label, fill=TEXT_COLOR, font=FONT)
        base = 30

        # Draw each cell
        for y in range(self.height):
            for x in range(self.width):
                L, T = x*CELL_SIZE, base + y*CELL_SIZE
                R, B = L + CELL_SIZE, T + CELL_SIZE
                cell = (x, y)
                if cell in self.walls:
                    col = WALL_COLOR
                elif cell == self.start:
                    col = START_COLOR
                elif cell == self.goal:
                    col = GOAL_COLOR
                elif cell in path:
                    col = PATH_COLOR
                elif cell in explored:
                    col = EXPLORED_COLOR
                else:
                    col = "black"
                d.rectangle([L, T, R, B], fill=col)

                # Overlay the value if available
                if cell in values:
                    txt = str(values[cell])
                    bb = d.textbbox((0, 0), txt, font=FONT)
                    wtxt, htxt = bb[2]-bb[0], bb[3]-bb[1]
                    d.text((L + (CELL_SIZE-wtxt)/2, T + (CELL_SIZE-htxt)/2),
                           txt, fill=TEXT_COLOR, font=FONT)

        # Draw grid lines
        for x in range(self.width+1):
            d.line([(x*CELL_SIZE, base), (x*CELL_SIZE, base+self.height*CELL_SIZE)], fill=GRID_COLOR)
        for y in range(self.height+1):
            d.line([(0, base+y*CELL_SIZE), (self.width*CELL_SIZE, base+y*CELL_SIZE)], fill=GRID_COLOR)

        img.save(out_png)

    def print_terminal(self, path, explored):
        # Print maze to terminal with ANSI colours
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                c = (x, y)
                if c == self.start:
                    row += ANSI_RED + "A" + ANSI_RESET
                elif c == self.goal:
                    row += ANSI_LIGHT_GREEN + "B" + ANSI_RESET
                elif c in self.walls:
                    row += ANSI_GREY + "#" + ANSI_RESET
                elif c in path:
                    row += ANSI_GREEN + "*" + ANSI_RESET
                elif c in explored:
                    row += ANSI_YELLOW + "." + ANSI_RESET
                else:
                    row += " "
            print("   " + row)
        print()

if __name__ == "__main__":
    root = os.path.dirname(__file__)
    for sub in ["Easy", "Medium", "Hard"]:
        fld = os.path.join(root, sub)
        txts = [f for f in os.listdir(fld) if f.endswith(".txt")]
        if len(txts) != 1:
            print(f"⚠ Skipping {sub}, found {len(txts)} .txt")
            continue
        lvl = sub.lower()
        maze = Maze(os.path.join(fld, txts[0]))

        # Original (no search)
        out0 = os.path.join(fld, f"{lvl}_original.png")
        maze.draw([], set(), {}, "original", f"{sub} Original", out0)
        print(f"Saved: {sub}/{os.path.basename(out0)}")

        # Greedy Best-First Search
        p, e, dm = maze.solve("greedy")
        maze.print_terminal(p, e)
        out1 = os.path.join(fld, f"{lvl}_greedy.png")
        maze.draw(p, e, dm, "greedy", f"{sub} Greedy h(n)", out1)
        print(f"Saved: {sub}/{os.path.basename(out1)}")

        # A* Search
        p, e, dm = maze.solve("astar")
        maze.print_terminal(p, e)
        out2 = os.path.join(fld, f"{lvl}_astar.png")
        maze.draw(p, e, dm, "astar", f"{sub} A* f(n)=g+h", out2)
        print(f"Saved: {sub}/{os.path.basename(out2)}")

    print("✅ All done!")
