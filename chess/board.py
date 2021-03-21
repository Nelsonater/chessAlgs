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
        self.isCheckmate = False
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
        if len(pos) != 2:
            print(f"Invalid string: {pos}. Quitting")
            return
        # Get ascii value of first char in pos string; a=97, b=98, etc. to calc the file
        tile = ord(pos[0])-97
        # Subtract the rank int from second char from boardWidth (which is also the height in this case, cause we index top left to bottom right)
        # Multiply the result by boardwidth to adjust for the 2d tiles list
        tile += (self.boardWidth - int(pos[1]))*self.boardWidth
        return self.tiles[tile]
    
    def getTileColor(self, tile1):
        if self.getTile(tile1) == 0:
            return
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
            self.active = 'w' if self.active == 'b' else 'b'
            self.tiles[tile2] = self.getTile(tile1)
            self.tiles[tile1] = 0
            if len([x for x in self.allLegalMoves().values() if len(x) > 0]) == 0:
                self.isCheckmate = True
    
    def isLegalMove(self, tile1, tile2):
        """ Checks if tile2 is a legal move for the piece on tile1 """
        return True if tile2 in self.getLegalMoves(tile1) else False
    
    def allLegalMoves(self, pretty=False, discAtk=True):
        moves = {}
        for i, t in enumerate(self.tiles):
            if self.getTileColor(i) == self.active:
                legalMoves = self.getLegalMoves(i, discAtk)
                if len(legalMoves) > 0:
                    moves[i] = legalMoves
        if pretty:
            # There's a fancy pythonic way to implement this...should fix soon(tm)
            moveNotation = []
            for p, options in moves.items():
                for move in options:
                    moveNotation.append(self.indexToNotation(move, p))
            return moveNotation
        return moves
    
    def indexToNotation(self, tile1, tile2=None):
        """ Returns the algebraic notation for a given tile index """
        """ Optional arg tile2 can be used for piece notation """
        pos = "" if tile2 == None or self.getTile(tile2).lower() == 'p' else self.getTile(tile2)
        pos += chr(tile1%self.boardWidth+97)
        pos += str(self.boardWidth - int(tile1/self.boardWidth))
        return pos
    
    def getLegalMoves(self, tile1, discAtk=True):
        """ Returns an array of all available legal moves for a given piece, by tile index """
        moves = []
        if self.getTileColor(tile1) != self.active:
            return moves
        piece = self.getTile(tile1)
        if piece != 0:
            if piece == 'p':
                # Black pawn
                # They can move 1 square down so long as it isn't blocked
                if self.getTile(tile1+self.boardWidth) == 0:
                    moves.append(tile1+self.boardWidth)
                # They can attack diagonally if tile is occupied by enemy
                if self.getTile(tile1+self.boardWidth+1) != 0 and self.getTile(tile1+self.boardWidth+1).isupper() and (tile1+self.boardWidth+1)%self.boardWidth != 0 :
                    moves.append(tile1+self.boardWidth+1)
                if self.getTile(tile1+self.boardWidth-1) != 0 and self.getTile(tile1+self.boardWidth-1).isupper() and (tile1+self.boardWidth-1)%self.boardWidth != self.boardWidth-1 :
                    moves.append(tile1+self.boardWidth-1)
                # They can move 2 tiles if on original rank
                if tile1 >= self.boardWidth and tile1 < 2*self.boardWidth:
                    if self.getTile(tile1+2*self.boardWidth) == 0:
                        moves.append(tile1+2*self.boardWidth)
                # TODO: Aunt croissant
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
                # They can move 2 tiles if on original rank
                if tile1 >= self.boardWidth*(self.boardWidth-2) and tile1 < self.boardWidth*(self.boardWidth-1):
                    if self.getTile(tile1-2*self.boardWidth) == 0:
                        moves.append(tile1-2*self.boardWidth)
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
                # ....Knights...oh, knights. The bane of pathing
                # Jk it's really not that bad. Knights can move to up to a maximum of 8 squares so I'll just calc each manually
                # Up left
                if ((tile1-self.boardWidth*2-1)%self.boardWidth != self.boardWidth-1 and tile1-self.boardWidth*2-1 >= 0 and tile1-self.boardWidth*2-1 < len(self.tiles) and (self.getTileColor(tile1-self.boardWidth*2-1) != self.getTileColor(tile1) or self.getTile(tile1-self.boardWidth*2-1) == 0 )):
                    moves.append(tile1-self.boardWidth*2-1)
                # Up right
                if ((tile1-self.boardWidth*2+1)%self.boardWidth != 0 and tile1-self.boardWidth*2+1 >= 0 and tile1-self.boardWidth*2+1 < len(self.tiles) and (self.getTileColor(tile1-self.boardWidth*2+1) != self.getTileColor(tile1) or self.getTile(tile1-self.boardWidth*2+1) == 0 )):
                    moves.append(tile1-self.boardWidth*2+1)
                # Down left
                if ((tile1+self.boardWidth*2-1)%self.boardWidth != self.boardWidth-1 and tile1+self.boardWidth*2-1 >= 0 and tile1+self.boardWidth*2-1 < len(self.tiles) and (self.getTileColor(tile1+self.boardWidth*2-1) != self.getTileColor(tile1) or self.getTile(tile1+self.boardWidth*2-1) == 0 )):
                    moves.append(tile1+self.boardWidth*2-1)
                # Down right
                if ((tile1+self.boardWidth*2+1)%self.boardWidth != 0 and tile1+self.boardWidth*2+1 >= 0 and tile1+self.boardWidth*2+1 < len(self.tiles) and (self.getTileColor(tile1+self.boardWidth*2+1) != self.getTileColor(tile1) or self.getTile(tile1+self.boardWidth*2+1) == 0 )):
                    moves.append(tile1+self.boardWidth*2+1)
                # Left up
                if ((tile1-self.boardWidth-2)%self.boardWidth < self.boardWidth-2 and tile1-self.boardWidth-2 >= 0 and tile1-self.boardWidth-2 < len(self.tiles) and (self.getTileColor(tile1-self.boardWidth-2) != self.getTileColor(tile1) or self.getTile(tile1-self.boardWidth-2) == 0 )):
                    moves.append(tile1-self.boardWidth-2)
                # Left down
                if ((tile1+self.boardWidth-2)%self.boardWidth < self.boardWidth-2 and tile1+self.boardWidth-2 >= 0 and tile1+self.boardWidth-2 < len(self.tiles) and (self.getTileColor(tile1+self.boardWidth-2) != self.getTileColor(tile1) or self.getTile(tile1+self.boardWidth-2) == 0 )):
                    moves.append(tile1+self.boardWidth-2)
                # Right up
                if ((tile1-self.boardWidth+2)%self.boardWidth > 1 and tile1-self.boardWidth+2 >= 0 and tile1-self.boardWidth+2 < len(self.tiles) and (self.getTileColor(tile1-self.boardWidth+2) != self.getTileColor(tile1) or self.getTile(tile1-self.boardWidth+2) == 0 )):
                    moves.append(tile1-self.boardWidth+2)
                # Right down
                if ((tile1+self.boardWidth+2)%self.boardWidth > 1 and tile1+self.boardWidth+2 >= 0 and tile1+self.boardWidth+2 < len(self.tiles) and (self.getTileColor(tile1+self.boardWidth+2) != self.getTileColor(tile1) or self.getTile(tile1+self.boardWidth+2) == 0 )):
                    moves.append(tile1+self.boardWidth+2)

            elif piece.lower() == 'b':
                # Bishop
                # Bishops move infinitely in diagonal lines until board edge or non empty tile
                # Check all tiles up and to right
                markerTile = tile1
                while (markerTile-self.boardWidth+1 >= 0) and self.getTile(markerTile-self.boardWidth+1) == 0 and (markerTile-self.boardWidth+1)%self.boardWidth != 0:
                    markerTile = markerTile - self.boardWidth + 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-self.boardWidth+1)%self.boardWidth != 0 and self.getTileColor(markerTile-self.boardWidth+1) != self.getTileColor(tile1) and (markerTile-self.boardWidth+1 >= 0):
                    moves.append(markerTile-self.boardWidth+1)
                # Check all tiles up and to left
                markerTile = tile1
                while (markerTile-self.boardWidth-1 < len(self.tiles)) and self.getTile(markerTile-self.boardWidth-1) == 0 and (markerTile-self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and (markerTile-self.boardWidth-1 >= 0):
                    markerTile = markerTile - self.boardWidth - 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-self.boardWidth-1 < len(self.tiles)) and (markerTile-self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and self.getTileColor(markerTile-self.boardWidth-1) != self.getTileColor(tile1) and (markerTile-self.boardWidth-1 >= 0):
                    moves.append(markerTile-self.boardWidth-1)
                # Check all tiles down and to right
                markerTile = tile1
                while (markerTile+self.boardWidth+1 < len(self.tiles)) and self.getTile(markerTile+self.boardWidth+1) == 0 and (markerTile+self.boardWidth+1)%self.boardWidth != 0 and (markerTile+self.boardWidth+1 >= 0):
                    markerTile = markerTile + self.boardWidth + 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+self.boardWidth+1 < len(self.tiles)) and (markerTile+self.boardWidth+1)%self.boardWidth != 0 and self.getTileColor(markerTile+self.boardWidth+1) != self.getTileColor(tile1) and (markerTile+self.boardWidth+1 >= 0):
                    moves.append(markerTile+self.boardWidth+1)
                # Check all tiles down and to left
                markerTile = tile1
                while (markerTile+self.boardWidth-1 < len(self.tiles)) and self.getTile(markerTile+self.boardWidth-1) == 0 and (markerTile-self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and (markerTile+self.boardWidth-1 >= 0):
                    markerTile = markerTile + self.boardWidth - 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+self.boardWidth-1 < len(self.tiles)) and (markerTile+self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and self.getTileColor(markerTile+self.boardWidth-1) != self.getTileColor(tile1) and (markerTile+self.boardWidth-1 >= 0):
                    moves.append(markerTile+self.boardWidth-1)
            elif piece.lower() == 'k':
                # King
                # King moves 1 tile in any direction, maybe there's a more elegant way than 8 checks
                # Up left
                if (tile1-self.boardWidth-1 >= 0 and tile1-self.boardWidth-1 < len(self.tiles) and (tile1-self.boardWidth-1 == 0 or self.getTileColor(tile1-self.boardWidth-1) != self.getTileColor(tile1) ) and (tile1-self.boardWidth-1)%self.boardWidth != self.boardWidth-1):
                    moves.append(tile1-self.boardWidth-1)
                # Up
                if (tile1-self.boardWidth >= 0 and tile1-self.boardWidth < len(self.tiles) and (tile1-self.boardWidth == 0 or self.getTileColor(tile1-self.boardWidth) != self.getTileColor(tile1) )):
                    moves.append(tile1-self.boardWidth)
                # Up right
                if (tile1-self.boardWidth+1 >= 0 and tile1-self.boardWidth+1 < len(self.tiles) and (tile1-self.boardWidth+1 == 0 or self.getTileColor(tile1-self.boardWidth+1) != self.getTileColor(tile1) ) and (tile1-self.boardWidth+1)%self.boardWidth != 0):
                    moves.append(tile1-self.boardWidth+1)
                # Left
                if (tile1-1 >= 0 and tile1-1 < len(self.tiles) and (tile1-1 == 0 or self.getTileColor(tile1-1) != self.getTileColor(tile1) )and (tile1-1)%self.boardWidth != self.boardWidth-1 ):
                    moves.append(tile1-1)
                # Reft
                if (tile1+1 >= 0 and tile1+1 < len(self.tiles) and (tile1+1 == 0 or self.getTileColor(tile1+1) != self.getTileColor(tile1) ) and (tile1+1)%self.boardWidth != 0):
                    moves.append(tile1+1)
                # Down left
                if (tile1+self.boardWidth-1 >= 0 and tile1+self.boardWidth-1 < len(self.tiles) and (tile1+self.boardWidth-1 == 0 or self.getTileColor(tile1+self.boardWidth-1) != self.getTileColor(tile1) )and (tile1+self.boardWidth-1)%self.boardWidth != self.boardWidth-1 ):
                    moves.append(tile1+self.boardWidth-1)
                # Down
                if (tile1+self.boardWidth >= 0 and tile1+self.boardWidth < len(self.tiles) and (tile1+self.boardWidth == 0 or self.getTileColor(tile1+self.boardWidth) != self.getTileColor(tile1) )):
                    moves.append(tile1+self.boardWidth)
                # Down right
                if (tile1+self.boardWidth+1 >= 0 and tile1+self.boardWidth+1 < len(self.tiles) and (tile1+self.boardWidth+1 == 0 or self.getTileColor(tile1+self.boardWidth+1) != self.getTileColor(tile1) ) and (tile1+self.boardWidth+1)%self.boardWidth != 0):
                    moves.append(tile1+self.boardWidth+1)
            elif piece.lower() == 'q':
                # Queen
                # Queen code is straightup copy pasted bishop + rook
                # ...maybe I should've wrote a function
                # Check all tiles up and to right
                markerTile = tile1
                while (markerTile-self.boardWidth+1 >= 0) and self.getTile(markerTile-self.boardWidth+1) == 0 and (markerTile-self.boardWidth+1)%self.boardWidth != 0:
                    markerTile = markerTile - self.boardWidth + 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-self.boardWidth+1)%self.boardWidth != 0 and self.getTileColor(markerTile-self.boardWidth+1) != self.getTileColor(tile1) and (markerTile-self.boardWidth+1 >= 0):
                    moves.append(markerTile-self.boardWidth+1)
                # Check all tiles up and to left
                markerTile = tile1
                while (markerTile-self.boardWidth-1 < len(self.tiles)) and self.getTile(markerTile-self.boardWidth-1) == 0 and (markerTile-self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and (markerTile-self.boardWidth-1 >= 0):
                    markerTile = markerTile - self.boardWidth - 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile-self.boardWidth-1 < len(self.tiles)) and (markerTile-self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and self.getTileColor(markerTile-self.boardWidth-1) != self.getTileColor(tile1) and (markerTile-self.boardWidth-1 >= 0):
                    moves.append(markerTile-self.boardWidth-1)
                # Check all tiles down and to right
                markerTile = tile1
                while (markerTile+self.boardWidth+1 < len(self.tiles)) and self.getTile(markerTile+self.boardWidth+1) == 0 and (markerTile+self.boardWidth+1)%self.boardWidth != 0 and (markerTile+self.boardWidth+1 >= 0):
                    markerTile = markerTile + self.boardWidth + 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+self.boardWidth+1 < len(self.tiles)) and (markerTile+self.boardWidth+1)%self.boardWidth != 0 and self.getTileColor(markerTile+self.boardWidth+1) != self.getTileColor(tile1) and (markerTile+self.boardWidth+1 >= 0):
                    moves.append(markerTile+self.boardWidth+1)
                # Check all tiles down and to left
                markerTile = tile1
                while (markerTile+self.boardWidth-1 < len(self.tiles)) and self.getTile(markerTile+self.boardWidth-1) == 0 and (markerTile-self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and (markerTile+self.boardWidth-1 >= 0):
                    markerTile = markerTile + self.boardWidth - 1
                    moves.append(markerTile)
                # If check ended because it ran into an enemy, add them to the legal move list
                if (markerTile+self.boardWidth-1 < len(self.tiles)) and (markerTile+self.boardWidth-1)%self.boardWidth != self.boardWidth-1 and self.getTileColor(markerTile+self.boardWidth-1) != self.getTileColor(tile1) and (markerTile+self.boardWidth-1 >= 0):
                    moves.append(markerTile+self.boardWidth-1)
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
        # Gonna loop through move list here and make sure none put your own king in check
        # These checks could've/should've been done when being originally added to the list but that mess is
        # already spaghetti enough and O(2n) == O(n) I think idk
        if discAtk:
            return [ x for x in moves if not self.isInCheck(tile1, x)]
        return moves
    
    def isInCheck(self, tile1, tile2):
        """ Answers the question: Would someone be in check if this move happened """
        # So... it's easy to figure out if a move someone chose to do also puts the enemy in check after
        # ... but to identify any potential move as bad because if the move is done, a discovery attack will
        # happen on the king sounds like a significantly more expensive process
        # I think there's no way to do it but to replicate the makeMove function but keep track of the move
        t1_piece = self.getTile(tile1)
        t2_piece = self.getTile(tile2)
        self.tiles[tile2] = t1_piece
        self.tiles[tile1] = 0
        self.active = 'w' if self.active == 'b' else 'b'

        for i, t in enumerate(self.tiles):
            if self.getTile(i) == 'k' or self.getTile(i) == 'K':
                movelist = self.allLegalMoves(False, False)
                # if i in movelist.values():
                if i in {x for v in movelist.values() for x in v}:
                    self.active = 'w' if self.active == 'b' else 'b'
                    self.tiles[tile1] = t1_piece
                    self.tiles[tile2] = t2_piece
                    # print(f"Potential Check! If {self.indexToNotation(tile2, tile1)}")
                    # print(movelist)
                    return True
        
        self.active = 'w' if self.active == 'b' else 'b'
        self.tiles[tile1] = t1_piece
        self.tiles[tile2] = t2_piece
        return False

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
                self.tiles[i*self.boardWidth+j] = t
                j += 1
    
    def outputFEN(self):
        fen = self.outputPlacementString()
        fen = f'{fen} {self.active} {self.castling} {self.enpassant} {self.halfmove} {self.fullmove}'
        return fen
    
    def outputPlacementString(self):
        placement = ""
        for r in range(self.boardWidth):
            counter = 0
            for f in range(self.boardWidth):
                piece = self.getTile(r*self.boardWidth+f)
                if piece == 0:
                    counter += 1
                    continue
                else:
                    placement += str(counter) if counter > 0 else ""
                    counter = 0
                    placement += piece
            placement += str(counter) if counter > 0 else ""
            placement += "/"
        placement = placement[:-1]

        return placement
