from graphics import GraphWin, Rectangle, Point, Text, color_rgb
from board import Board

WIDTH = 800
HEIGHT = 800

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
            pixWidth = i_file*tileWidth+tileWidth/2
            pixHeight = i_rank*tileHeight+tileHeight/2
            message = Text(Point(i_file*tileWidth+tileWidth/2, i_rank*tileHeight+tileHeight/2), piece)
            message.draw(win)
        
def main():
    myboard = Board()
    myboard.printBoard()
    win = GraphWin('Chess', WIDTH, HEIGHT)
    drawBoard(myboard, win)
    win.getMouse()
    win.close()

main()