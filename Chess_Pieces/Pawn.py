"""
Contains Info about Pawns
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from Chess_Pieces.Pieces import Piece
from Chess_Pieces.Queen import Queen
from Chess_Pieces.Rook import Rook
from Chess_Pieces.Bishop import Bishop
from Chess_Pieces.Knight import Knight


@dataclass
class Pawn(Piece):
    """
    A Class representing a Pawn
    """
    has_moved: bool
    first_move: tuple[int, int]

    def __init__(self, colour, position):
        super().__init__(colour, position)
        self.notation = self.colour + 'P'
        self.has_moved = False
        self.first_move = tuple()
        if self.colour == 'W':
            self.possible_moves = [(1, 0), (2, 0), (1, 1), (1, -1)]
        else:
            self.possible_moves = [(-1, 0), (-2, 0), (-1, 1), (-1, -1)]

    def get_legal_moves(self, board: list[list[Optional[Piece]]]) -> list[tuple]:
        """
        Get the legal moves that can be made by the piece on a board with the given position
        """
        legal_moves = []
        rank, file = self.position
        # if self.colour == 'W':
        #     if board[rank + 1][file] is None:
        #         legal_moves.append((1 + rank, 0 + file))
        #         if not self.has_moved and board[rank + 2][file] is None:
        #             legal_moves.append((2 + rank, 0 + file))
        #
        #     if file != 0 and board[rank + 1][file - 1] is not None and board[rank + 1][file - 1].colour == 'B':
        #         legal_moves.append((1 + rank, -1 + file))
        #
        #     if file != 7 and board[rank + 1][file + 1] is not None and board[rank + 1][file + 1].colour == 'B':
        #         legal_moves.append((1 + rank, 1 + file))
        # else:
        #     if board[rank - 1][file] is None:
        #         legal_moves.append((-1 + rank, 0 + file))
        #         if not self.has_moved and board[rank - 2][file] is None:
        #             legal_moves.append((-2 + rank, 0 + file))
        #
        #     if file != 0 and board[rank - 1][file - 1] is not None and board[rank - 1][file - 1].colour == 'W':
        #         legal_moves.append((-1 + rank, -1 + file))
        #
        #     if file != 7 and board[rank - 1][file + 1] is not None and board[rank - 1][file + 1].colour == 'W':
        #         legal_moves.append((-1 + rank, 1 + file))

        for move in self.possible_moves:
            if 0 <= move[0] + rank <= 7 and 0 <= move[1] + file <= 7:
                # If making the move will keep the piece within the boundaries of the board

                if move[1] == 0:
                    # It is not a capture

                    # Either colour pawn moving one square
                    if abs(move[0]) == 1 and board[move[0] + rank][move[1] + file] is None:
                        # If the square is empty, it is a legal move
                        legal_moves.append((move[0] + rank, move[1] + file))

                    # White pawn moving two squares forward
                    elif move[0] == 2 and not self.has_moved and board[2 + rank][file] is None and\
                            board[1 + rank][file] is None:
                        # If both squares in front of the pawn are empty and pawn has not moved, it is legal
                        legal_moves.append((move[0] + rank, move[1] + file))

                    # Black pawn moving two squares forward
                    elif move[0] == -2 and not self.has_moved and board[-2 + rank][file] is None and \
                            board[-1 + rank][file] is None:
                        # If both squares in front of the pawn are empty and pawn has not moved, it is legal
                        legal_moves.append((move[0] + rank, move[1] + file))

                else:
                    # Captures
                    if board[move[0] + rank][move[1] + file] is not None and \
                            board[move[0] + rank][move[1] + file].colour != self.colour:

                        legal_moves.append((move[0] + rank, move[1] + file))

        return legal_moves

    def make_move(self, destination: tuple[int, int]):
        """
        Move a piece to the specified square
        """
        if not self.has_moved:
            self.has_moved = True
            self.first_move = destination
        self.position = destination

    # No longer used
    # def promote(self, piece_to_promote, board: list[list[Optional[Piece]]]):
    #     """
    #     Promote a pawn to piece_to_promote on board
    #     """
    #
    #     rank, file = self.position
    #     if piece_to_promote == 'Q':
    #         board[rank][file] = Queen(self.colour, self.position)
    #
    #     elif piece_to_promote == 'R':
    #         # Added this to prevent chicanery with castling
    #         new_piece = Rook(self.colour, self.position)
    #         new_piece.has_moved = True
    #         board[rank][file] = new_piece
    #
    #     elif piece_to_promote == 'N':
    #         board[rank][file] = Knight(self.colour, self.position)
    #     elif piece_to_promote == 'B':
    #         board[rank][file] = Bishop(self.colour, self.position)
