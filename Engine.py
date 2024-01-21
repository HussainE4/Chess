"""
Contains Info about Chess Engines
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from Board import Board, Pawn, Queen, Rook, Knight, Bishop, King

PIECE_VALUES = {'P': 1, 'N': 3, 'B': 3.5, 'R': 5, 'Q': 9, 'K': 0}


@dataclass
class Engine2:
    """
    A Chess Engine

    """
    board: Board

    def __init__(self, board: Board,):
        self.board = board

    def select_move_try3(self, depth: int, colour: str, move, alpha, beta):
        """
        Choose a move for colour, searching 'depth' moves deep.

        """

        if depth == 0:
            return (move, self.evaluate_v1(depth, colour, move))

        legal_moves = self.board.legal_check_moves(colour)
        if len(legal_moves) == 0:
            return (move, self.evaluate_v1(depth, colour, move))

        if colour == 'W':
            maximum = - 1000
            best_moves = []
            for move_possible in legal_moves:
                self.board.make_move(move_possible[0], move_possible[1])
                x, score = self.select_move_try3(depth - 1, 'B', move_possible, alpha, beta)
                self.board.unmake_move()

                if score > maximum:
                    maximum = score
                    best_moves = [x]
                elif score == maximum:
                    best_moves.append(x)
                # alpha = max(alpha, score)
                # if beta <= alpha:
                #     break
            if move is None:
                # If we have reached the root node, choose one of the best moves
                return (random.choice(best_moves), maximum)
                # return (best_moves[0], maximum)
            else:
                # Otherwise return the move made to get to the position so far
                return (move, maximum)

        else:
            minimum = 1000
            best_moves = []
            for move_possible in legal_moves:
                self.board.make_move(move_possible[0], move_possible[1])
                x, score = self.select_move_try3(depth - 1, 'W', move_possible, alpha, beta)
                self.board.unmake_move()

                if score < minimum:
                    minimum = score
                    best_moves = [x]
                elif score == minimum:
                    best_moves.append(x)
                # beta = min(beta, score)
                # if beta <= alpha:
                #     break
            if move is None:
                # If we have reached the root node, choose one of the best moves
                return (random.choice(best_moves), minimum)
            else:
                # Otherwise return the move made to get to the position so far
                return (move, minimum)

    def evaluate_v1(self, depth, colour, move: tuple[tuple[int, int], tuple[int, int]]):
        """
        Evaluate a chess position version 1.
        """
        global PIECE_VALUES

        if depth != 0:
            # Then there are no further legal moves according to select_move_d1()
            # If black is in check, then it is Checkmate
            if self.board.king_in_check('B'):
                return 999

            if self.board.king_in_check('W'):
                return -999
            return 0

        white_points = 0
        black_points = 0
        for piece in self.board.white_pieces:

            if isinstance(piece, King) and piece.has_castled:
                white_points += 1

            if isinstance(piece, Queen):
                white_points += 9

            elif isinstance(piece, Rook):
                white_points += 5

            elif isinstance(piece, Bishop):
                white_points += 3.5

            elif isinstance(piece, Knight):
                white_points += 3
                if 2 <= piece.position[1] <= 5:
                    white_points += 0.2

            elif isinstance(piece, Pawn):
                white_points += 1
                if piece.has_moved and 2 <= piece.position[1] <= 5:
                    white_points += 0.1

        for piece in self.board.black_pieces:

            # black_points += 0.02 * piece.position[0]
            if isinstance(piece, King) and piece.has_castled:
                black_points += 1

            if isinstance(piece, Queen):
                black_points += 9

            if isinstance(piece, Rook):
                black_points += 5

            if isinstance(piece, Bishop):
                black_points += 3.5

            if isinstance(piece, Knight):
                black_points += 3
                if 2 <= piece.position[1] <= 5:
                    black_points += 0.2

            if isinstance(piece, Pawn):
                black_points += 1
                if piece.has_moved and 2 <= piece.position[1] <= 5:
                    black_points += 0.1

        return white_points - black_points


def difficulty_zero(board: Board, colour: str) -> (tuple[int, int], tuple[int, int]):
    """
    Make a random move on the given Board for the given colour and return the move made in the form
    (start_posn, end_posn)
    """

    if colour == 'W':
        # Randomly select a piece of the colour if it has at least one legal move
        piece = random.choice(board.white_pieces)
        while len(piece.legal_check_moves(board.positions)) == 0:
            piece = random.choice(board.white_pieces)
    else:
        piece = random.choice(board.black_pieces)
        while len(piece.legal_check_moves(board.positions)) == 0:
            piece = random.choice(board.black_pieces)

    move = random.choice(piece.legal_check_moves(board.positions))
    return (piece.position, move)
