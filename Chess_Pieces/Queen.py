"""
Contains Info about Queens
"""

from __future__ import annotations
from dataclasses import dataclass
from Chess_Pieces.Pieces import Piece


@dataclass
class Queen(Piece):
    """
    A Class representing a Queen
    """

    def __init__(self, colour, position):
        super().__init__(colour, position)
        self.notation = self.colour + 'Q'
        self.possible_moves = [(y, 0) for y in range(1, 8)] + [(-y, 0) for y in range(1, 8)] + \
                              [(0, x) for x in range(1, 8)] + [(0, -x) for x in range(1, 8)] + \
                              [(x, x) for x in range(1, 8)] + [(-x, -x) for x in range(1, 8)] + \
                              [(-x, x) for x in range(1, 8)] + [(x, -x) for x in range(1, 8)]
