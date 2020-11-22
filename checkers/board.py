import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece
import random
from minimax import optimizer


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.threaten_reds = self.threaten_whites = 0

        '''weights for optimizing the evaluate function'''
        self.bias = random.gauss(0, 1)
        self.weight_red = random.gauss(0, 1)
        self.weight_white = random.gauss(0, 1)
        self.weight_white_king = random.gauss(0, 1)
        self.weight_red_king = random.gauss(0, 1)
        self.weight_threaten_red = random.gauss(0, 1)
        self.weight_threaten_white = random.gauss(0, 1)

        self.weights = [self.bias, self.weight_red, self.weight_white, self.weight_red_king, self.weight_white_king,
                self.weight_threaten_red, self.weight_threaten_white]

        self.features = [1, self.red_left, self.white_left, self.red_kings, self.white_kings, self.threaten_reds,
                self.threaten_whites]

        self.create_board()

    def draw_squares(self, win):
        """
        Draw squares in the game window.
        :param win:
        :return:
        """
        win.fill(BLACK)

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        """
        Evaluation function for AI player!
        :return:
        """
        # return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
        return self.bias + (self.weight_red * self.red_left) + (self.weight_white * self.white_left) + (
                self.weight_red_king * self.red_kings) + (self.weight_white_king * self.white_kings) + (
                       self.weight_threaten_red * self.threaten_reds) + (
                       self.weight_threaten_white * self.threaten_whites)

    def get_all_pieces(self, color):
        """Return all pieces"""
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        """Move the piece to the new row and column and check the king condition."""
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        """
        Return the piece in the specific row and column
        :param row:
        :param col:
        :return:
        """
        return self.board[row][col]

    def create_board(self):
        """Create the board and placed the pieces on it. row by row"""
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        """Draw all pieces on the board Game!"""
        self.draw_squares(win)
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
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:  # if we found empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:  # if we found empty square
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves

    def calculate_threatens(self):
        self.threaten_reds = 0
        self.threaten_whites = 0
        red_skips = []
        white_skips = []

        colors = [RED, WHITE]
        for color in colors:
            for piece in self.get_all_pieces(color):
                valid_moves = self.get_valid_moves(piece)
                for move, skip in valid_moves.items():
                    if color == RED:
                        white_skips += skip
                    elif color == WHITE:
                        red_skips += skip

        self.threaten_whites = len(set(white_skips))
        self.threaten_reds = len(set(red_skips))

    def optimize_weights(self, loss, lr):
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + lr * self.features[i] * loss

    def apply_weights(self, weights):
        for i in range(len(self.weights)):
            self.weights[i] = weights[i]


