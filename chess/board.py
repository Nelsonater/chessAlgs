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
    
    def getTileColor(self, tile1):
        return 'w' if self.getTile(tile1).isupper() else 'b'
    
    def printBoard(self):
        """ Debug tool to print board to console """
        rank = ''
        for i, t in enumerate(self.tiles):
            rank = str(t) + ' ' + rank 
            if i % self.boardWidth == 0:
                print(rank)
                rank = ''
    
    def movePiece(self, tile1, tile2):
        if self.isLegalMove(tile1, tile2):
            self.tiles[tile2] = self.getTile(tile1)
            self.tiles[tile1] = 0
    
    def isLegalMove(self, tile1, tile2):
        """ Checks if tile2 is a legal move for the piece on tile1 """
        return True if tile2 in self.getLegalMoves(tile1) else False
    
    def getLegalMoves(self, tile1):
        """ Returns an array of all available legal moves for a given piece, by tile index """
        moves = []
        piece = self.getTile(tile1)
        if piece != 0:
            if piece == 'p':
                # Black pawn
                # They can move 1 square down so long as it isn't blocked
                if self.getTile(tile1+self.boardWidth) == 0:
                    moves.append(tile1+self.boardWidth)
                # They can attack diagonally if tile is occupied by enemy
                if self.getTile(tile1+self.boardWidth+1) != 0 and self.getTile(tile1+self.boardWidth+1).isupper():
                    moves.append(tile1+self.boardWidth+1)
                if self.getTile(tile1+self.boardWidth-1) != 0 and self.getTile(tile1+self.boardWidth-1).isupper():
                    moves.append(tile1+self.boardWidth-1)
                # TODO: They can move 2 tiles if on original rank
            elif piece == 'P':
                # White pawn
                # They can move 1 square up so long as it isn't blocked
                if self.getTile(tile1-self.boardWidth) == 0:
                    moves.append(tile1-self.boardWidth)
                # They can attack diagonally if tile is occupied by enemy
                if self.getTile(tile1-self.boardWidth+1) != 0 and self.getTile(tile1-self.boardWidth+1).islower():
                    moves.append(tile1-self.boardWidth+1)
                if self.getTile(tile1-self.boardWidth-1) != 0 and self.getTile(tile1-self.boardWidth-1).islower():
                    moves.append(tile1-self.boardWidth-1)
            elif piece.lower() == 'r':
                # Rook
                # Rooks can move infinitely in straight lines until board edge or non empty tile
                # Check all tiles to the right
                markerTile = tile1
                while (markerTile+1 < len(self.tiles)) and self.getTile(markerTile+1) == 0 and (markerTile+1)%self.boardWidth != 0:
                    markerTile += 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+1 < len(self.tiles)) and (markerTile+1)%self.boardWidth != 0 and self.getTileColor(markerTile+1) != self.getTileColor(tile1):
                    moves.append(markerTile+1)
                # Check all tiles to the left
                markerTile = tile1
                while (markerTile-1 >= 0) and self.getTile(markerTile-1) == 0 and (markerTile-1)%self.boardWidth != self.boardWidth-1:
                    markerTile -= 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-1 >= 0) and (markerTile-1)%self.boardWidth != self.boardWidth-1 and self.getTileColor(markerTile-1) != self.getTileColor(tile1):
                    moves.append(markerTile-1)
                # Check all tiles below
                markerTile = tile1
                while (markerTile+8 < len(self.tiles)) and self.getTile(markerTile+8) == 0:
                    markerTile += 8
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+8 < len(self.tiles)) and self.getTileColor(markerTile+8) != self.getTileColor(tile1):
                    moves.append(markerTile+8)
                # Check all tiles above
                markerTile = tile1
                while (markerTile-8 >= 0) and self.getTile(markerTile-8) == 0:
                    markerTile -= 8
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-8 >= 0) and self.getTileColor(markerTile-8) != self.getTileColor(tile1):
                    moves.append(markerTile-8)
            elif piece.lower() == 'n':
                # Knight
                print('night')
            elif piece.lower() == 'b':
                # Bishop
                # Bishops move infinitely in diagonal lines until board edge or non empty tile
                # Check all tiles up and to right
                markerTile = tile1
                while (markerTile-self.boardWidth+1 >= 0) and self.getTile(markerTile-self.boardWidth+1) == 0 and (markerTile-self.boardWidth+1)%self.boardWidth != 0:
                    markerTile -= self.boardWidth+1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-self.boardWidth+1)%self.boardWidth != 0 and self.getTileColor(markerTile-self.boardWidth+1) != self.getTileColor(tile1) and (markerTile-self.boardWidth+1 >= 0):
                    moves.append(markerTile-self.boardWidth+1)
                # Check all tiles up and to left
                markerTile = tile1
                while (markerTile-self.boardWidth-1 < len(self.tiles)) and self.getTile(markerTile-self.boardWidth-1) == 0 and (markerTile-self.boardWidth-1)%self.boardWidth != 0 and (markerTile-self.boardWidth-1 >= 0):
                    markerTile -= self.boardWidth-1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-self.boardWidth-1 < len(self.tiles)) and (markerTile-self.boardWidth-1)%self.boardWidth != 0 and self.getTileColor(markerTile-self.boardWidth-1) != self.getTileColor(tile1) and (markerTile-self.boardWidth-1 >= 0):
                    moves.append(markerTile-self.boardWidth-1)
                # Check all tiles down and to right
                markerTile = tile1
                while (markerTile+self.boardWidth+1 < len(self.tiles)) and self.getTile(markerTile+self.boardWidth+1) == 0 and (markerTile+self.boardWidth+1)%self.boardWidth != 0 and (markerTile+self.boardWidth+1 >= 0):
                    markerTile += self.boardWidth+1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+self.boardWidth+1 < len(self.tiles)) and (markerTile+self.boardWidth+1)%self.boardWidth != 0 and self.getTileColor(markerTile+self.boardWidth+1) != self.getTileColor(tile1) and (markerTile+self.boardWidth+1 >= 0):
                    moves.append(markerTile+self.boardWidth+1)
                # Check all tiles down and to left
                markerTile = tile1
                while (markerTile+self.boardWidth-1 < len(self.tiles)) and self.getTile(markerTile+self.boardWidth-1) == 0 and (markerTile+self.boardWidth-1)%self.boardWidth != 0 and (markerTile+self.boardWidth-1 >= 0):
                    markerTile += self.boardWidth-1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+self.boardWidth-1 < len(self.tiles)) and (markerTile+self.boardWidth-1)%self.boardWidth != 0 and self.getTileColor(markerTile+self.boardWidth-1) != self.getTileColor(tile1) and (markerTile+self.boardWidth-1 >= 0):
                    moves.append(markerTile+self.boardWidth-1)
            elif piece.lower() == 'k':
                # King
                print('bossman')
            elif piece.lower() == 'q':
                # Queen
                print('dama')
        return moves


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
    
    def outputFEN(self):
        fen = self.outputPlacementString()
        fen = f'{fen} {self.active} {self.castling} {self.enpassant} {self.halfmove} {self.fullmove}'
        return fen
    
    def outputPlacementString(self):
        return "8/8/8/8/8/8/8/8"
