from graphics import GraphWin, Rectangle, Point, Text, color_rgb, Image
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

        # TODO: Draw piece sprites using board.getTile
        piece = board.getTile(i)
        if piece != 0:
            if piece == 'p' or piece == 'P':
                pawn = Image(Point(i_file*tileWidth+tileWidth/2, i_rank*tileHeight+tileHeight/2), 'chess/img/pawn.png')
                pawn.draw(win)
            else:
                message = Text(Point(i_file*tileWidth+tileWidth/2, i_rank*tileHeight+tileHeight/2), piece)
                message.draw(win)

def getNextMove(board, win):
    while True:
        p = win.getMouse()
        mouseFile = int(p.getX() / (WIDTH/board.boardWidth))
        mouseRank = int(p.getY() / (HEIGHT/board.boardWidth))
        tile1 = mouseRank*board.boardWidth + mouseFile
        if board.getTile(tile1) != 0:
            break
    p = win.getMouse()
    mouseFile = int(p.getX() / (WIDTH/board.boardWidth))
    mouseRank = int(p.getY() / (HEIGHT/board.boardWidth))
    tile2 = mouseRank*board.boardWidth + mouseFile
    board.movePiece(tile1, tile2)
    # print (f"({p.getX()}, {p.getY()}) -> ({mouseFile}, {mouseRank})")
        
def main():
    myboard = Board()
    myboard.printBoard()
    win = GraphWin('Chess', WIDTH, HEIGHT)
    while not win.isClosed():
        drawBoard(myboard, win)
        getNextMove(myboard, win)
        win.update()
        time.sleep(.1)
    win.close()

main()