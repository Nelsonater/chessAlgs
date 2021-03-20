class Board:
    def __init__(self, boardwidth=8):
        """ Board is essentially represented by a list of Integers
        I chose to represent this a 2d array starting at a8 (top left) and ending h1 (bottom right)
        Even though it hurt my brain a little, this system matches fen better so :shrug:

        0  - Empty
        1  - WKing
        2  - WQueen
        3  - WBishop
        4  - WKnight
        5  - WRook
        6  - WPawn
        7  - BKing
        8  - BQueen
        9  - BBishop
        10 - BKnight
        11 - BRook
        12 - BPawn """
        self.boardWidth = boardwidth
        self.tiles = [0] * self.boardWidth * self.boardWidth
        self.initializeBoard()

    def initializeBoard(self):
        """ Initializes a new board with a standard 8x8 chess board starting position """
        # If given boardWidth was 8, use standard starting pos, otherwise empty
        if self.boardWidth == 8:
            self.importFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

    # Ex. C5 - pos first gets set to '2' because ord('c')-97 is 2
    #     Then if we assume boardWidth of 8, 8-5-1 = 2
    # c5 expected val. 2+2*8 = 18
    # a[0-7], b[8-15], c[16-23]
    def getTile(self, pos):
        """ Gets the integer value for the piece at a given board position
            I couldn't decide if this function should be called with a tile index or standard notation
            ...so I just did both"""
        if type(pos) is int:
            return self.tiles[pos]
        # Get ascii value of first char in pos string; a=97, b=98, etc. to calc the file
        tile = ord(pos[0])-97
        # Subtract the rank int from second char from boardWidth (which is also the height in this case, cause we index top left to bottom right) Also subtract 1 because the list is zero indexed
        # Multiply the result by boardwidth to adjust for the 2d tiles list
        tile += (self.boardWidth - int(pos[1]) - 1)*self.boardWidth
        return self.tiles[tile]
    
    def printBoard(self):
        """ Debug tool to print board to console """
        rank = ''
        for i, t in enumerate(self.tiles):
            rank = rank.join(str(t))
            if i % self.boardWidth:
                print(rank)
                rank = ''


    def importFEN(self, fen):
        """ Imports a new board position starting at a given fen string """
        splitfen = fen.split(' ')
        placement = splitfen[0]
        self.importPlacementString(placement)
        activeplayer = splitfen[1]
        castling = splitfen[2]
        enpassant = splitfen[3]
        halfmove = splitfen[4]
        fullmove = splitfen[5]

    def importPlacementString(self, placement):
        """ Given the first part of a fen string, will assign the tiles with the proper pieces """
        print("TBI")
        self.tiles[56] = 5

