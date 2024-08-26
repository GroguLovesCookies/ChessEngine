from string import ascii_lowercase

from classes.board import Board
from moves.move import Move
from pieces import chess_pieces, get_piece_color, reverse_chess_pieces, get_piece_value


class ChessMove(Move):
    MT_CASTLE_SHORT = 1
    MT_CASTLE_LONG = 2
    MT_PROMOTE_QUEEN = 3
    MT_PROMOTE_ROOK = 4
    MT_PROMOTE_BISHOP = 5
    MT_PROMOTE_KNIGHT = 6

    def __init__(self, board: Board, start: tuple, end: tuple, move_type: int = 0):
        super().__init__(board, start, end)
        self.move_type = move_type

    def make_move(self):
        if self.move_type == ChessMove.MT_CASTLE_LONG:
            rank = 7 if self.is_white_move else 0
            self.board[(2, rank)] = self.board[(4, rank)]
            self.board[(4, rank)] = 0
            self.board[(3, rank)] = self.board[(0, rank)]
            self.board[(0, rank)] = 0
            return
        elif self.move_type == ChessMove.MT_CASTLE_SHORT:
            rank = 7 if self.is_white_move else 0
            self.board[(6, rank)] = self.board[(4, rank)]
            self.board[(4, rank)] = 0
            self.board[(5, rank)] = self.board[(7, rank)]
            self.board[(7, rank)] = 0
            return
        self.board[self.start] = 0
        self.board[self.end] = self.piece_moved
        if self.move_type == ChessMove.MT_PROMOTE_QUEEN:
            self.board[self.end] = chess_pieces["q"] | get_piece_color(self.piece_moved)
        elif self.move_type == ChessMove.MT_PROMOTE_ROOK:
            self.board[self.end] = chess_pieces["r"] | get_piece_color(self.piece_moved)
        elif self.move_type == ChessMove.MT_PROMOTE_BISHOP:
            self.board[self.end] = chess_pieces["b"] | get_piece_color(self.piece_moved)
        elif self.move_type == ChessMove.MT_PROMOTE_KNIGHT:
            self.board[self.end] = chess_pieces["n"] | get_piece_color(self.piece_moved)

    def undo_move(self):
        if self.move_type == ChessMove.MT_CASTLE_LONG:
            rank = 7 if self.is_white_move else 0
            self.board[(4, rank)] = self.board[(2, rank)]
            self.board[(2, rank)] = 0
            self.board[(0, rank)] = self.board[(3, rank)]
            self.board[(3, rank)] = 0
            return
        elif self.move_type == ChessMove.MT_CASTLE_SHORT:
            rank = 7 if self.is_white_move else 0
            self.board[(4, rank)] = self.board[(6, rank)]
            self.board[(6, rank)] = 0
            self.board[(7, rank)] = self.board[(5, rank)]
            self.board[(5, rank)] = 0
            return

        self.board[self.start] = self.piece_moved
        self.board[self.end] = self.piece_taken

    def __repr__(self):
        if self.move_type == ChessMove.MT_CASTLE_SHORT:
            return "O-O"
        elif self.move_type == ChessMove.MT_CASTLE_LONG:
            return "O-O-O"

        moved = reverse_chess_pieces[get_piece_value(self.piece_moved)]
        moved = "" if moved == "p" else moved.upper()

        target_file = ascii_lowercase[self.end[0]]
        target_rank = self.end[1] + 1
        out: str = f"{moved}{target_file}{target_rank}"

        if self.move_type == ChessMove.MT_PROMOTE_QUEEN:
            return out + "=Q"
        elif self.move_type == ChessMove.MT_PROMOTE_ROOK:
            return out + "=R"
        elif self.move_type == ChessMove.MT_PROMOTE_BISHOP:
            return out + "=B"
        elif self.move_type == ChessMove.MT_PROMOTE_KNIGHT:
            return out + "=N"

        return out