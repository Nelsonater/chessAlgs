from graphics import GraphWin, Rectangle, Point, Text, color_rgb, Image, Circle
from bot_random import ChessRandom
from board import Board
import time

WIDTH = 600
HEIGHT = 600

def drawBoard(board, win):
    tileWidth = WIDTH/board.boardWidth
    tileHeight = HEIGHT/board.boardWidth

    for i in range(board.boardWidth*board.boardWidth):
        # Calc rank/file using top left as 0, 0
        i_file = i % board.boardWidth
        i_rank = int(i/board.boardWidth)

        rect = Rectangle(Point(i_file*tileWidth, i_rank*tileHeight), Point((i_file+1)*tileWidth, (i_rank+1)*tileHeight))
        if i_rank%2 == 0:
            rect.setFill(color_rgb(241, 217, 181)) if i%2 == 0 else rect.setFill(color_rgb(181, 136, 99))
        else:
            rect.setFill(color_rgb(181, 136, 99)) if i%2 == 0 else rect.setFill(color_rgb(241, 217, 181))
        rect.draw(win)

        piece = board.getTile(i)
        if piece != 0:
            piece_sprite = None
            if piece == 'p':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/bp.png')
            elif piece == 'P':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/wp.png')
            elif piece == 'r':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/br.png')
            elif piece == 'R':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/wr.png')
            elif piece == 'n':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/bn.png')
            elif piece == 'N':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/wn.png')
            elif piece == 'b':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/bb.png')
            elif piece == 'B':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/wb.png')
            elif piece == 'k':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/bk.png')
            elif piece == 'K':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/wk.png')
            elif piece == 'q':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/bq.png')
            elif piece == 'Q':
                piece_sprite = Image(tileToCoord(board, i), 'chess/img/wq.png')
            else:
                message = Text(tileToCoord(board, i), piece)
                message.draw(win)
            piece_sprite.draw(win)

def drawLegalMoves(board, win, tile1):
    legalmoves = board.getLegalMoves(tile1)

    tileWidth = WIDTH/board.boardWidth
    tileHeight = HEIGHT/board.boardWidth

    for move in legalmoves:
        circ = Circle(tileToCoord(board, move), min(tileWidth, tileHeight)/4)
        circ.setFill('gray')
        circ.draw(win)

def tileToCoord(board, tile1):
    tileWidth = WIDTH/board.boardWidth
    tileHeight = HEIGHT/board.boardWidth
    tile_file = tile1 % board.boardWidth
    tile_rank = int(tile1/board.boardWidth)
    return Point(tile_file*tileWidth+tileWidth/2, tile_rank*tileHeight+tileHeight/2)

def getNextMove(board, win):
    while True:
        p = win.getMouse()
        mouseFile = int(p.getX() / (WIDTH/board.boardWidth))
        mouseRank = int(p.getY() / (HEIGHT/board.boardWidth))
        tile1 = mouseRank*board.boardWidth + mouseFile
        if board.getTile(tile1) != 0 and len(board.getLegalMoves(tile1)) > 0:
            drawLegalMoves(board, win, tile1)
            break
    p = win.getMouse()
    mouseFile = int(p.getX() / (WIDTH/board.boardWidth))
    mouseRank = int(p.getY() / (HEIGHT/board.boardWidth))
    tile2 = mouseRank*board.boardWidth + mouseFile
    board.movePiece(tile1, tile2)
    # print (f"({p.getX()}, {p.getY()}) -> ({mouseFile}, {mouseRank})")

def drawCheckmate(board, win):
    message = Text(Point(WIDTH/2, HEIGHT/2), "Checkmate!")
    message.draw(win)
    win.getMouse()
        
def main():
    myboard = Board()
    comp = ChessRandom(myboard, 'b')
    print(myboard.outputFEN())
    win = GraphWin('Chess', WIDTH, HEIGHT)
    while not win.isClosed():
        drawBoard(myboard, win)
        if myboard.isCheckmate:
            print("Checkmate!")
            drawCheckmate(myboard, win)
        if myboard.active == 'w':
            getNextMove(myboard, win)
        else:
            comp.nextMove()
        # print(myboard.allLegalMoves(True))
        win.update()
        time.sleep(.1)
    win.close()

if __name__ == "__main__":
    main()