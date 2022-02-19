from copy import deepcopy
import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .pieces import Piece

class Board:
    	
    def __init__(self):
        self.board = []
        self.redLeft = self.whiteLeft = 12
        self.redKings = self.whiteKings = 0
        self.createBoard()
    
    def drawSquares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.whiteLeft - self.redLeft + (self.whiteKings - self.redKings)

    def getAllPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.makeKing()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.redKings += 1 

    def getPiece(self, row, col):
        return self.board[row][col]

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.drawSquares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.redLeft -= 1
                else:
                    self.whiteLeft -= 1
    
    def winner(self):
        if self.redLeft <= 0:
            return WHITE
        elif self.whiteLeft <= 0:
            return RED
        
        return None 
    


    def getValidMoves(self, piece):

        moves = {}
        if piece.king or piece.color == RED:
            # stop = max(piece.row-3, -1)
            moves.update(self._traverseLeft(piece.row, piece.col, -1, piece, []))
            moves.update(self._traverseRight(piece.row, piece.col, -1, piece, []))
        if piece.king or piece.color == WHITE:
            # stop = min(piece.row+3, ROWS)
            moves.update(self._traverseLeft(piece.row, piece.col, 1, piece, []))
            moves.update(self._traverseRight(piece.row, piece.col, 1, piece, []))

        return moves

    def _traverseLeft(self, row, column, step, piece, skipped=[]):
        moves = {}
        last = []
        
        next_row, next_col = (row+step, column - 1)
        if  0 <= next_row < ROWS and next_col >= 0:
            step1 = self.board[next_row][next_col]
            if step1 == 0:
                if not skipped:
                    moves[((piece.row, piece.col), (next_row, next_col))] = skipped 
            elif step1.color != piece.color:
                next_row, next_col = (next_row+step, next_col - 1)
                if  0 <= next_row < ROWS and next_col >= 0:
                    skipped.append(step1)
                    step2 = self.board[next_row][next_col]
                    if step2 == 0:
                        moves[((piece.row, piece.col), (next_row, next_col))] = skipped
                        if len(skipped) < 2:
                            moves.update(self._traverseLeft(next_row, next_col, step, piece, list(skipped)))
                            moves.update(self._traverseRight(next_row, next_col, step, piece, list(skipped)))


        return moves
    
    def _traverseRight(self, row, column, step, piece, skipped=[]):
        moves = {}
        last = []


        next_row, next_col = (row+step, column + 1)
        if  0 <= next_row < ROWS and next_col < COLS:

            step1 = self.board[next_row][next_col]
            if step1 == 0:
                if not skipped:
                    moves[((piece.row, piece.col), (next_row, next_col))] = skipped 
            elif step1.color != piece.color:
                next_row, next_col = (next_row+step, next_col + 1)
                if  0 <= next_row < ROWS and next_col < COLS:
                    skipped.append(step1)
                    step2 = self.board[next_row][next_col]
                    if step2 == 0:
                        moves[((piece.row, piece.col), (next_row, next_col))] = skipped
                        if len(skipped) < 2:
                            moves.update(self._traverseLeft(next_row, next_col, step, piece, list(skipped)))
                            moves.update(self._traverseRight(next_row, next_col, step, piece, list(skipped)))
        return moves

   