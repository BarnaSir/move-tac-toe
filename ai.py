#!/usr/bin/env python3
import platform

import numpy as np

from utils import merge_two_dicts

INF = np.inf

VALID_MOVES = {
    0: (1, 3, 4), 1: (0, 2, 4), 2: (1, 4, 5),
    3: (0, 4, 6), 4: (0, 1, 2, 3, 5, 6, 7, 8), 5: (4, 2, 8),
    6: (4, 3, 7), 7: (4, 6, 8), 8: (4, 5, 7),
}

ALL_POSITIONS = {
    (50, 50), (300, 50), (550, 50),
    (50, 300), (300, 300), (550, 300),
    (50, 550), (300, 550), (550, 550),
}

POSITIONS_TO_INDEX = {
    (50, 50): 0, (300, 50): 1, (550, 50): 2,
    (50, 300): 3, (300, 300): 4, (550, 300): 5,
    (50, 550): 6, (300, 550): 7, (550, 550): 8,
}

INDEX_TO_POSITIONS = dict((j, i) for i, j in POSITIONS_TO_INDEX.items())

best_move = None
DEPTH = 7


def is_game_over(player_1_board, player_2_board):
    """
    Determines if the game is over.
    :param player_1_board: containing board information of player_1
    :param player_2_board: containing board information of player_2
    :return: Tuple of length two.  First value represents if the game is over(i.e True or False)
             Second value returns 1 if player_1 wins, 2 if player_2 wins and None if no one wins.
    """

    # Check conditions only if the player whose condition is being checked has 3 pieces in the board.

    # The condition is the collinearity of the points satisfied through same slope.

    if len(player_1_board) == 3:
        values_tuple = tuple(player_1_board.values())
        x1, y1 = values_tuple[0][0], values_tuple[0][1]
        x2, y2 = values_tuple[1][0], values_tuple[1][1]
        x3, y3 = values_tuple[2][0], values_tuple[2][1]

        if (x1 - x2) * (y2 - y3) == (x2 - x3) * (y1 - y2):
            return True, 1

    if len(player_2_board) == 3:
        values_tuple = tuple(player_2_board.values())
        x1, y1 = values_tuple[0][0], values_tuple[0][1]
        x2, y2 = values_tuple[1][0], values_tuple[1][1]
        x3, y3 = values_tuple[2][0], values_tuple[2][1]

        if (x1 - x2) * (y2 - y3) == (x2 - x3) * (y1 - y2):
            return True, 2

    return False, None


def get_possible_drags(player_1_board, player_2_board, player):
    """
    Returns the set of possible drags given the board state and current player.
    Parameter player can be either 1 or 2 of int dtype.

    A possible drag has a tuple having two tuples.  First tuple is from-position and second tuple is to-position.
    """
    possible_drags = set()

    # set current_player_board according to the player parameter
    if player == 1:
        current_player_board = player_1_board
    else:
        current_player_board = player_2_board

    for i in current_player_board.values():
        for j in VALID_MOVES[POSITIONS_TO_INDEX[i]]:

            if INDEX_TO_POSITIONS[j] not in merge_two_dicts(player_1_board, player_2_board).values():
                possible_drags.add((i, INDEX_TO_POSITIONS[j]))
    return possible_drags

def Minimax(player_1_board, player_2_board, depth=7, alpha=-INF, beta=INF, maximizingPlayer=True):
    """
    Minimax algorithm with alpha-beta pruning.
    :param player_1_board: containing board information of player_1
    :param player_2_board: containing board information of player_2
    :param depth: the depth of the algorithm.
    :param alpha: alpha of alpha-beta pruning
    :param beta: beta of alpha-beta pruning
    :param maximizingPlayer: if the player is maximizing player or minimizing player
    :return: tuple of length two, first giving the value of the state and second giving the steps to take
    """

    # setting best_move and DEPTH global so that the best_move
    # is retained and DEPTH is compared with initial depth=<int>
    global best_move, DEPTH

    if depth == 0 or is_game_over(player_1_board, player_2_board)[0]:
        if is_game_over(player_1_board, player_2_board)[0]:
            if is_game_over(player_1_board, player_2_board)[1] == 2:
                return 1000+depth, None
            else:
                return -1000-depth, None
        else:
            return 0, None

    if maximizingPlayer:
        value = -INF

        # For just putting the pieces
        if len(player_2_board) < 3:

            possible_moves = ALL_POSITIONS - set(player_1_board.values()) - set(player_2_board.values())

            max_key = max([8] + list(player_1_board.keys()) + list(player_2_board.keys()))

            for i in possible_moves:

                # playing the move
                player_2_board[max_key+1] = i

                # calculating the score
                value_t = Minimax(player_1_board, player_2_board, depth-1, alpha, beta, False)[0]

                # comparing and setting value and best move
                if value_t > value:
                    value = value_t

                    if alpha > value:
                        alpha = value

                    # best move is set if the node is at the root
                    if depth == DEPTH:
                        best_move = i

                # reverting the move
                player_2_board.pop(max_key+1, None)

                # alpha-beta pruning
                if alpha >= beta:
                    break

            return value, best_move

        # For dragging the pieces
        else:

            # creating set of possible drags
            possible_drags = get_possible_drags(player_1_board, player_2_board, 2)

            # looping through all possible drags
            for i in possible_drags:

                # playing the drag
                dict_temp = dict((j, i) for i, j in player_2_board.items())
                dict_temp.pop(i[0], None)
                player_2_board = dict((j, i) for i, j in dict_temp.items())
                max_key = max([8] + list(player_1_board.keys()) + list(player_2_board.keys()))
                player_2_board[max_key+1] = i[1]

                # calculating the value of the state
                value_t = Minimax(player_1_board, player_2_board, depth-1, alpha, beta, False)[0]

                # comparing the values and setting values and best_move
                if value_t > value:
                    value = value_t
                    if depth == DEPTH:
                        best_move = i

                    if value > alpha:
                        alpha = value

                # reverting the drag
                player_2_board.pop(max_key+1, None)
                player_2_board[max_key+1] = i[0]

                # alpha-beta pruning
                if alpha >= beta:
                    break

            return value, best_move

    else:
        value = INF

        # For just putting the pieces
        if len(player_1_board) < 3:

            # creating the possible put pieces moves
            possible_moves = ALL_POSITIONS - set(player_1_board.values()) - set(player_2_board.values())
            max_key = max([8] + list(player_2_board.keys()) + list(player_1_board.keys()))

            # looping through all possible moves
            for i in possible_moves:

                # playing the move
                player_1_board[max_key + 1] = i

                # calculating the state of the board
                value_t = Minimax(player_1_board, player_2_board, depth-1, alpha, beta, True)[0]

                # comparing and setting the best_move
                if value_t < value:
                    value = value_t
                    if depth == DEPTH:
                        best_move = i

                    if value < beta:
                        beta = value

                # reverting the move
                player_1_board.pop(max_key + 1, None)

                # alpha-beta pruning
                if alpha >= beta:
                    break

            return value, best_move

        # For dragging the pieces
        else:

            # creating the possible drags
            possible_drags = get_possible_drags(player_1_board, player_2_board, 1)

            # looping through all the possible drags
            for i in possible_drags:

                # playing the drag
                dict_temp = dict((j, i) for i, j in player_1_board.items())
                dict_temp.pop(i[0], None)
                player_1_board = dict((j, i) for i, j in dict_temp.items())
                max_key = max([8] + list(player_1_board.keys()) + list(player_2_board.keys()))
                player_1_board[max_key+1] = i[1]

                # calculating the state of the game using the minimax algorithm
                value_t = Minimax(player_1_board, player_2_board, depth-1, alpha, beta, True)[0]

                # comparing the value with value_t and setting the best_move and value
                if value_t < value:
                    value = value_t
                    if depth == DEPTH:
                        best_move = i

                    if value < beta:
                        beta = value

                # reverting the move
                player_1_board.pop(max_key + 1, None)
                player_1_board[max_key + 1] = i[0]

                # alpha-beta pruning
                if alpha >= beta:
                    break

            return value, best_move