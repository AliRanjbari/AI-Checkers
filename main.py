import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.minimax import minimax
import time

FPS = 60

WHITE_DEPTH = 3
RED_DEPTH = 1

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def getRowColFromMouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

if __name__ == '__main__':
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game.update()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, newBoard = minimax(game.getBoard(), WHITE_DEPTH, True)
            game.aiMove(newBoard)

        else:
            value, newBoard = minimax(game.getBoard(), RED_DEPTH, False)
            game.aiMove(newBoard)


        if game.winner() != None:
            run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.update()
    
    pygame.quit()