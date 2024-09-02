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
    MT_DOUBLE_PUSH = 7
    MT_EN_PASSANT = 8

    def __init__(self, board: Board, start: tuple, end: tuple, move_type: int = 0):
        super().__init__(board, start, end)
        self.move_type = move_type

    def make_move(self):
        self.board.reset_rights()
        if self.move_type == ChessMove.MT_CASTLE_LONG:
            rank = 7 if self.is_white_move else 0
            self.board[(2, rank)] = self.board[(4, rank)]
            self.board[(4, rank)] = 0
            self.board[(3, rank)] = self.board[(0, rank)]
            self.board[(0, rank)] = 0

            self.board.castling[0 if self.is_white_move else 2] = False
            self.board.castling[1 if self.is_white_move else 3] = False

            return
        elif self.move_type == ChessMove.MT_CASTLE_SHORT:
            rank = 7 if self.is_white_move else 0
            self.board[(6, rank)] = self.board[(4, rank)]
            self.board[(4, rank)] = 0
            self.board[(5, rank)] = self.board[(7, rank)]
            self.board[(7, rank)] = 0

            self.board.castling[0 if self.is_white_move else 2] = False
            self.board.castling[1 if self.is_white_move else 3] = False

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
        elif self.move_type == ChessMove.MT_DOUBLE_PUSH:
            offset: int = 1 if self.is_white_move else -1
            self.board.ep_square = ((self.end[0], self.end[1] + offset), self.end)
        elif self.move_type == ChessMove.MT_EN_PASSANT:
            ep_square = self.board.ep_square[-1]
            if ep_square[0] is not None:
                self.board[ep_square[1]] = 0

        if get_piece_value(self.piece_moved) == chess_pieces["k"]:
            self.board.castling[0 if self.is_white_move else 2] = False
            self.board.castling[1 if self.is_white_move else 3] = False

        if get_piece_value(self.piece_moved) == chess_pieces["r"]:
            if self.start[0] == 0:
                self.board.castling[0 if self.is_white_move else 2] = False
            elif self.start[0] == 7:
                self.board.castling[1 if self.is_white_move else 3] = False


    def undo_move(self):
        self.board.restore_rights()
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

        if self.piece_moved == 0:
            return ""
        moved = reverse_chess_pieces[get_piece_value(self.piece_moved)]
        moved = "" if moved == "p" else moved.upper()

        target_file = ascii_lowercase[self.end[0]]
        target_rank = 8 - self.end[1]
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