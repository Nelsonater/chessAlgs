class Board:
    def __init__(self, boardwidth=8):
        """ Board is essentially represented by a list of chars
        I chose to represent this a 2d array starting at a8 (top left) and ending h1 (bottom right)
        Even though it hurt my brain a little, this system matches fen better so :shrug:

        0 - Empty
        K - WKing
        Q - WQueen
        B - WBishop
        N - WKnight
        R - WRook
        P - WPawn
        k - BKing
        q - BQueen
        b - BBishop
        n - BKnight
        r - BRook
        p - BPawn """
        self.boardWidth = boardwidth
        self.tiles = [0] * self.boardWidth * self.boardWidth
        self.active = 'w'
        self.castling = 'KQkq'
        self.enpassant = '-'
        self.halfmove = '0'
        self.fullmove = '1'
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
        # Subtract the rank int from second char from boardWidth (which is also the height in this case, cause we index top left to bottom right)
        # Multiply the result by boardwidth to adjust for the 2d tiles list
        tile += (self.boardWidth - int(pos[1]))*self.boardWidth
        return self.tiles[tile]
    
    def printBoard(self):
        """ Debug tool to print board to console """
        rank = ''
        for i, t in enumerate(self.tiles):
            rank = str(t) + ' ' + rank 
            if i % self.boardWidth == 0:
                print(rank)
                rank = ''
    
    def movePiece(self, tile1, tile2):
        if self.legalMove(tile1, tile2):
            self.tiles[tile2] = self.getTile(tile1)
            self.tiles[tile1] = 0
    
    def legalMove(self, tile1, tile2):
        """ Will one day run checks if piece on tile1 can move to tile2. For now it's anarchy baby """
        return True

    def importFEN(self, fen):
        """ Imports a new board position starting at a given fen string """
        splitfen = fen.split(' ')
        placement = splitfen[0]
        self.importPlacementString(placement)
        activeplayer = splitfen[1]
        self.active = activeplayer
        castling = splitfen[2]
        self.castling = castling
        enpassant = splitfen[3]
        self.enpassant = enpassant
        halfmove = splitfen[4]
        self.halfmove = halfmove
        fullmove = splitfen[5]
        self.fullmove = fullmove

    def importPlacementString(self, placement):
        """ Given the first part of a fen string, will assign the tiles with the proper pieces """
        ranks = placement.split('/')
        for i, r in enumerate(ranks):
            j = 0
            for t in r:
                if t.isdigit():
                    j += int(t)
                    continue
                self.tiles[i*8+j] = t
                j += 1

