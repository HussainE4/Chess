"""
Contains Info about KIngs
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
from Chess_Pieces.Pieces import Piece
from Chess_Pieces.Rook import Rook


@dataclass
class King(Piece):
    """
    A Class representing a King
    """
    has_moved: bool
    has_castled: bool
    first_move: tuple[int, int]

    def __init__(self, colour, position):
        super().__init__(colour, position)
        self.notation = self.colour + 'K'
        self.possible_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.has_moved = False
        self.first_move = tuple()
        self.has_castled = False

    def get_legal_moves(self, board: list[list[Optional[Piece]]]) -> list[tuple]:
        """
        Get the legal moves that can be made by the piece
        """
        legal_moves = []
        rank, file = self.position
        for move in self.possible_moves:
            # Legal move if move is within board boundaries and no piece of the same colour on the square
            if 0 <= move[0] + rank <= 7 and 0 <= move[1] + file <= 7 \
                    and (board[move[0] + rank][move[1] + file] is None
                         or board[move[0] + rank][move[1] + file].colour != self.colour):
                legal_moves.append((move[0] + rank, move[1] + file))
        return legal_moves

    def legal_check_moves(self, board: list[list[[Piece]]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Return a list of all the positions, considering checks, that the piece can legally move to. Also considers
        castling
        """
        legal_moves = super().legal_check_moves(board)
        legal_moves.extend((self.can_castle(Board.Board(board))))
        return legal_moves

    def make_move(self, destination: tuple[int, int]):
        """
        Move the King to the specified square. Update the has_moved attribute
        """
        if not self.has_moved:
            self.has_moved = True
            self.first_move = destination
        self.position = destination

    def can_castle(self, board: Board.Board):
        """
        Returns the legal castling moves that can be made, if any
        """
        legal_castle_moves = []
        if not self.has_moved and not board.king_in_check(self.colour):
            # White king
            if self.colour == 'W':
                # Get the two rooks
                queen_rook, king_rook = board.positions[0][0], board.positions[0][7]
                black_legal_moves = board.all_legal_moves('B')

                # If the Queen rook has not moved and no pieces in between them
                if isinstance(queen_rook, Rook) and not queen_rook.has_moved and queen_rook.colour == self.colour:

                    if all(board.positions[0][i] is None for i in range(1, 4)):
                        # If no enemy pieces are blocking the castle
                        if (0, 2) not in black_legal_moves and (0, 3) not in black_legal_moves:
                            legal_castle_moves.append((self.position, (0, 2)))
                            # Can Castle Queenside

                # Kingside Castling
                if isinstance(king_rook, Rook) and not king_rook.has_moved:
                    if all(board.positions[0][i] is None for i in range(5, 7)):

                        if (0, 5) not in black_legal_moves and (0, 6) not in black_legal_moves:
                            legal_castle_moves.append((self.position, (0, 6)))
                            # Can Castle Kingside
            else:
                queen_rook, king_rook = board.positions[7][0], board.positions[7][7]
                white_legal_moves = board.all_legal_moves('W')
                if isinstance(queen_rook, Rook) and not queen_rook.has_moved:
                    if all(board.positions[7][i] is None for i in range(1, 4)):

                        if (7, 2) not in white_legal_moves and (7, 3) not in white_legal_moves:
                            legal_castle_moves.append((self.position, (7, 2)))
                            # Can Castle Queenside
                if isinstance(king_rook, Rook) and not king_rook.has_moved:
                    if all(board.positions[7][i] is None for i in range(5, 7)):

                        if (7, 5) not in white_legal_moves and (7, 6) not in white_legal_moves:
                            legal_castle_moves.append((self.position, (7, 6)))
                            # Can Castle Kingside

        return legal_castle_moves


import Board
