import World
import threading
import time
import sys

ACTIONS = World.ACTIONS
Q = {}
for x in range(World.BOARD_WIDTH):
    for y in range(World.BOARD_HEIGHT):
        temp = {}
        for action in ACTIONS:
            temp[action] = 0.1
        Q[(x, y)] = temp

for (pos, c, w) in World.exits:
    for action in ACTIONS:
        Q[pos][action] = w


def do_action(action):
    s = World.robot
    r = -World.score
    World.try_move(action)
    s2 = World.robot
    r += World.score
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc


def print_Q():
    for y in range(World.BOARD_HEIGHT):
        for x in range(World.BOARD_WIDTH):
            v = '{:.1f},{:.1f},{:.1f},{:.1f}'.format(Q[(x,y)][ACTIONS[0]]*10, Q[(x,y)][ACTIONS[1]]*10, Q[(x,y)][ACTIONS[2]]*10, Q[(x,y)][ACTIONS[3]]*10)
            sys.stdout.write('{:12} '.format(v))
        sys.stdout.write('\n')
        sys.stdout.flush()

def run():
    discount = 0.9
    time.sleep(1)
    alpha = 1
    t = 1
    while True:
        # Pick the right action
        s = World.robot
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.game_over:
            print_Q()
            World.restart_game()
            time.sleep(1)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.017)


t = threading.Thread(target=run)
t.daemon = True
t.start()
if len(sys.argv) == 1 or not (sys.argv[1] == 'd' or sys.argv[1] == 's'):
    print 'You must specify the type of game world: d for deterministic, s for stochastic'
else:
    World.start_game(sys.argv[1])

