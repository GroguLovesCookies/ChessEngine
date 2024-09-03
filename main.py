from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove

parser = ChessParser()
board = parser.load("K7/8/8/1r6/8/8/8/8")
board.castling[2] = False
board.castling[3] = False
print(list(board.attacked_squares))

gen = ChessMoveGenerator(board)
moves = gen.generate(True, True)
print(moves)

for y, row in enumerate(board):
    print("\n", "---"*8)
    for x, column in enumerate(row):
        print("|%|" if (x, y) in board.attacked_squares else "| |", end="")