import random
import time
from Tkinter import *

BOARD_WIDTH = 10
BOARD_HEIGHT = 10
CELL_SIZE = 50

ACTIONS = ["up", "down", "left", "right"]
MOVES = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

root = Tk()
root.attributes('-topmost',True)
board = Canvas(root, width=BOARD_WIDTH*CELL_SIZE, height=BOARD_HEIGHT*CELL_SIZE)

def generate_random_walls(num, exclude):
    a = []
    for i in range(num):
        while True:
            pos = (random.randrange(BOARD_WIDTH), random.randrange(BOARD_HEIGHT))
            if pos not in exclude and pos not in a:
                a.append(pos)
                break
    return a

def render_cell(position, color):
    (x, y) = position
    return board.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill=color)

def render_grid(walls, exits):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            render_cell((x, y), "white")
    
    for pos in walls:
        render_cell(pos, "black")
    
    for (pos, c, w) in exits:
        render_cell(pos, c)

robot = (0, BOARD_HEIGHT-1)
exits = [((BOARD_WIDTH-1, 0), "green", 1), ((BOARD_WIDTH-1, 1), "red", -1)]
score = 1
game_over = False
walk_reward = -0.04

# walls = generate_random_walls(BOARD_WIDTH*BOARD_HEIGHT/4, [robot] + [pos for (pos, c, w) in exits])
# walls = [(1, 1), (1, 2), (2, 1), (2, 2)]
walls = [(1,1), (1,2),(1,4),(1,6),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,4),(3,6),(4,1),(4,3),(5,1),(5,2),(5,3),(5,4),(6,1),(7,3),(7,5),(7,6),(7,7),(7,8),(8,2),(8,5),(8,8)]
render_grid(walls, exits)
me = render_cell(robot, "blue")
board.grid(row=0, column=0)

def move_robot(to):
    global robot, me
    dx = to[0] - robot[0]
    dy = to[1] - robot[1]
    board.move(me, dx*CELL_SIZE, dy*CELL_SIZE)
    robot = to


def try_move(action):
    global robot, score, walk_reward, game_over
    (dx, dy) = MOVES[action]
    new_x = robot[0] + dx
    new_y = robot[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < BOARD_WIDTH) and (new_y >= 0) and (new_y < BOARD_HEIGHT) and not ((new_x, new_y) in walls):
        move_robot((new_x, new_y))
    for (exit_pos, c, w) in exits:
        if (new_x, new_y) == exit_pos:
            score += w
            print "Game Over! Your score is: ", score
            game_over = True
            return


def restart_game():
    global score, game_over
    move_robot((0, BOARD_HEIGHT-1))
    score = 1
    game_over = False


def start_game():
    root.mainloop()
