from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove

parser = ChessParser()
board = parser.load("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R")

gen = ChessMoveGenerator(board)
moves = gen.generate(False)
print(moves)

move = moves[5]
move.make_move()
print(parser.save(board))
print(board.castling)
move.undo_move()
print(board.castling)