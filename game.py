from queue import Queue
from random import randint
import pygame
import time
from parse_maze import parse_maze_png

grid_height = 31
grid_width = 28
maze_png_filename = 'maze.png'
grid_filename = 'grid.pac'

grid = parse_maze_png(
    maze_png_filename,
    grid_filename,
    0,  # randint(0, 3),
    0,  # randint(0, 3)
)


def vert(pos):
    y, x = pos
    return y*grid_width + x


class Graph:
    def __init__(self, v_n: int):
        self.adj = [set() for _ in range(v_n)]

    def add_edge(self, u: int, v: int):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def import_grid(self, grid):
        for y in range(grid_height):
            for x in range(grid_width):
                if not grid[y][x]:
                    v = vert((y, x))

                    left = y, x-1
                    right = y, x+1
                    up = y-1, x
                    down = y+1, x

                    if x-1 >= 0 and not grid[y][x-1]:
                        self.add_edge(v, vert(left))
                    if x+1 < grid_width and not grid[y][x+1]:
                        self.add_edge(v, vert(right))
                    if y-1 >= 0 and not grid[y-1][x]:
                        self.add_edge(v, vert(up))
                    if y+1 < grid_height and not grid[y+1][x]:
                        self.add_edge(v, vert(down))


def shortest_path(g, u, v, pre):
    q = Queue()
    visited = [0 for _ in range(len(g.adj))]
    dist = [float('inf') for _ in range(len(g.adj))]
    for i in range(len(g.adj)):
        pre[i] = None

    q.put(u)
    visited[u] = True
    dist[u] = 0

    while not q.empty():
        cur = q.get()

        for neigh in g.adj[cur]:
            if not visited[neigh]:
                visited[neigh] = True
                dist[neigh] = dist[cur] + 1
                pre[neigh] = cur
                q.put(neigh)
                if neigh == v:
                    return True
    return False


def get_shortest_path(g, u, v):
    pre = [None for _ in range(len(g.adj))]
    shortest_path(g, u, v, pre)
    yield v
    pred = pre[v]
    while pred is not None:
        yield pred
        pred = pre[pred]


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


pygame.init()
scale = 15
screen_width = 28 * scale
screen_height = 31 * scale
display = pygame.display.set_mode((screen_width, screen_height))
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
display.fill(black)

for y, row in enumerate(grid):
    for x, tile in enumerate(row):
        if grid[y][x]:
            pygame.draw.rect(display, blue, (x*scale, y*scale, scale, scale))


def get_tunnels(grid):
    for i in range(grid_height):
        if not grid[i][0]:
            yield vert((i, 0))


def draw_obj_from_xy(x, y, col=random_color()):
    pygame.draw.rect(display, col, (x*scale, y*scale, scale, scale))


def draw_obj_from_n(tile, col=random_color()):
    x = (tile % grid_width) * scale
    y = (tile // grid_width) * scale
    pygame.draw.rect(display, col, (x, y, scale, scale))


g = Graph(grid_width*grid_height)
g.import_grid(grid)

for i in get_tunnels(grid):
    g.add_edge(i, i + grid_width - 1)

# init pos of ghost
ghost_t = vert((1, 1))

# init pos of pacman
pact = vert((17, 14))
pacv = 1
done = False
while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                pacv = -1
            elif e.key == pygame.K_RIGHT:
                pacv = 1
            elif e.key == pygame.K_UP:
                pacv = -grid_width
            elif e.key == pygame.K_DOWN:
                pacv = grid_width

    if pact % grid_width == 0 and pacv == -1:
        next_tile = pact + grid_width - 1
    elif pact % grid_width == grid_width - 1 and pacv == 1:
        next_tile = pact - grid_width + 1
    else:
        next_tile = pact + pacv

    if next_tile in g.adj[pact]:
        draw_obj_from_n(next_tile, yellow)
        draw_obj_from_n(pact, black)
        pact = next_tile

    short = [i for i in get_shortest_path(g, ghost_t, pact)][::-1]

    try:
        next_tile = short[1]
    except IndexError:
        done = True

    draw_obj_from_n(ghost_t, black)
    draw_obj_from_n(next_tile, red)
    ghost_t = next_tile

    time.sleep(0.1)

    pygame.display.update()
