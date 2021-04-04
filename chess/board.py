import math
"""

TO IMPLEMENT:
board.py
    Castling
    Drawing
    En passant
    50 move rule
    I'm pretending like I don't 100% know I've made a lot of time complexity efficiency errors in this codebase
    that will definitely bite me in the ass at scale when training future AI. pls fix
main.py
    make rendering less shit
bot_random.py
    inherit from base AI class

"""
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
        # Keeps track of the starting index of the "castling rooks"
        self.castlingrooks = {}
        # Generated list of moves a king could castle to
        self.castlingmoves = []
        # gamestate var to track if game 
        # 0 - Playing
        # 1 - Black checkmate
        # 2 - White checkmate
        # 3 - Draw
        self.gamestate = 0
        self.initializeBoard()

    def initializeBoard(self):
        """ Initializes a new board with a standard 8x8 chess board starting position """
        # If given boardWidth was 8, use standard starting pos, otherwise empty
        if self.boardWidth == 8:
            self.importFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        for i, t in enumerate(self.tiles):
            if t == 'K':
                for j in range(i, i+self.boardWidth):
                    if j >= 0 and j < len(self.tiles) and self.getTile(j) == 'R':
                        self.castlingrooks['wk'] = j
                for j in range(i-self.boardWidth, i):
                    if j >= 0 and j < len(self.tiles) and self.getTile(j) == 'R':
                        self.castlingrooks['wq'] = j
            if t == 'k':
                for j in range(i, i+self.boardWidth):
                    if j >= 0 and j < len(self.tiles) and self.getTile(j) == 'r':
                        self.castlingrooks['bk'] = j
                for j in range(i-self.boardWidth, i):
                    if j >= 0 and j < len(self.tiles) and self.getTile(j) == 'r':
                        self.castlingrooks['bq'] = j


    # Ex. C5 - pos first gets set to '2' because ord('c')-97 is 2
    #     Then if we assume boardWidth of 8, 8-5-1 = 2
    # c5 expected val. 2+2*8 = 18
    # a[0-7], b[8-15], c[16-23]
    def getTile(self, pos, getIndex=False):
        """ Gets the integer value for the piece at a given board position
            I couldn't decide if this function should be called with a tile index or standard notation
            ...so I just did both. Optional param index to instead return tile index"""
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
        print(f"Translated {pos} to {tile}")
        return self.tiles[tile] if getIndex == False else tile
    
    def getTileColor(self, tile1):
        if self.getTile(tile1) == 0:
            return
        return 'w' if self.getTile(tile1).isupper() else 'b'
    
    def setTile(self, tile1, piece):
        if tile1 >= 0 and tile1 < len(self.tiles):
            self.tiles[tile1] = piece
    
    def asciiBoard(self):
        """ Debug tool to print board to console """
        # TODO: Fix, make it look better, build and return a string instead of printing
        board = ''
        for i, t in enumerate(self.tiles):
            if t == 0:
                board += '*'
            else:
                board += str(t)
            if (i+1) % self.boardWidth == 0:
                board += '\n'
        return board
    
    def movePiece(self, tile1, tile2):
        if self.isLegalMove(tile1, tile2):
            # Remove castling rights if king moves
            if self.getTile(tile1) == 'K':
                self.castling = self.castling.replace('K', '')
                self.castling = self.castling.replace('Q', '')
            if self.getTile(tile1) == 'k':
                self.castling = self.castling.replace('k', '')
                self.castling = self.castling.replace('q', '')
            # Remove castling rights if the closest rook to the king moves or dies
            if tile1 == self.castlingrooks['wq'] or tile2 == self.castlingrooks['wq']:
                self.castling.replace('Q', '')
            if tile1 == self.castlingrooks['wk'] or tile2 == self.castlingrooks['wk']:
                self.castling.replace('K', '')
            if tile1 == self.castlingrooks['bk'] or tile2 == self.castlingrooks['bk']:
                self.castling.replace('k', '')
            if tile1 == self.castlingrooks['bq'] or tile2 == self.castlingrooks['bq']:
                self.castling.replace('q', '')

            # King just castled
            if self.getTile(tile1).lower() == 'k' and tile2 in self.castlingmoves:
                self.setTile(tile2, self.getTile(tile1))
                self.setTile(tile1, 0)
                # Kingside black castle
                if tile2 > tile1 and self.active == 'b':
                    self.setTile(tile2-1, 'r')
                    self.setTile(self.castlingrooks['bk'], 0)
                # Queenside black castle
                if tile2 < tile1 and self.active == 'b':
                    self.setTile(tile2+1, 'r')
                    self.setTile(self.castlingrooks['bq'], 0)
                # Kingside white castle
                if tile2 > tile1 and self.active == 'w':
                    self.setTile(tile2-1, 'R')
                    self.setTile(self.castlingrooks['wk'], 0)
                # Queenside black castle
                if tile2 < tile1 and self.active == 'w':
                    self.setTile(tile2+1, 'R')
                    self.setTile(self.castlingrooks['wq'], 0)
            else:
                self.setTile(tile2, self.getTile(tile1))
                self.setTile(tile1, 0)

            self.active = 'w' if self.active == 'b' else 'b'
            if len([x for x in self.allLegalMoves().values() if len(x) > 0]) == 0:
                self.gamestate = 1 if self.active == 'w' else 2
            return True
        return False
    
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
    
    def notationToIndex(self, tile1):
        return self.getTile(tile1, True)
    
    def canCastle(self, tile1):
        """ Returns a list of any castling moves a given king can make
        So... this is gonna get a little weird.
        I want to preserve the ability to handle non standard sized boards
        The way I see it, here's the logic:
        - King cannot move
        - The closest rook to the king to the left and right of him I'll call his castling rooks
        - Castling rook can't have moved
        - The king, and none of the squares between him and his destination can be in check (this will be a lowkey expensive calc)
        - After castling, the king should move to ceil(abs(R-K) / 2)
        - Where R is the rook's index, and K the king's. The rook should be placed next to king either +1 if queenside castle or -1"""
        moves = []
        # Black King castling rights
        if self.getTile(tile1) == 'k':
            # Kingside rook and the king haven't moved
            if self.castling.find('k') >= 0:
                kingsquare = tile1 + math.ceil(abs(tile1 - self.castlingrooks['bk'])/2)
                self.castlingmoves.append(kingsquare)
                # Check each tile between the king and the square he wants to move to, inclusive
                valid = True
                if self.enemySeesTile(kingsquare):
                    valid = False
                for i in range(tile1+1, kingsquare):
                    if i != 0 or self.enemySeesTile(i):
                        valid = False
                if valid:
                    moves.append(kingsquare)
            # Queenside rook and the king haven't moved
            if self.castling.find('q') >= 0:
                kingsquare = tile1 - math.ceil(abs(tile1 - self.castlingrooks['bq'])/2)
                self.castlingmoves.append(kingsquare)
                valid = True
                if self.enemySeesTile(kingsquare):
                    valid = False
                for i in range(kingsquare, tile1):
                    if self.getTile(i) != 0 or self.enemySeesTile(i):
                        valid = False
                if valid:
                    moves.append(kingsquare)
                    moves.append(tile1 - math.ceil(abs(tile1 - self.castlingrooks['bq'])/2))
        
        # White King castling rights
        if self.getTile(tile1) == 'K':
            # Kingside rook and the king haven't moved
            if self.castling.find('K') >= 0:
                kingsquare = tile1 + math.ceil(abs(tile1 - self.castlingrooks['wk'])/2)
                self.castlingmoves.append(kingsquare)
                # Check each tile between the king and the square he wants to move to, inclusive
                valid = True
                if self.enemySeesTile(kingsquare):
                    valid = False
                for i in range(tile1+1, kingsquare):
                    if self.getTile(i) != 0 or self.enemySeesTile(i):
                        valid = False
                if valid:
                    moves.append(kingsquare)
            # Queenside rook and the king haven't moved
            if self.castling.find('Q') >= 0:
                # Check for checks here
                kingsquare = tile1 - math.ceil(abs(tile1 - self.castlingrooks['wq'])/2)
                self.castlingmoves.append(kingsquare)
                valid = True
                if self.enemySeesTile(kingsquare):
                    valid = False
                for i in range(kingsquare, tile1):
                    if self.getTile(i) != 0 or self.enemySeesTile(i):
                        valid = False
                if valid:
                    moves.append(kingsquare)
        return moves
    
    def enemySeesTile(self, tile1):
        """ Returns true if other player can see a given tile index """
        # At least, it would...if it didn't recurse infinitely
        return False
        self.active = 'w' if self.active == 'b' else 'b'
        moves = self.allLegalMoves(False, False)
        self.active = 'w' if self.active == 'b' else 'b'
        return True if tile1 in moves.values() else False
    
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
                # Castling
                moves.extend(self.canCastle(tile1))
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
                if i in [x for v in movelist.values() for x in v]:
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
