import pygame
import argparse
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax import minimax, criterion

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
FPS = 60


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main(opt):
    if opt.game_mode == 'person2person':
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

        while run:
            clock.tick(FPS)

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
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

        while run:
            clock.tick(FPS)
            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(), opt.minimax_depth, WHITE, game)
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
        run = True
        clock = pygame.time.Clock()
        game = Game(WIN)

        while run:
            clock.tick(FPS)

            if game.winner() is not None:
                print("The winner is: ", game.winner())
                run = False

            if game.turn == WHITE:
                value, new_board = minimax(game.get_board(), opt.minimax_depth, WHITE, game)
                game.ai_move(new_board)
            elif game.turn == RED:
                value, new_board = minimax(game.get_board(), opt.minimax_depth, False, game)
                game.ai_move(new_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # pygame.time.delay(1000)
            game.update()

    elif opt.game_mode == 'person2ai_ml':
        pass
    elif opt.game_mode == 'ai2ai_ml':
        weights = None

        for epoch in range(opt.epochs):
            run = True
            clock = pygame.time.Clock()
            game = Game(WIN)
            red = white = False
            if weights is not None:
                game.board.apply_weights(weights)

            iter = 0
            while iter < 100 and run:
                clock.tick(FPS)

                if game.turn == WHITE:
                    white_value, new_board = minimax(game.get_board(), opt.minimax_depth, True, game)
                    situation = game.ai_move(new_board)
                    if situation: # if we can't move any further
                        print('Can\'t move any further')
                        break
                    white = True
                elif game.turn == RED:
                    red_value, new_board = minimax(game.get_board(), opt.minimax_depth, False, game)
                    situation = game.ai_move(new_board)
                    if situation:
                        print('Can\'t move any further')
                        break
                    red = True

                if red and white:
                    loss = criterion(white_value, red_value)
                    game.board.optimize_weights(loss, 0.1)
                    red = white = False
                    print(loss)
                    if game.winner() is not None:
                        if game.winner() == WHITE:
                            loss = criterion(24, white_value)
                            game.board.optimize_weights(loss, 0.1)
                            print('White is the winner and the loss is : ', loss)
                            weights = game.board.weights
                            break

                        elif game.winner() == RED:
                            loss = criterion(-24, red_value)
                            game.board.optimize_weights(loss, 0.1)
                            print('Red is the winner and the loss is : ', loss)
                            weights = game.board.weights
                            break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                game.update()
                iter += 1

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

    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--lr', type=float, default=0.1)

    opt = parser.parse_args()
    main(opt)
