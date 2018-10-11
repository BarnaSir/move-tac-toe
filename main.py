#!/usr/bin/env python3
import sys

from collections import namedtuple
from math import hypot
from itertools import cycle
from playsound import playsound

from tkinter import *
from tkinter import messagebox

from ai import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
WIDTH = HEIGHT = 600
GAP = 50
ONE_TIME_CONSTANT = 1
ALLOW_SINGLE_CLICK = 1
xRelease, yRelease = None, None
from_y = from_x = None
picked_status = 0
debug = 0

POINTS = [
    (GAP, GAP), (WIDTH//2, GAP), (WIDTH-GAP, GAP),
    (GAP, HEIGHT//2), (WIDTH//2, HEIGHT//2), (WIDTH-GAP, HEIGHT//2),
    (GAP, HEIGHT-GAP), (WIDTH//2, HEIGHT-GAP), (WIDTH-GAP, HEIGHT-GAP),
]

VALID_MOVES = {
    0: (1, 3, 4), 1: (0, 2, 4), 2: (1, 4, 5),
    3: (0, 4, 6), 4: (0, 1, 2, 3, 5, 6, 7, 8), 5: (4, 2, 8),
    6: (4, 3, 7), 7: (4, 6, 8), 8: (4, 5, 7)
}

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

nt = namedtuple('Player', ['name', 'color_notation'])

class Player(nt):

    owned_position = {}
    remaining_piece = 3

    def __init__(self, name, color_notation):
        super().__init__()


def draw_grid(canvas):
    for i in range(8):
        canvas.create_line(GRID_POINTS[i][0], GRID_POINTS[i][1], GRID_POINTS[i][2],
                           GRID_POINTS[i][3], width=4)


def get_nearest_node(x, y):
    """
    Grabs the nearest location if it's clicked within the near boundary of any location.
    If the given coordinate can't be associated with any location, it returns None, None.
    """
    temp = sys.maxsize
    for i in range(9):
        distance = hypot(x-POINTS[i][0], y-POINTS[i][1])
        if distance < temp:
            temp = distance
            nearest_point = (POINTS[i][0], POINTS[i][1])
    if temp > 40:
        return None, None
    return nearest_point


def own_cell(x, y, player):
    """
    Returns True if the given coordinate is associated
    with current player.
    """
    if (x, y) in player.owned_position.values(): return 1


def get_oval_obj_key(x, y, player):
    """
    Returns the index of the piece (determined from given coordinates)
    """
    for key, val in player.owned_position.items():
        if val == (x, y):
            return key


def is_empty(x, y):
    """
    Checks if the node determined from given coordinate is empty.
    """
    if player_1.owned_position or player_2.owned_position:
        if (x, y) in player_1.owned_position.values() or (x, y) in player_2.owned_position.values():
            return 0
    return 1


def is_movable(a, b):
    """
    It checks whether the selected object is movable.
    Any object is movable if it's valid move has empty location.
    """
    current_index = POINTS.index((a, b))
    for i in VALID_MOVES[current_index]:
        x, y = POINTS[i]
        if is_empty(x, y):
            return 1
    return 0


def can_move_piece():
    """
    Determines whether the filling of piece is finished and pieces can be moved.
    """
    info['text'] = ""
    if player_1.remaining_piece == 0 and player_2.remaining_piece == 0:
        return 1


def valid_move_has_empty_cell(tupp):
    """
    Checks if the move is completely valid by checking whether
    the destined location is empty.
    """
    for i in tupp:
        x, y = POINTS[i]
        if is_empty(x, y):
            return True
    return False


def legal_move(x, y, x_prev=None, y_prev=None):
    """
    Returns True if the move is valid. Otherwise, False.
    """
    if x_prev == x and y_prev == y:
        return True
    current_index = POINTS.index((x, y))
    previous_index = POINTS.index((x_prev, y_prev))
    if current_index in VALID_MOVES[previous_index]:
        return True
    info['text'] = "Invalid Move  "
    return False


def check_moving_condition(a, b, x_prev, y_prev):
    """
    Returns true if move condition is valid.
    """
    return a is not None and x_prev is not None and is_empty(a, b) and legal_move(a, b, x_prev, y_prev)


def bring_oval_in_motion(event, obj_index):
    """
    Brings the currently selected piece into motion by floating it.
    """
    canvas.coords(obj_index, event.x-30, event.y-30, event.x+30, event.y+30)


def stop_floating_obj(from_x, from_y, current_player):
    """
    If a piece is made to move to the invalid location, then this function is called.
    It will unbind the motion, thus stopping the motion of floating object and relocates
    to the original place.
    """
    canvas.unbind("<Motion>")
    index_of_obj = get_oval_obj_key(from_x, from_y, current_player)
    if index_of_obj is None:
        return 0
    canvas.coords(index_of_obj, from_x - 30, from_y - 30, from_x + 30,
                  from_y + 30)


def move_a_piece(a, b, x_prev, y_prev):
    """
    Creates a piece in a new position and deletes from old position.
    """
    oval_obj = canvas.create_oval(a-30, b-30, a+30, b+30, fill=current_player.color_notation)
    canvas.delete(get_oval_obj_key(x_prev, y_prev, current_player))
    current_player.owned_position.pop(get_oval_obj_key(x_prev, y_prev, current_player), None)
    current_player.owned_position[oval_obj] = (a, b)


def toggle_turn():
    global current_player
    current_player = players.__next__()
    status['text'] = "  Turn: " + current_player.color_notation


def fill_pieces(a, b, current_player):
    """
    Fills the empty location with the pieces of current player.
    """
    oval_obj = canvas.create_oval(a-30, b-30, a+30, b+30, fill=current_player.color_notation)
    current_player.owned_position[oval_obj] = (a, b)
    current_player.remaining_piece -= 1
    playsound("sounds/filling.wav")
    if check_game():
        show_result()
        return 1
    toggle_turn()


def float_piece(from_x, from_y, current_player):
    """
    Brings the current piece into motion by using bring_oval_into_motion.
    """
    index_of_obj = get_oval_obj_key(from_x, from_y, current_player)
    canvas.bind("<Motion>", lambda event: bring_oval_in_motion(event, index_of_obj))
    return 1


def move_pieces(a, b, from_x, from_y):
    """
    Moves piece, unbinds the motion event listener and checks if the
    current user has won the game. If the game is not over, then it toggles the turn.
    """
    canvas.unbind("<Motion>")
    move_a_piece(a, b, from_x, from_y)
    playsound("sounds/moving.wav")
    if check_game():
        show_result()
        return 0
    toggle_turn()


def prevent_function(a, b, current_player):
    """
    Determines whether the pick current player is trying to make is valid. Valid pick is one if
    current user owns the piece and it is movable.
    """
    if not own_cell(a, b, current_player):
        info['text'] = "Not your piece.  "
        return 1
    if not is_movable(a, b):
        info['text'] = "Immovable!  "
        return 1


def is_invalid_drop(a, b, picked_status):
    """
    Returns whether the floating object is dropped in the legal valid place.
    """
    return a is None or ((a is None  or not is_empty(a, b)) and can_move_piece() and picked_status == 1)


def bypass_release_once(button_release):
    """
    Clicking/dragging consists of two events:- ButtonPress and ButtonRelease.
    During each event, the function move is called. However, during filling of pieces,
    only one event should call the move function. Hence, to dismiss the calling of move
    function during ButtonPress, which can be programmatically represented as
    (if button_release == False), we don't allow any code of move function to be
    executed.
    """
    return not can_move_piece() and button_release == False


def move(event, button_release):
    """
    It fills the pieces into the grid followed by moving of the pieces.
    It does the filling only when the ButtonPress corresponds to an empty(valid) location.
    After completion of filling, this function grabs the piece owned by current user during
    the ButtonPress and moves the very piece into the empty location during the ButtonRelease.
    Moving process is completed only when the valid conditions are met.

    picked_status variable stores the value 1 if a piece is successfully picked. Otherwise, zero(default).
    """
    global from_y, from_x, picked_status, current_player


    a, b = get_nearest_node(event.x, event.y)

    if bypass_release_once(button_release):
        return
    if is_invalid_drop(a, b, picked_status):
        picked_status = stop_floating_obj(from_x, from_y, current_player)
        return

    if not can_move_piece():

        if button_release:
            if is_empty(a, b):
                fill_pieces(a, b, current_player)
                if current_player == player_2:
                    if can_move_piece():
                        ((from_ai_x, from_ai_y), (to_ai_x, to_ai_y)) = Minimax(player_1.owned_position.copy(), player_2.owned_position.copy())[1]
                        move_pieces(to_ai_x, to_ai_y, from_ai_x, from_ai_y)
                        return
                    ai_x, ai_y = Minimax(player_1.owned_position.copy(), player_2.owned_position.copy())[1]
                    fill_pieces(ai_x, ai_y, current_player)

    else:

        if not button_release and not is_empty(a, b):

            from_x, from_y = get_nearest_node(event.x, event.y)
            if prevent_function(from_x, from_y, current_player):
                picked_status = 0
            else:
                picked_status = float_piece(from_x, from_y, current_player)

        elif button_release:

            a, b = get_nearest_node(event.x, event.y)
            if picked_status != 1:
                return
            if check_moving_condition(a, b, from_x, from_y):
                picked_status = move_pieces(a, b, from_x, from_y)
                if current_player == player_2:
                    ((from_ai_x, from_ai_y), (to_ai_x, to_ai_y)) = Minimax(player_1.owned_position.copy(), player_2.owned_position.copy())[1]
                    move_pieces(to_ai_x, to_ai_y, from_ai_x, from_ai_y)
            else:
                picked_status = stop_floating_obj(from_x, from_y, current_player)


def check_game():
    """
    Checks if the win condition of game is met.
    Returns true if three coordinates of current player are collinear.
    """
    global current_player
    coordinates = tuple(current_player.owned_position.values())
    if len(coordinates) != 3:
        return 0
    x1, y1 = coordinates[0][0], coordinates[0][1]
    x2, y2 = coordinates[1][0], coordinates[1][1]
    x3, y3 = coordinates[2][0], coordinates[2][1]
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)


def help_game():
    messagebox.showinfo("Help", "Welcome to the movable tic-tac-toe game. "
                                "The playing rules and win conditions are same "
                                "as that of Tic-Tac-Toe game except the limitation of number of pieces. "
                                "Each player has 3 pieces and after s/he has put all the "
                                "pieces in the board, s/he should drag the pieces. "
                                "Single click to put the piece in the board and drag to move piece from "
                                "one place to another ")


def close():
    root.destroy()


def show_result():
    print("Game won by ", current_player.color_notation)
    status['text'] = "Game Over!  " + current_player.color_notation + " won the game"
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<ButtonRelease-1>")
    user_response = messagebox.askyesno("Game Over!!! ", current_player.color_notation + " won the game. Do you want to play another game?")
    root.destroy()
    if user_response:
        ask_turn()


player_1 = Player("Sudarshan", "Blue")
player_2 = Player("Barna", "Red")
players = cycle([player_1, player_2])


def ask_turn():
    global human_turn, ai_turn, root
    root = Tk()
    root.title("Move-tac-toe")
    root.resizable(False, False)

    frame = Frame(root, width=800, height=700)
    frame.pack()
    canvas = Canvas(frame, width=800, height=700, bg="white")
    canvas.pack(side=BOTTOM)

    canvas.create_rectangle(
        0, 0,
        WINDOW_WIDTH, WINDOW_HEIGHT,
        width=int(WINDOW_WIDTH / 15),
        fill='#fff',
        outline='#bbb',
    )

    canvas.create_text(
        WINDOW_WIDTH / 2,
        4 * WINDOW_HEIGHT / 10 - 100,
        text='MOVE TAC TOE', fill='#222',
        font=('Times', int(-(WINDOW_WIDTH+30) / 12), 'bold')
    )


    canvas.create_text(
        int(WINDOW_WIDTH / 2),
        int(WINDOW_WIDTH / 2 - 80),
        text='Who plays first?', fill='#111',
        font=('Franklin Gothic', int(-1200 / 40))
    )


    ai_turn = Button(root, text="AI", padx=65, pady=30, command=lambda: new_game(0))
    ai_turn.configure(width=10, font="Times 14 bold", activebackground="#33B5E5", relief=FLAT)

    human_turn = Button(root, text="Human", padx=50, pady=30, command=lambda: new_game(1))
    human_turn.configure(width=10, font="Times 14 bold", activebackground="#33B5E5", relief=FLAT)

    canvas.create_window(460, 430, anchor=NW, window=ai_turn)
    canvas.create_window(140, 430, anchor=NW, window=human_turn)


def new_game(who_plays_first):
    global current_player, canvas, info, status, root
    player_1.remaining_piece = player_2.remaining_piece = 3
    player_1.owned_position = {}
    player_2.owned_position = {}
    root.destroy()

    root = Tk()
    root.title("Move-tac-toe")
    root.resizable(False, False)
    frame = Frame(root, width=800, height=700)
    frame.pack()
    canvas = Canvas(frame, width=620, height=600, bg="white")
    canvas.pack(side=BOTTOM)

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=close)
    menu_bar.add_cascade(label="File", menu=file_menu)
    menu_bar.add_command(label="Instructions", command=help_game)


    info = Label(root, text="", font="Times 12 bold")
    status = Label(root, text="  Turn:  " + player_1.color_notation, font="Times 12 bold", padx=0, pady=5, bd=6)
    info.pack(side=RIGHT)
    status.pack(side=LEFT, fill=X)
    canvas.delete(ALL)
    draw_grid(canvas)
    canvas.bind('<ButtonPress-1>', lambda event: move(event, False))
    canvas.bind('<ButtonRelease-1>', lambda event: move(event, True))

    toggle_turn()
    if not who_plays_first:
        toggle_turn()
        ai_x, ai_y = Minimax(player_1.owned_position.copy(), player_2.owned_position.copy())[1]
        fill_pieces(ai_x, ai_y, current_player)


ask_turn()
root.mainloop()
