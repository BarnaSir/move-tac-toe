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
    print("entered click event as ", current_player.name)
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
        print("Game won by ", current_player.name)
        status['text'] = "the window will be closed soon"
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


def double_click(event):
    global xPrev, yPrev, current_player, FilledUp
    if FilledUp != 1:
        return 0
    print("entered double click fxn")
    # current_player = toggle_turn()
    print("entered as", current_player.name)
    a, b = nearest_node(event.x, event.y)
    if a is None: return
    if xPrev == None and is_empty(a, b):
        return
    if len(player_1.owned_position) != 3 and len(player_2.owned_position) != 3:
        return
    # print("passed first if condition")
    print("Global variable is now", xPrev)
    # current_player = players.__next__()
    # print("position owned by "+current_player.name+" " + str(len(current_player.owned_position)))
    # print("double clicked by ", current_player.name)
    info['text'] = ""
    if len(player_1.owned_position) == 3 and len(player_2.owned_position) == 3:
        toggle_turn()
    if not own_cell(a, b, current_player) and not is_empty(a, b):
        print("Not your piece")
        info['text'] = "That's not your piece"
        toggle_turn()
        return
    print("it's "+current_player.name+"'s turn now")
    if xPrev == None and own_cell(a, b, current_player) and all_filled():
        xPrev, yPrev = a, b
        print("Doubled clicked by ", current_player.name)
        canvas.delete(get_oval_obj_key(a, b, current_player))
        current_player.owned_position.pop(get_oval_obj_key(a, b, current_player), None)
        # current_player = players.__next__()
    elif xPrev != None and is_empty(a, b) and legal_move(a, b, xPrev, yPrev):
        # current_player = players.__next__()
        print("Doubled clicked by ", current_player.name)
        oval_obj = canvas.create_oval(a-20, b-20, a+20, b+20, fill=current_player.color_notation)
        current_player.owned_position[oval_obj] = (a, b)
        # toggle_turn()
        xPrev = yPrev = None
    print("position owned by "+current_player.name+" are " + str(current_player.owned_position))
    status_bar()
    if check_game():
        print("Game won by ", current_player.name)
        status['text'] = "the window will be closed soon"
        # exit(0)
        canvas.unbind("<Button-1>")
        canvas.unbind("<Double-Button-1>")

def legal_move(x, y, xPrev, yPrev):
    print("current position is", x, y)
    print("previous position is", xPrev, yPrev)
    print(POINTS)
    current_index = POINTS.index((x, y))
    previous_index = POINTS.index((xPrev, yPrev))
    if current_index in VALID_MOVES[previous_index]:
        return True

def game_finished():
    print("game over")

def toggle_turn():
    global current_player
    current_player = players.__next__()
    # return current_player

def status_bar():
    if current_player == player_1:
        print("It's " + player_2.name + "'s turn now")
        status['text'] = "Turn: " + player_2.name + "(" + player_2.color_notation + ")"
    else:
        print("It's " + player_1.name + "'s turn now")
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
    check_list = tuple(current_player.owned_position.values())
    print("went to check game and found check_list")
    print(check_list)
    if len(check_list) != 3:
        return 0
    return (check_list[0][0] == check_list[1][0] == check_list[2][0]) \
           or (check_list[0][1] == check_list[1][1] == check_list[2][1]) \
           or ((check_list[0][0] == check_list[0][1]) and (check_list[1][0] == check_list[1][1]) and (check_list[2][0] == check_list[2][1])) \
           or (((check_list[0][0] == check_list[0][1]) or (check_list[1][0] == check_list[1][1]) or (check_list[2][0] == check_list[2][1])) and addfn(check_list))

def addfn(check_list):
    return (check_list[0] == check_list[1][::-1] or check_list[0] == check_list[2][::-1] or check_list[1] == check_list[2][::-1]) and ((WIDTH//2, HEIGHT//2) in check_list)

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
players_list = {player_1: player_2, player_2: player_1}
players = cycle([player_1, player_2])
info = Label(root, text="", font="Times 13")
info.pack(side=RIGHT)
status = Label(root, text="Turn: "+player_2.name + "(" + player_2.color_notation + ")" , bd=1, relief=SUNKEN, anchor=W, font="Times 13")
status.pack(side=BOTTOM, fill=X)
toggle_turn()
canvas.bind('<Double-Button-1>', double_click)
# canvas.bind('<ButtonPress-1>', one)
canvas.bind('<ButtonPress-1>', update)
# canvas.bind('<Double-Button-1>', lambda event: double_click(event, xpyp))
root.mainloop()