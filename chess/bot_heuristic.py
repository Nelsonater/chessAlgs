from board import Board
from aibase import AIBaseClass
import random
from copy import copy

class BotHeuristic(AIBaseClass):
    def getNextMove(self):
        possibleMoves = self.board.allLegalMoves()
        bestScore = -1
        bestMove = ()
        if len(possibleMoves) == 0:
            return
        for move in possibleMoves:
            for obj in possibleMoves[move]:
                moveScore = self.getBoardScore([(move, obj)])
                if bestScore < moveScore:
                    bestScore = moveScore
                    bestMove = (move,obj)
        print(f"Found best move {self.board.indexToNotation(bestMove[0])} to {self.board.indexToNotation(bestMove[1])}")
        self.board.movePiece(bestMove[0], bestMove[1])
    
    def getBoardScore(self, nextMoves = None):
        """ Attempt to 'score' the current board position, or the board position
            after nextMoves if nextMoves is not None. nextMoves is a list of tuples
            detailing what moves to do from current board position """
        score = 0
        # Score increments, fiddle with these as needed
        inc_takepiece = 5
        inc_middleboard = 3
        inc_outermid = 2
        # Get representation of board to work with
        newboard = copy(self.board.getTiles())
        for t1, t2 in nextMoves:
            newboard[t2] = newboard[t1]
            newboard[t1] = 0
        # First off, purely look for material advantages
        for tile in newboard:
            if tile == 'r': score -= 500
            if tile == 'n': score -= 300
            if tile == 'b': score -= 300
            if tile == 'q': score -= 900
            if tile == 'k': score -= 99999
            if tile == 'p': score -= 100
            if tile == 'R': score += 500
            if tile == 'N': score += 300
            if tile == 'B': score += 300
            if tile == 'Q': score += 900
            if tile == 'K': score += 99999
            if tile == 'P': score += 100
        if self.color == 'b': score = -score
        # Computer likes direct control of middle
        # TODO: Weigh this to vastly prefer pawns/knights
        # Score inceases moderately for each piece bot has in d4/d5/e4/e5
        if ((newboard[self.board.notationToIndex('d4')].isupper() and self.color == 'w') or
            (newboard[self.board.notationToIndex('d4')].islower() and self.color == 'b')):
            score += inc_middleboard
        if ((newboard[self.board.notationToIndex('d5')].isupper() and self.color == 'w') or
            (newboard[self.board.notationToIndex('d5')].islower() and self.color == 'b')):
            score += inc_middleboard
        if ((newboard[self.board.notationToIndex('e4')].isupper() and self.color == 'w') or
            (newboard[self.board.notationToIndex('e4')].islower() and self.color == 'b')):
            score += inc_middleboard
        if ((newboard[self.board.notationToIndex('e5')].isupper() and self.color == 'w') or
            (newboard[self.board.notationToIndex('e5')].islower() and self.color == 'b')):
            score += inc_middleboard
        # Computer likes indirect control of middle
        # Score increases if bishops/rooks/queens can see middle tiles
        # Computer likes putting their king close to the corner
        # Look at pawn structure to determine which player controls more tiles
        # Pawns like to be as far forward as possible while staying connected
        # Penalize weaknesses like backwards pawns, doubling pawns
        # Reward castling when available/moving pieces that are preventing castling
        # Penalize moving the pawns in front of the king after castling
        # Penalize giving up castling rights (except obv to castle)
        # Reward putting the rooks on the opponents back 2 ranks
        # Reward doubling rooks/knights to a lesser extent
        return score