"""
Contains Info about Chess Pieces
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Piece:
    """
    A parent class for a piece

    Instance Atrributes:
        - position: The current position of the piece as a tuple representing the coordinates of the square
        - colour: The colour (W or B) of the piece
        - notation: The piece's colour, followed by its notation (K, Q, R, N, B, P)
        - possible_moves: The possible moves that can be made by the piece


    Representation Invariants:
        - colour == 'W' or colour == 'B'
    """
    position: tuple[int, int]
    colour: str
    notation: str
    possible_moves: list[tuple[int, int]]

    def __init__(self, colour, position):
        """
        Create a piece with colour and place it on position
        """
        self.colour = colour
        self.position = position

    def get_legal_moves(self, board: list[list[Optional[Piece]]]) -> list[tuple[int, int]]:
        """
        Return a list of all the positions that the piece is looking at
        """
        legal_moves = []
        rank, file = self.position
        i = 0

        while i < len(self.possible_moves):

            move = self.possible_moves[i]
            # Legal move if move is within board boundaries and no piece on the square
            if 0 <= move[0] + rank <= 7 and 0 <= move[1] + file <= 7 and board[move[0] + rank][move[1] + file] is None:
                legal_moves.append((move[0] + rank, move[1] + file))
                i += 1
            else:
                # The piece can no longer move in the same direction
                if 0 <= move[0] + rank <= 7 and 0 <= move[1] + file <= 7 and\
                        board[move[0] + rank][move[1] + file].colour != self.colour:
                    # It is a capture if within board and piece of opposite colour on the square.
                    legal_moves.append((move[0] + rank, move[1] + file))

                i = 7 * (1 + i // 7)

        return legal_moves

    def legal_check_moves(self, board: list[list[[Piece]]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Return a list of all the positions, considering checks, that the piece can legally move to
        """
        moves = []
        position = self.position

        for move in self.get_legal_moves(board):
            rank, file = position

            # For each position the piece is looking at, create a copy board in which the potential move is made
            copy_positions = [row[:] for row in board]
            copy_positions[move[0]][move[1]], copy_positions[rank][file] = self, None
            self.position = move
            copy_board = Board.Board(copy_positions)

            # If making that move would not put the king in check, it is a legal move
            if not copy_board.king_in_check(self.colour):
                moves.append((position, move))

            # Reset the piece's position
            self.position = position

        return moves

    def make_move(self, target: tuple[int, int]):
        """
        Move a piece to the destination.

        Precondition:
            - target in self.legal_check_moves(board)
        """
        # legal_moves = self.get_legal_moves(board)
        # If move is legal, update piece's position

        # Original Template
        # if target in legal_moves:
        #     self.position = target
        #     return True
        # return False

        # Checks V1
        # if target in legal_moves:
        #     rank, file = self.position
        #     copy_positions = [row[:] for row in board]
        #     copy_positions[target[0]][target[1]] = self
        #     copy_positions[rank][file] = None
        #     self.position = target
        #     copy_board = Board.Board(copy_positions)
        #     return not copy_board.king_in_check(self.colour)

        # Checks V2
        self.position = target


import Board
