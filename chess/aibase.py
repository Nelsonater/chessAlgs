class AIBaseClass:
    def __init__(self, board, color):
        self.board = board
        self.color = color
    
    def getNextMove(self):
        return -1