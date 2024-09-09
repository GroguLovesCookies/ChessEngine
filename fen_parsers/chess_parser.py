from classes.board import Board
from fen_parsers.fen_parser import FenParser
from move_generators.chess_move_generator import ChessMoveGenerator
from pieces import get_piece_value, is_white_piece, chess_pieces


class ChessParser(FenParser):
    def load(self, fen: str) -> Board:
        board = Board(ChessMoveGenerator, self.width, self.height)

        i = 0
        for char in fen:
            if i >= board.width * board.height:
                break
            if char.isdigit():
                i += int(char)
            elif char.isalpha():
                colour = 0b10000 if char.isupper() else 0b00000
                piece = self.piece_bank[char.lower()]
                x = i % board.width
                y = i // board.width
                board[(x, y)] = piece | colour
                bitboard = board.get_bitboard(char.isupper())
                bitboard[piece]  |= 1 << (63 - i)
                if char.lower() == "k":
                    board.kings[0 if char.isupper() else 1] = (x, y)
                i += 1

        board.reload_attacked()
        return board

    def save(self, board: Board) -> str:
        fen: str = ""
        gap: int = 0
        for row in board.board:
            for piece in row:
                if piece == 0:
                    gap += 1
                else:
                    if gap > 0:
                        fen += str(gap)
                        gap = 0
                    char: chr = self.reverse_piece_bank[get_piece_value(piece)]
                    fen += char.upper() if is_white_piece(piece) else char
            if gap > 0:
                fen += str(gap)
                gap = 0
            fen += "/"
        return fen
