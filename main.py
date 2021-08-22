import pygame
import math
from queue import PriorityQueue

from pygame.constants import GL_SHARE_WITH_CURRENT_CONTEXT, WINDOWHITTEST

WIDTH = 800
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pathfinder")


RED = (255,0,0) # Represents Closed Node
GREEN = (0,255,0) # Represents Open Node
WHITE = (225,225,225) # Reset/Default Node
BLACK =(0,0,0) # Represents Node that is a barrier
ORANGE = (255,165,0) # Represents start and End node


class node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width 
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col 
    
    def reset(self):
        self.color = WHITE      
    
    def make_path(self):
        self.color = (64,244,208)
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.width))

    def check_neighbors(self,grid):
        if self.row < self.total_rows -1 and not grid[self.row + 1][self.col].color == BLACK: #checks neighbor one block up down
            self.neighbors.append(grid[self.row + 1][self.col])
       
        if self.row > 0 and not grid[self.row - 1][self.col].color == BLACK: #checks neighbor one block up
            self.neighbors.append(grid[self.row - 1][self.col])
       
        if self.col < self.total_rows -1 and not grid[self.row ][self.col + 1].color == BLACK: #checks neighbor one block up right
            self.neighbors.append(grid[self.row ][self.col +1])
       
        if self.col > 0  and not grid[self.row ][self.col - 1].color == BLACK: #checks neighbor one block up left
            self.neighbors.append(grid[self.row ][self.col -1])

# Calculates shortest estimated distance
def heuristic(point_1,point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(y2-y1) + abs(x2-x1)

def reconstruct_path(came_from, current ,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start ))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end: #make path
            reconstruct_path(came_from, end, draw)
            end.color = ORANGE
            start.color = ORANGE
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = GREEN

        draw()

        if current != start:
            current.color = RED

    return False


def make_grid(rows,width):
    grid = []
    size = width // rows    # determines size/gap of each individual cube on the grid
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            Node = node(i, j, size, rows)
            grid[i].append(Node)

    return grid

def draw_grid(win, rows, width): #Grid Lines
    size = width // rows
    for i in range(rows):
        pygame.draw.line(win, (128,128,128), (0, i * size),(width, i * size))
        for j in range(rows):
            pygame.draw.line(win, (128,128,128), (j * size, 0), (j * size, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:        # draw cubes with colors
        for node in row:
            node.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    size = width // rows
    y , x = pos

    row = y // size
    col = x // size
    
    return row, col

def main(win, width):
    rows = 50       
    grid = make_grid(rows, width)
    start = None
    end = None

    run = True
    started = False
    while run:
        
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: #left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.color = ORANGE
            
                elif not end and node != start:
                    end = node
                    end.color = ORANGE
            
                elif node != end and node != start:
                    node.color = BLACK

            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN: # start pathfinding algorithm 
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                      for node in row:
                        node.check_neighbors(grid)
                   
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()

main(WIN, WIDTH)

    
