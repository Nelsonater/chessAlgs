from board import Board
from aibase import AIBaseClass
import random

class ChessRandom(AIBaseClass):
    def getNextMove(self):
        possibleMoves = self.board.allLegalMoves()
        if len(possibleMoves) == 0:
            return
        piece = random.choice(list(possibleMoves.keys()))
        self.board.movePiece(piece, random.choice(possibleMoves[piece]))
