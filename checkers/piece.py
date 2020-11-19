from .constants import RED, GREY, SQUARE_SIZE, CROWN
import pygame


class Piece:
    PADDING = 20
    OUTLINE = 5

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """
        Calculate the position of the piece
        :return:
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        """
        Draw the piece on the game window.
        :param win:
        :return:
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """
        Move the piece to the desired row and col
        :param row:
        :param col:
        :return:
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return f'<({self.color})({self.row}, {self.col})>'
