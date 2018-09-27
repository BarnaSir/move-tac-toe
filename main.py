from sys import maxsize
from math import hypot
from itertools import cycle

from tkinter import *

root = Tk()
root.title("Barna's board Game")
root.resizable(False, False)
frame = Frame(root, width=600, height=500)
frame.pack()
canvas = Canvas(frame, width=600, height=500, bg="white")
canvas.pack()
WIDTH = 600
HEIGHT = 500
GAP = 50
xPress = None
yPress = None
FilledUp = None
xRelease, yRelease = None, None
POINTS = ((GAP, GAP), (GAP, HEIGHT/2), (WIDTH-GAP, HEIGHT/2), (GAP, HEIGHT-GAP),
          (WIDTH-GAP, HEIGHT-GAP), (WIDTH/2, GAP), (WIDTH-GAP, GAP), (WIDTH/2, HEIGHT-GAP),
          (WIDTH/2, HEIGHT/2))
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
    global FilledUp
    if len(player_1.owned_position) == 3 and len(player_2.owned_position) == 3:
        FilledUp = 1
    if FilledUp != None:
        return
    toggle_turn()
    print("entered click event as ", current_player.name)
    global current_player
    x, y = event.x, event.y
    (a, b) = nearest_node(x, y)
    if a is None or not is_empty(a, b):
        return 0
    if all_filled():
        print("all are filled")
    # toggle_turn()
    if current_player.initial_choices != 0:
        current_player.initial_choices -= 1
        oval_obj = canvas.create_oval(a-20, b-20, a+20, b+20, fill=current_player.color_notation)
        # oval_obj.place(100, 100)
        current_player.owned_position[oval_obj] = (a, b)
        # print(current_player.owned_position)
        print(current_player.name, "made a move.")
        # print("Positions owned by", current_player.name, "are:", current_player.owned_position)
        status['text'] = current_player.name + " made a move"
        # toggle_turn()
        if player_1 == current_player:
            print("It's "+player_2.name+"'s turn now")
            status['text'] = status['text'] + ". It's "+player_2.name+"'s turn now"
        else:
            print("It's "+player_1.name+"'s turn now")
            status['text'] = status['text'] + ". It's "+player_1.name+"'s turn now"
    else:
        # current_player = players.__next__()
        # toggle_turn()
        pass

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


def double_click(event):
    print("entered double click fxn")
    # current_player = toggle_turn()
    print("entered as", current_player.name)
    global xPress, yPress, current_player
    a, b = nearest_node(event.x, event.y)
    if a is None: return
    if xPress == None and is_empty(a, b):
        return
    if len(player_1.owned_position) != 3 and len(player_2.owned_position) != 3:
        return
    # print("passed first if condition")
    print("Global variable is now", xPress)
    # current_player = players.__next__()
    # print("position owned by "+current_player.name+" " + str(len(current_player.owned_position)))
    # print("double clicked by ", current_player.name)
    if len(player_1.owned_position) == 3 and len(player_2.owned_position) == 3:
        toggle_turn()
    if not own_cell(a, b, current_player) and not is_empty(a, b):
        print("Not your piece")
        toggle_turn()
        return
    print("it's "+current_player.name+"'s turn now")
    if xPress == None and own_cell(a, b, current_player) and all_filled():
        xPress, yPress = a, b
        print("Doubled clicked by ", current_player.name)
        canvas.delete(get_oval_obj_key(a, b, current_player))
        current_player.owned_position.pop(get_oval_obj_key(a, b, current_player), None)
        # current_player = players.__next__()
    elif xPress != None and is_empty(a, b):
        # current_player = players.__next__()
        print("Doubled clicked by ", current_player.name)
        oval_obj = canvas.create_oval(a-20, b-20, a+20, b+20, fill=current_player.color_notation)
        current_player.owned_position[oval_obj] = (a, b)
        # toggle_turn()
        xPress = yPress = None

def toggle_turn():
    global current_player
    current_player = players.__next__()
    # return current_player

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

def check():
    pass

def is_empty(x, y):
    if player_1.owned_position or player_2.owned_position:
        if (x, y) in player_1.owned_position.values() or (x, y) in player_2.owned_position.values():
            return 0
    return 1

def all_filled():
    if len(player_1.owned_position) == len(player_2.owned_position) == 3:
        return 1

# def delete_node(x, y):

def one(event):
    print("pressed at ", event.x, event.y)


draw_grid()
print(POINTS)
player_1 = Player("Sudarshan", "Blue")
player_2 = Player("Barna", "Yellow")
# current_player = player_1
players_list = {player_1: player_2, player_2: player_1}
players = cycle([player_1, player_2])
status = Label(root, text="It's "+player_1.name+"'s turn now!" , bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
canvas.bind('<Double-Button-1>', double_click)
# canvas.bind('<ButtonPress-1>', one)
canvas.bind('<ButtonPress-1>', update)
# canvas.bind('<Double-Button-1>', lambda event: double_click(event, xpyp))
root.mainloop()