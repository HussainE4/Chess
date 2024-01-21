"""
Contains Info about a single game of Chess
"""

from __future__ import annotations
from dataclasses import dataclass
from Board import Board, EMPTY_BOARD, Pawn
from Engine import Engine2, difficulty_zero

import pygame_widgets
from pygame_widgets.button import Button
import pygame
import math
import os

global SCREEN
global BACKGROUND_IMAGE
global PIECES
global RED_SQUARE

# Features
# TODO Optimise Engines
# TODO En Passant


@dataclass
class Game:
    """
    A game of chess

    Instance Attributes:
        - board: The board that the game is played on
        - white_turn: A boolean value keeping track of which player's turn it is
        - is_over: A boolean value keeping track of whether the game is over (Stalemate or Checkmate)
        - computer_colour: The colour of the engine player, 'W' or 'B' or 'N' if there is no engine
        - moves: A list of the moves made up till this point in the form, (piece_notation, start_posn, end_posn)
    """

    board: Board
    white_turn: bool
    is_over: bool
    computer_colour: str
    computer_difficulty: int
    moves: list[tuple[str, tuple[int, int]]]

    def __init__(self, opponent: str, computer_colour: str, computer_difficulty):
        self.board = Board(EMPTY_BOARD)
        self.white_turn = True
        if opponent == 'C':
            self.computer_colour = computer_colour
            self.computer_difficulty = computer_difficulty

        else:
            self.computer_colour = 'N'
        self.is_over = False
        self.moves = []

    def play_game(self):
        """
        Play a single game of chess
        """
        # Setup variables, assets and pygame
        global SCREEN
        global BACKGROUND_IMAGE
        global PIECES
        global RED_SQUARE

        pygame.init()
        pygame.font.init()
        SCREEN = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Chess")
        FPS = 60

        RED_SQUARE = pygame.image.load(os.path.join("Assets", "red_square.png"))
        grey_dot = pygame.image.load(os.path.join("Assets", "grey_dot.svg.png"))
        BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "Chessboard480.svg.png")).convert()
        PIECES = {'BP': pygame.image.load(os.path.join('Assets', 'b_pawn.png')).convert_alpha(),
                  'BN': pygame.image.load(os.path.join('Assets', 'b_knight.png')).convert_alpha(),
                  'BB': pygame.image.load(os.path.join('Assets', 'b_bishop.png')).convert_alpha(),
                  'BR': pygame.image.load(os.path.join('Assets', 'b_rook.png')).convert_alpha(),
                  'BQ': pygame.image.load(os.path.join('Assets', 'b_queen.png')).convert_alpha(),
                  'BK': pygame.image.load(os.path.join('Assets', 'b_king.png')).convert_alpha(),
                  'WP': pygame.image.load(os.path.join('Assets', 'w_pawn.png')).convert_alpha(),
                  'WN': pygame.image.load(os.path.join('Assets', 'w_knight.png')).convert_alpha(),
                  'WB': pygame.image.load(os.path.join('Assets', 'w_bishop.png')).convert_alpha(),
                  'WR': pygame.image.load(os.path.join('Assets', 'w_rook.png')).convert_alpha(),
                  'WQ': pygame.image.load(os.path.join('Assets', 'w_queen.png')).convert_alpha(),
                  'WK': pygame.image.load(os.path.join('Assets', 'w_king.png')).convert_alpha(),
                  }
        piece_to_move = "potato"
        moving = False
        pos = None
        board_posn = None
        rect = None
        self.draw_board(pos, board_posn, rect)

        end = False
        while not self.is_over and not end:

            clock = pygame.time.Clock()
            # Event handling
            for event in pygame.event.get():
                clock.tick(FPS)

                if event.type == pygame.QUIT:
                    # If quit, end the game
                    end = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the Mouse Button is held, get whatever is at the selected square

                    # self.draw_board(pos, board_posn, rect)
                    pos = pygame.mouse.get_pos()
                    if self.computer_colour == 'W':
                        board_posn = (pos[1] // 100, 7 - pos[0] // 100)
                    else:
                        board_posn = (7 - pos[1] // 100, pos[0] // 100)

                    if 0 <= board_posn[0] <= 7 and 0 <= board_posn[1] <= 7:
                        piece_to_move = self.board.positions[board_posn[0]][board_posn[1]]
                        if piece_to_move and ((self.white_turn and piece_to_move.colour == 'W') or
                                                          (not self.white_turn and piece_to_move.colour == 'B')):

                            # If the square is not empty and correct colour, make it capable of being moved
                            rect = pygame.Rect(math.floor(pos[0]), math.floor(pos[1]), 100, 100)
                            if rect.collidepoint(event.pos):
                                moving = True

                            # Draw all the legal moves that can be made
                            for move in piece_to_move.legal_check_moves(self.board.positions):
                                move = move[1]
                                if self.computer_colour == 'W':
                                    draw_posn = (700 - move[1] * 100 + 37, (move[0]) * 100 + 37)
                                else:
                                    draw_posn = (move[1] * 100 + 37, (7 - move[0]) * 100 + 37)
                                SCREEN.blit(grey_dot, (draw_posn[0], draw_posn[1]))
                            pygame.display.flip()
                        else:
                            pos = None

                    else:
                        pos = None

                elif event.type == pygame.MOUSEBUTTONUP:
                    # If mouse button is released, stop moving
                    moving = False

                    # If we have selected a valid piece before this, get position where the piece was released
                    if pos:
                        end_pos = pygame.mouse.get_pos()
                        if self.computer_colour == 'W':
                            end_board_posn = (end_pos[1] // 100, 7 - end_pos[0] // 100)
                        else:
                            end_board_posn = (7 - end_pos[1] // 100, end_pos[0] // 100)

                        # If the end position is a legal move, make the move
                        if (board_posn, end_board_posn) in piece_to_move.legal_check_moves(self.board.positions):
                            self.make_move(board_posn, end_board_posn, pos, rect)

                        else:
                            # If target was not a legal move, redraw board based on last position
                            pos = None
                            self.draw_board(pos, board_posn, rect)

                elif moving and event.type == pygame.MOUSEMOTION:
                    # Redraw the board showing the piece being moved
                    rect.move_ip(event.rel)
                    self.draw_board(pos, board_posn, rect)

                # Engine's Turn
                if not self.is_over and self.computer_turn():
                    if self.computer_difficulty == 0:
                        move = difficulty_zero(self.board, self.computer_colour)
                        self.make_move(move[0][0], move[0][1], pos, rect)

                    else:
                        engine = Engine2(self.board)
                        move = engine.select_move_try3(self.computer_difficulty, self.computer_colour, None, -999, 999)
                        # engine = Engine(None, self.board, self.computer_difficulty, self.computer_colour)
                        # move = engine.select_move_d1(-999, 999)

                        self.make_move(move[0][0], move[0][1], pos, rect)


        # At the end of the game, write down all the moves made
        # for i in range(0, len(self.moves) - 1, 2):
        #     white_move, black_move = self.moves[i], self.moves[i + 1]
        #     white_posn, black_posn = position_to_coordinate(white_move[1]), position_to_coordinate(black_move[1])
        #     font = pygame.font.Font("Assets/Arial.ttf", 30)
        #
        #     white_text, black_text = '', ''
        #     if white_move[0] != 'P':
        #         white_text = white_move[0]
        #     white_text += white_posn
        #     if black_move[0] != 'P':
        #         black_text = black_move[0]
        #     black_text += black_posn
        #
        #     message = font.render('(' + white_text + ', ' + black_text + ')', True, (0, 0, 0))
        #     message_rect = message.get_rect()
        #
        #     if i % 4 == 0:
        #         rect_x, rect_y = 900, 40 + 10 * i
        #     else:
        #         rect_x, rect_y = 1100, 40 + 10 * (i - 2)
        #     if rect_y >= 380:
        #         rect_y += 40
        #
        #     message_rect.center = (rect_x, rect_y)
        #     screen.blit(message, message_rect)
        #     pygame.display.flip()

        # Keep board in final state until mouse is pressed
        end_button = Button(SCREEN, 900, 450, 200, 100, text="Continue")
        while not end:

            events = pygame.event.get()
            for event in events:
                pygame_widgets.update(events)
                pygame.display.update()
                if event.type == pygame.QUIT or end_button.clicked:
                    end = True

    def make_move(self, board_posn: tuple[int, int], end_board_posn: tuple[int, int], pos, rect):
        """
        Move the piece_to_move with position board_posn to end_board_posn
        """
        piece = self.board.positions[board_posn[0]][board_posn[1]]
        self.board.make_move(board_posn, end_board_posn)
        self.moves.append((piece.notation[1], end_board_posn))

        # Deal with promotions
        if isinstance(piece, Pawn) and ((piece.colour == 'W' and end_board_posn[0] == 7) or
                                        (piece.colour == 'B' and end_board_posn[0] == 0)):

            new_piece = self.draw_promotion(piece.colour)
            self.board.promote_pawn(piece, new_piece)

        # Alternate Turns
        self.white_turn = not self.white_turn
        self.draw_board(pos, board_posn, rect)
        # pos = None

        # Stalemate / Checkmate
        if self.white_turn and len(self.board.legal_check_moves('W')) == 0:
            # It is now White's turn, and they cannot make any legal moves

            if self.board.king_in_check('W'):
                self.display_message('Black Wins')
            else:
                self.display_message('Stalemate')
            self.is_over = True

        elif not self.white_turn and self.board.legal_check_moves('B') == set():
            # It is now Black's turn and they cannot make any legal moves

            if self.board.king_in_check('B'):
                self.display_message('White Wins')
            else:
                self.display_message('Stalemate')
            self.is_over = True

        elif self.white_turn and self.board.king_in_check('W'):
            self.display_message('White is in Check')
            self.draw_red_squares('W')

        elif not self.white_turn and self.board.king_in_check('B'):
            self.display_message('Black is in Check')
            self.draw_red_squares('B')

        else:
            # If no other messages are displayed, display which player's turn it is
            if self.white_turn:
                self.display_message("White's Turn")
            else:
                self.display_message("Black's Turn")

    def draw_board(self, pos, board_posn, rect):
        """
        Draw a chess board and all pieces
        """

        SCREEN.fill((255, 255, 255))
        SCREEN.blit(BACKGROUND_IMAGE, [0, 0])
        pieces_list = self.board.white_pieces + self.board.black_pieces

        for piece in pieces_list:
            # Go through each piece

            if pos is not None and board_posn == piece.position:
                # If we have selected this piece, then draw its movement
                SCREEN.blit(PIECES[piece.notation], rect)

            else:
                # Draw pieces in current position if they are not being moved
                if self.computer_colour == 'W':
                    # If playing against a White Computer, flip the board
                    SCREEN.blit(PIECES[piece.notation],
                                ((7 - piece.position[1]) * 100, (piece.position[0]) * 100))
                else:
                    SCREEN.blit(PIECES[piece.notation],
                                (piece.position[1] * 100, (7 - piece.position[0]) * 100))

        pygame.display.flip()

    def draw_red_squares(self, colour: str):
        """
        Draw red square around the king of the given colour when it is in check
        """
        king_location = self.board.get_king_location(colour)

        if self.computer_colour == 'W':
            SCREEN.blit(RED_SQUARE, (700 - king_location[1] * 100, (king_location[0]) * 100))
        else:
            SCREEN.blit(RED_SQUARE, (king_location[1] * 100, (7 - king_location[0]) * 100))

        pygame.display.flip()

    def display_message(self, text: str):
        """
        Print the given text message onto the screen
        """
        font = pygame.font.Font("Assets/Arial.ttf", 50)
        message = font.render(text, True, (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (1000, 400)
        SCREEN.blit(message, message_rect)
        pygame.display.flip()

    def draw_promotion(self, colour: str):
        """
        Draw a promotion window and return the piece promoted to
        """
        pygame.display.set_caption("Select a piece to promote the pawn to")
        pieces_possible = ['Q', 'R', 'N', 'B']
        if self.computer_colour == colour:
            return 'Q'
        for i in range(4):
            if colour == 'W':
                SCREEN.blit(PIECES[colour + pieces_possible[i]], (800 + 100 * i, 0))
            else:
                SCREEN.blit(PIECES[colour + pieces_possible[i]], (800 + 100 * i, 700))

        pygame.display.flip()

        # game loop
        running = True
        while running:

            # for loop through the event queue
            for event in pygame.event.get():

                # Check for QUIT event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if colour == 'W':
                        return pieces_possible[(pos[0] // 100) - 8]
                    else:
                        return pieces_possible[(pos[0] // 100) - 8]

    def computer_turn(self) -> bool:
        """
        Returns whether or not it is the computer's turn to make a move
        """
        return (self.computer_colour == 'W' and self.white_turn) or (self.computer_colour == 'B' and not self.white_turn)
