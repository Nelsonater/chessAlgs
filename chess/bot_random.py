from board import Board
import random

class ChessRandom:
    def __init__(self, board, color):
        self.board = board
        self.color = color
    
    def nextMove(self):
        possibleMoves = self.board.allLegalMoves()
        if len(possibleMoves) == 0:
            return
        piece = random.choice(list(possibleMoves.keys()))
        self.board.movePiece(piece, random.choice(possibleMoves[piece]))
