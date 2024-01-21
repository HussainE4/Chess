"""
Contains Info about Knight
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from Chess_Pieces.Pieces import Piece


@dataclass
class Knight(Piece):
    """
    A Class representing a Knight
    """

    def __init__(self, colour, position):
        super().__init__(colour, position)
        self.notation = self.colour + 'N'
        self.possible_moves = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

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
