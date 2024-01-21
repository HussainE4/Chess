"""
Contains Info about Rooks
"""

from __future__ import annotations
from dataclasses import dataclass
from Chess_Pieces.Pieces import Piece


@dataclass
class Rook(Piece):
    """
    A Class representing a Rook
    """
    has_moved: bool
    first_move: tuple[int, int]

    def __init__(self, colour, position):
        super().__init__(colour, position)
        self.notation = self.colour + 'R'
        self.has_moved = False
        self.first_move = tuple()
        self.possible_moves = [(y, 0) for y in range(1, 8)] + [(-y, 0) for y in range(1, 8)] + \
                              [(0, x) for x in range(1, 8)] + [(0, -x) for x in range(1, 8)]

    def make_move(self, destination: tuple[int, int]):
        """
        Move the Rook to the specified square. Update the has_moved attribute
        """
        if not self.has_moved:
            self.has_moved = True
            self.first_move = destination
        self.position = destination
