from sys import maxsize
from math import hypot
from itertools import cycle

from tkinter import *

root = Tk()
root.title("Barna's board Game")
root.resizable(False, False)
frame = Frame(root, width=800, height=700)
frame.pack()
canvas = Canvas(frame, width=620, height=600, bg="white")
canvas.pack(side=BOTTOM)
WIDTH = HEIGHT = 600
GAP = 50
ONE_TIME_CONSTANT = 1
xPrev = None
yPrev = None
FilledUp = None
xRelease, yRelease = None, None
POINTS = [
            (GAP, GAP), (WIDTH//2, GAP), (WIDTH-GAP, GAP),
            (GAP, HEIGHT//2), (WIDTH//2, HEIGHT//2), (WIDTH-GAP, HEIGHT//2),
            (GAP, HEIGHT-GAP), (WIDTH//2, HEIGHT-GAP), (WIDTH-GAP, HEIGHT-GAP),
          ]
VALID_MOVES = {0: (1, 3, 4), 1: (0, 2, 4), 2: (1, 4, 5),
               3: (0, 4, 6), 4: (0, 1, 2, 3, 5, 6, 7, 8), 5: (4, 2, 8),
               6: (4, 3, 7), 7: (4, 6, 8), 8: (4, 5, 7) }
GRID_POINTS = {
               0: (GAP, GAP, WIDTH-GAP, GAP),
               1: (GAP, HEIGHT/2, WIDTH-GAP, HEIGHT/2),
               2: (GAP, HEIGHT-GAP, WIDTH-GAP, HEIGHT-GAP),
               3: (WIDTH/2, GAP, WIDTH/2, HEIGHT-GAP),
               4: (WIDTH-GAP, GAP, WIDTH-GAP, HEIGHT-GAP),
               5: (GAP, GAP, WIDTH-GAP, HEIGHT-GAP),
               6: (GAP, HEIGHT-GAP, WIDTH-GAP, GAP),
               7: (GAP, GAP, GAP, HEIGHT-GAP)
              }

class Player:

    def __init__(self, name, color_notation):
        self.name = name
        self.color_notation = color_notation
        self.initial_choices = 3
        self.owned_position = {}


def draw_grid():
    for i in range(8):
        canvas.create_line(GRID_POINTS[i][0], GRID_POINTS[i][1], GRID_POINTS[i][2], GRID_POINTS[i][3])


def update(event):
    global FilledUp, current_player
    if len(player_1.owned_position) == 3 and len(player_2.owned_position) == 3:
        FilledUp = 1
    if FilledUp != None:
        return
    toggle_turn()
    x, y = event.x, event.y
    (a, b) = nearest_node(x, y)
    if a is None or not is_empty(a, b):
        toggle_turn()
        return 0
    if all_filled():
        print("all are filled")
    if current_player.initial_choices != 0:
        current_player.initial_choices -= 1
        oval_obj = canvas.create_oval(a-20, b-20, a+20, b+20, fill=current_player.color_notation)
        current_player.owned_position[oval_obj] = (a, b)
        print(current_player.name, "made a move.")
        status_bar()
    else:
        pass
    if check_game():
        result()

def result():
    print("Game won by ", current_player.name)
    status['text'] = "Game Over!!!  " + current_player.name + " wins."
    canvas.unbind("<Button-1>")
    canvas.unbind("<Double-Button-1>")

def nearest_node(x, y):
    temp = maxsize
    for i in range(9):
        distance = hypot(x-POINTS[i][0], y-POINTS[i][1])
        if distance < temp:
            temp = distance
            nearest_point = (POINTS[i][0], POINTS[i][1])
    if temp > 30:
        return None, None
    return nearest_point

def valid_double_click():
    return

def double_click(event):
    global xPrev, yPrev, current_player, FilledUp, ONE_TIME_CONSTANT
    if FilledUp != 1:
        return 0
    a, b = nearest_node(event.x, event.y)
    if (a is None) or (xPrev == None and is_empty(a, b)) or (len(player_1.owned_position) != 3 and len(player_2.owned_position) != 3):
        return

    if ONE_TIME_CONSTANT == 1:
        toggle_turn()

    info['text'] = ""
    if xPrev != None and not is_empty(a, b):
        info['text'] = "The position is not empty"
        return 0
    if not own_cell(a, b, current_player) and not is_empty(a, b):
        if xPrev == None:
            info['text'] = "That's not your piece"
        else:
            info['text'] = "The position is not empty"
        return
    if xPrev == None and own_cell(a, b, current_player) and FilledUp==1:
        ONE_TIME_CONSTANT -= 1
        xPrev, yPrev = a, b
        current_index = POINTS.index((a,b))
        if not is_valid_move_empty_cell(VALID_MOVES[current_index]):
            info['text'] = "IMMOVABLE"
            xPrev, yPrev = None, None
            return False
        canvas.itemconfig(get_oval_obj_key(a, b, current_player), outline="white", width=7)
    elif xPrev != None and is_empty(a, b) and legal_move(a, b, xPrev, yPrev):
        oval_obj = canvas.create_oval(a-20, b-20, a+20, b+20, fill=current_player.color_notation)
        canvas.delete(get_oval_obj_key(xPrev, yPrev, current_player))
        current_player.owned_position.pop(get_oval_obj_key(xPrev, yPrev, current_player), None)
        current_player.owned_position[oval_obj] = (a, b)
        if check_game():
            result()
        else:
            status_bar()
        toggle_turn()
        if xPrev == a and yPrev == b:
            toggle_turn()
        xPrev = yPrev = None


def legal_move(x, y, xPrev, yPrev):
    if xPrev == x and yPrev == y:
        return True
    current_index = POINTS.index((x, y))
    previous_index = POINTS.index((xPrev, yPrev))
    print(VALID_MOVES[previous_index])
    if current_index in VALID_MOVES[previous_index]:
        return True
    info['text'] = "INVALID MOVE"
    return False

def is_valid_move_empty_cell(tupp):
    for i in tupp:
        x, y = POINTS[i]
        if is_empty(x, y):
            return True
    return False

def is_movable():
    pass

def toggle_turn():
    global current_player
    current_player = players.__next__()

def status_bar():
    if current_player == player_1:
        status['text'] = "Turn: " + player_2.name + "(" + player_2.color_notation + ")"
    else:
        status['text'] = "Turn: " + player_1.name + "(" + player_1.color_notation + ")"


def move_condition():
    if len(player_1.owned_position) == 3 or len(player_2.owned_position) == 3:
        return 1

def own_cell(x, y, current_player):
    if (x, y) in current_player.owned_position.values():
        return 1

def get_oval_obj_key(x, y, current_player):
    for key, val in current_player.owned_position.items():
        if val == (x, y):
            return key

def check_game():
    global current_player
    coordinates = tuple(current_player.owned_position.values())
    if len(coordinates) != 3:
        return 0
    x1, y1 = coordinates[0][0], coordinates[0][1]
    x2, y2 = coordinates[1][0], coordinates[1][1]
    x3, y3 = coordinates[2][0], coordinates[2][1]
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)


def is_empty(x, y):
    if player_1.owned_position or player_2.owned_position:
        if (x, y) in player_1.owned_position.values() or (x, y) in player_2.owned_position.values():
            return 0
    return 1

def all_filled():
    if len(player_1.owned_position) == len(player_2.owned_position) == 3:
        return 1


draw_grid()
player_1 = Player("Sudarshan", "Blue")
player_2 = Player("Barna", "Yellow")
players_list = {player_1: player_2, player_2: player_1}
players = cycle([player_1, player_2])
info = Label(root, text="", font="Times 13")
info.pack(side=RIGHT)
status = Label(root, text="Turn: "+player_2.name + "(" + player_2.color_notation + ")" , bd=1, relief=SUNKEN, anchor=W, font="Times 13")
status.pack(side=BOTTOM, fill=X)
toggle_turn()
canvas.bind('<Double-Button-1>', double_click)
canvas.bind('<ButtonPress-1>', update)
root.mainloop()