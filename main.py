from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove

parser = ChessParser()
board = parser.load("r3k11r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R")

gen = ChessMoveGenerator(board)
moves = gen.generate(True)
print(moves)

move = moves[1]
move.make_move()
move.undo_move()
print(board.castling)