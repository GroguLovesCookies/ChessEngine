from classes.board import Board
from typing import Dict
from pieces import chess_pieces


class FenParser:
    def __init__(self, width: int=8, height: int=8, piece_bank: Dict[chr, int] = chess_pieces):
        self.width = width
        self.height = height
        self.piece_bank = piece_bank
        self.reverse_piece_bank: Dict[int, chr] = {value: key for key, value in piece_bank.items()}

    def load(self, fen: str) -> Board:
        ...

    def save(self, board: Board) -> str:
        ...