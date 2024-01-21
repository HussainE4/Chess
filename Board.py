"""
Contains Info about Chess Board
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from Chess_Pieces.Pieces import Piece
from Chess_Pieces.King import King
from Chess_Pieces.Queen import Queen
from Chess_Pieces.Rook import Rook
from Chess_Pieces.Bishop import Bishop
from Chess_Pieces.Knight import Knight
from Chess_Pieces.Pawn import Pawn


EMPTY_BOARD = [[None for i in range(8)] for c in range(8)]


@dataclass
class Board:
    """ A Chess Board

    Instance Atrributes:
        - positions: A list of the 8 ranks. Each rank is a list of the pieces stored at each square or None if empty
        - black_pieces: A list of all the black pieces
        - white_pieces: A list of all the white pieces
        - white_king_location: A tuple storing the current location of the white king
        - black_king_location: A tuple storing the current location of the black king
        - captured_pieces: A list storing all of the captured pieces (used for unmaking moves)

    Representation Invariants:
    """
    positions: list[list[Optional[Piece]]]
    black_pieces: list[Piece]
    white_pieces: list[Piece]
    white_king_location: tuple[int, int]
    black_king_location: tuple[int, int]
    captured_pieces: list[Piece]
    moves: list[tuple[tuple[int, int], tuple[int, int], bool]]

    def __init__(self, position: list[list[Optional[Piece]]]):

        if position == EMPTY_BOARD:
            # Set up the board with all the pieces
            self.positions = [[None for _ in range(8)] for _ in range(8)]
            self.positions[0] = [Rook('W', (0, 0)), Knight('W', (0, 1)), Bishop('W', (0, 2)), Queen('W', (0, 3)),
                                 King('W', (0, 4)), Bishop('W', (0, 5)), Knight('W', (0, 6)), Rook('W', (0, 7))]
            self.positions[7] = [Rook('B', (7, 0)), Knight('B', (7, 1)), Bishop('B', (7, 2)), Queen('B', (7, 3)),
                                 King('B', (7, 4)), Bishop('B', (7, 5)), Knight('B', (7, 6)), Rook('B', (7, 7))]

            for i in range(8):
                self.positions[1][i] = Pawn('W', (1, i))
                self.positions[6][i] = Pawn('B', (6, i))

            # self.positions[2: 6] = [[None] * 8] * 4
            self.white_pieces = self.positions[0] + self.positions[1]
            self.black_pieces = self.positions[7] + self.positions[6]
            self.white_king_location = (0, 4)
            self.black_king_location = (7, 4)
            self.captured_pieces = []
            self.moves = []

        else:
            # Creating an instance of Board when given a set up of the positions of the pieces
            self.positions = position
            self.white_pieces = []
            self.black_pieces = []
            self.captured_pieces = []
            self.moves = []

            for row in position:
                for square in row:

                    if square is not None:
                        if square.colour == 'W':
                            self.white_pieces.append(square)
                        else:
                            self.black_pieces.append(square)

                        if isinstance(square, King) and square.colour == 'W':
                            self.white_king_location = square.position
                        elif isinstance(square, King) and square.colour == 'B':
                            self.black_king_location = square.position

    def make_move(self, start_position: tuple[int, int], end_position: tuple[int, int]):
        """
        Move the piece at start_position to end_position
        """
        piece = self.positions[start_position[0]][start_position[1]]
        piece.make_move(end_position)

        # Deal with Castling
        if isinstance(piece, King):
            if end_position[1] - start_position[1] == 2:
                # Kingside Castle
                rook = self.positions[end_position[0]][7]
                assert isinstance(rook, Rook)
                rook.make_move((end_position[0], 5))
                piece.has_castled = True
                self.positions[end_position[0]][5], self.positions[end_position[0]][7] = rook, None

            elif end_position[1] - start_position[1] == -2:
                # Queenside Castle
                rook = self.positions[end_position[0]][0]
                assert isinstance(rook, Rook)
                rook.make_move((end_position[0], 3))
                piece.has_castled = True
                self.positions[end_position[0]][3], self.positions[end_position[0]][0] = rook, None

        # Update the board
        self.update_board(piece, end_position, start_position)
        # self.print_board()

    def update_board(self, piece: Piece, end_position: tuple[int, int], start_position: tuple[int, int]):
        """
        Update the board state to reflect piece moving from start_position to end_position
        """

        if isinstance(self.positions[end_position[0]][end_position[1]], Piece):
            self.moves.append((start_position, end_position, True))
            # If it is a Capture, then remove captured piece from list of pieces
            piece_to_remove = self.positions[end_position[0]][end_position[1]]
            self.captured_pieces.append(piece_to_remove)
            if piece.colour == 'W':
                self.black_pieces.remove(piece_to_remove)
            else:
                self.white_pieces.remove(piece_to_remove)
        else:
            self.moves.append((start_position, end_position, False))

        # Move piece from start_position to end_position
        self.positions[end_position[0]][end_position[1]],\
            self.positions[start_position[0]][start_position[1]] = piece, None

        # Update King location if it was the piece that was moved
        if isinstance(piece, King):
            if piece.colour == 'W':
                self.white_king_location = piece.position
            else:
                self.black_king_location = piece.position

        # Promote Pawn if at the end
        # if isinstance(piece, Pawn) and \
        #         ((piece.colour == 'W' and end_position[0] == 7) or (piece.colour == 'B' and end_position[0] == 0)):
        #
        #     piece_to_promote = ''
        #     while piece_to_promote not in {'Q', 'R', 'N', 'B'}:
        #         piece_to_promote = input("Enter the piece that the pawn should be promoted to (Q, R, N, B)")
        #     piece.promote(piece_to_promote, self.positions)
        #
        #     if piece.colour == 'W':
        #         self.white_pieces.remove(piece)
        #         self.white_pieces.append(self.positions[end_position[0]][end_position[1]])
        #     else:
        #         self.black_pieces.remove(piece)
        #         self.black_pieces.append(self.positions[end_position[0]][end_position[1]])

    def all_legal_moves(self, colour: str) -> set[tuple[int, int]]:
        """
        Return all the positions that are being looked at by a certain colour
        """

        moves = set()
        if colour == 'W':
            for piece in self.white_pieces:
                moves.update(piece.get_legal_moves(self.positions))
        else:
            for piece in self.black_pieces:
                moves.update(piece.get_legal_moves(self.positions))

        return moves

    def legal_check_moves(self, colour: str) -> set[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Return all the positions that can be legally moved to by a certain colour
        """
        moves = set()
        if colour == 'W':
            for piece in self.white_pieces:
                moves.update(piece.legal_check_moves(self.positions))
        else:
            for piece in self.black_pieces:
                moves.update(piece.legal_check_moves(self.positions))

        return moves

    def king_in_check(self, colour: str) -> bool:
        """
        Return whether the king of colour is in check or not.
        """
        king_location = self.get_king_location(colour)

        if colour == 'W':
            # Return if the white king's current location is attacked by any of black's pieces
            return king_location in self.all_legal_moves('B')
        else:
            # Return if the black king's current location is attacked by any of white's pieces
            return king_location in self.all_legal_moves('W')

    def get_king_location(self, colour: str) -> tuple[int, int]:
        """
        Return the position of the colour king
        """
        if colour == 'W':
            return self.white_king_location
        else:
            return self.black_king_location

    def promote_pawn(self, pawn_to_promote: Pawn, new_piece: str):
        """
        Promote the pawn to new_piece at end_position
        """

        rank, file = pawn_to_promote.position
        board = self.positions

        # Update board position to replace pawn_to_promote with the new piece
        if new_piece == 'Q':
            board[rank][file] = Queen(pawn_to_promote.colour, pawn_to_promote.position)

        elif new_piece == 'R':
            new_piece = Rook(pawn_to_promote.colour, pawn_to_promote.position)
            # Added this to prevent chicanery with castling
            new_piece.has_moved = True
            board[rank][file] = new_piece

        elif new_piece == 'N':
            board[rank][file] = Knight(pawn_to_promote.colour, pawn_to_promote.position)

        elif new_piece == 'B':
            board[rank][file] = Bishop(pawn_to_promote.colour, pawn_to_promote.position)

        # Update list of pieces
        if pawn_to_promote.colour == 'W':
            self.white_pieces.remove(pawn_to_promote)
            self.white_pieces.append(self.positions[rank][file])
        else:
            self.black_pieces.remove(pawn_to_promote)
            self.black_pieces.append(self.positions[rank][file])

    def clear_board(self):
        """
        Resets the board positions after a game
        """

        self.__init__(EMPTY_BOARD)

    def unmake_move(self):
        """
        Undoes a move that took a piece from start position to end position
        """
        start_position, end_position, capture = self.moves.pop()
        piece = self.positions[end_position[0]][end_position[1]]
        piece.position = start_position

        self.positions[end_position[0]][end_position[1]], \
            self.positions[start_position[0]][start_position[1]] = None, piece

        if (isinstance(piece, Pawn) or isinstance(piece, King) or isinstance(piece, Rook)) and piece.first_move == end_position:
            piece.has_moved = False
            piece.first_move = ()

        if isinstance(piece, King):
            if end_position[1] - start_position[1] == 2:
                rook = self.positions[end_position[0]][5]
                rook.position = (end_position[0], 7)
                assert isinstance(rook, Rook)
                rook.has_moved = False
                piece.has_castled = False
                piece.has_moved = False
                self.positions[end_position[0]][5], self.positions[end_position[0]][7] = None, rook

            elif end_position[1] - start_position[1] == -2:
                # Queenside Castle
                rook = self.positions[end_position[0]][3]
                rook.position = (end_position[0], 0)
                assert isinstance(rook, Rook)
                rook.has_moved = False
                piece.has_castled = False
                self.positions[end_position[0]][3], self.positions[end_position[0]][0] = None, rook

            # Update King Location
            if piece.colour == 'W':
                self.white_king_location = piece.position
            else:
                self.black_king_location = piece.position

        if len(self.captured_pieces) > 0 and capture:
            last_captured_piece = self.captured_pieces.pop()

            # Then the last move was a capture
            self.positions[end_position[0]][end_position[1]] = last_captured_piece

            if piece.colour == 'W':
                self.black_pieces.append(last_captured_piece)
            else:
                self.white_pieces.append(last_captured_piece)

    # def check_castle_legality(self, colour: str):
    #     """
    #     Return if it is possible for a king of side colour to castle
    #     """
    #     king_location = self.get_king_location(colour)
    #     king = self.positions[king_location[0]][king_location[1]]
        # if king.colour == 'W':
        #     rook_positions = [(0, 0), (0, 7)]
        # else:
        #     rook_positions = [(7, 0), (7, 7)]

        # if not king.has_moved:
        #     if king.colour == 'W':
        #         rook_positions = [(0, 0), (0, 7)]
        #         # King location = (0, 4)
        #         for position in rook_positions:
        #             piece = self.positions[position[0]][position[1]]
        #             if isinstance(piece, Rook) and not piece.has_moved:
        #                 for square in range()

        # piece = self.positions[0][0]
        # if isinstance(piece, Rook) and not piece.has_moved:
        #     if self.positions[0][1] is None and self.positions[0][2] is None and self.positions[0][3] is None:
        #         opposite_legal_moves = self.all_legal_moves('B')
    #         if self.positions[0][2] not in opposite_legal_moves and self.positions[0][3] not in opposite_legal_moves:
        #             return True

    # No longer used
    def print_board(self):
        """
        Prints the chess board in a grid state
        """
        for i in range(7, -1, -1):
            print(i + 1, end=' ')
            for piece in self.positions[i]:
                if piece is None:
                    print('[  ]', end=' ')
                else:
                    print('[' + piece.notation + ']', end=' ')
            print()
        print("    A    B    C    D    E    F    G    H")


# No longer used
def coordinate_to_position(coordinate: str) -> tuple[int, int]:
    """
    Convert chess board coordinates to a usable tuple
    >>> coordinate_to_position('A1')
    (0, 0)
    >>> coordinate_to_position('A8')
    (7, 0)
    >>> coordinate_to_position('H1')
    (0, 7)
    >>> coordinate_to_position('E4')
    (3, 4)

    """
    file, rank = coordinate
    file = str(file).upper()
    return (int(rank) - 1, ord(file) - ord('A'))


def position_to_coordinate(position: tuple[int, int]) -> str:
    """
    Convert the tuple containing a position on the board into actual chess coordinates
    >>> position_to_coordinate((0, 0))
    'A1'
    >>> position_to_coordinate((7, 0))
    'A8'
    >>> position_to_coordinate((0, 7))
    'H1'
    >>> position_to_coordinate((3, 4))
    'E4'
    """

    rank, file = position
    return chr(97 + file) + str(rank + 1)
