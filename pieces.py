chess_pieces = {
    "p": 0b00001,
    "n": 0b00010,
    "b": 0b00011,
    "r": 0b00100,
    "q": 0b00101,
    "k": 0b00110
}

reverse_chess_pieces = {value: key for key, value in chess_pieces.items()}

def get_piece_value(piece: int):
    return piece & 0b01111

def get_piece_color(piece: int):
    return piece & 0b10000

def is_white_piece(piece: int):
    return get_piece_color(piece) == 0b10000

def is_same_color(piece1: int, piece2: int):
    return piece1 != 0 and piece2 != 0 and get_piece_color(piece1) == get_piece_color(piece2)