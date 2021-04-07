class AIBaseClass:
    def __init__(self, board, color):
        self.board = board
        self.color = color
    
    def getNextMove(self):
        return -1
    
    def getBoardScore(self, nextMove = None):
        return -1