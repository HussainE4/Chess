"""
Contains Info about Bishop
"""

from __future__ import annotations
from dataclasses import dataclass
from Chess_Pieces.Pieces import Piece


@dataclass
class Bishop(Piece):
    """
    A Class representing a Bishop
    """

    def __init__(self, colour, position):
        super().__init__(colour, position)
        self.notation = self.colour + 'B'
        self.possible_moves = [(x, x) for x in range(1, 8)] + [(-x, -x) for x in range(1, 8)] + \
                              [(-x, x) for x in range(1, 8)] + [(x, -x) for x in range(1, 8)]
