import pygame
import argparse
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax_white, minimax_red


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
FPS = 60


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main(opt):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if opt.game_mode == 'person2person':
            if game.winner() is not None:
                print(game.winner())
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)
            game.update()

        elif opt.game_mode == 'person2ai':
            if game.turn == WHITE:
                value, new_board = minimax_white(game.get_board(), opt.minimax_depth, WHITE, game)
                game.ai_move(new_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)
            game.update()

        elif opt.game_mode == 'ai2ai':
            if game.turn == WHITE:
                value, new_board = minimax_white(game.get_board(), opt.minimax_depth, WHITE, game)
                game.ai_move(new_board)

            pygame.time.delay(1000)
            game.update()
            if game.turn == RED:
                value, new_board = minimax_red(game.get_board(), opt.minimax_depth, RED, game)
                game.ai_move(new_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.time.delay(1000)
            game.update()

        elif opt.game_mode == 'person2ai_ml':
            pass
        elif opt.game_mode == 'ai2ai_ml':
            pass

        # pygame.time.delay(1000)
        # game.update()

        # if game.turn == RED:
        #     value, new_board = minimax_red(game.get_board(), 3, RED, game)
        #     game.ai_move(new_board)

        # value, new_board = minimax(game.get_board(), 3, game.turn, game)
        # game.ai_move(new_board)
        # pygame.time.delay(1000)
        # game.update()
    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game_mode', type=str, default='person2person',
                        choices=['person2person', 'person2ai', 'ai2ai', 'person2ai_ml', 'ai2ai_ml'],
                        help='person2person: play 2 persons together\n'
                             'person2ai: play person with ai player\n'
                             'ai2ai: play 2 ai players together\n'
                             'person2ai_ml: play a person with ai player to train'
                             ' its evaluation function for better ai moves\n'
                             'ai2ai_ml: play 2 ai players together to train their evaluation functions for '
                             'better ai moves')
    parser.add_argument('--minimax_depth', type=int, default=3,
                        help='minimax tree depth')

    opt = parser.parse_args()
    main(opt)
