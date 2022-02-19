from copy import deepcopy
from typing import NewType
from numpy import inf
import random
import pygame
from checkers.game import Game

RED = (255,0,0)
WHITE = (255,255,255)

# def minimax(position, depth, maxPlayer):
#     new_board = deepcopy(position) 
#     if maxPlayer:
#         color = WHITE
#     else:
#         color = RED

#     actions = getAllMoves(position, color)
#     # print(f"moves_size: {len(actions)}")
#     for i, v in enumerate(actions):
#         print(f"{i}: {v}")
#     choice = input()
#     # action = random.choice(list(actions.items()))
#     action = list(actions.items())[int(choice)]

#     return (1, simulateMove(action, position))



def minimax(position, depth, maxPlayer):
    if position.winner():
        if position.winner() == WHITE:
            return (18, position) # 18 is the maximum evaluation output 
        return (-18, position)
    if depth == 0:
        return (position.evaluate(), position)
    if maxPlayer:
        v = -inf
        max_position = position
        for a in getAllMoves(position, WHITE).items():
            board = simulateMove(a, position)
            e, new_position = minimax(board, depth-1, False)
            if max(v, e) == e:
                v = e
                max_position = board
        return (v, max_position)

    else:
        v = inf
        min_position = position
        for a in getAllMoves(position, RED).items():
            board = simulateMove(a, position)
            e, new_position = minimax(board, depth-1, True)
            if min(v, e) == e:
                v = e
                min_position = board
        return (v, min_position)
    



def simulateMove(action, board):
    new_board = deepcopy(board) 
    move, skipped = action
    piece = new_board.board[move[0][0]][move[0][1]]


    new_board.move(piece, move[1][0], move[1][1])
    new_board.remove(skipped)

    return new_board

def getAllMoves(board, color):
    moves = {}
    for p in board.getAllPieces(color):
        moves.update(board.getValidMoves(p))
    return moves