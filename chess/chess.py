from graphics import GraphWin, Rectangle, Point, Text
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
        # TODO: Pick prettier color scheme
        if i_rank%2 == 0:
            rect.setFill('blue') if i%2 == 0 else rect.setFill('green')
        else:
            rect.setFill('blue') if i%2 == 1 else rect.setFill('green')
        rect.draw(win)

        # TODO: Draw piece sprites using board.getTile
        piece = board.getTile(i)
        if piece != 0:
            pixWidth = i_file*tileWidth+tileWidth/2
            pixHeight = i_rank*tileHeight+tileHeight/2
            print (f"Drawing at ({pixWidth}, {pixHeight})")
            message = Text(Point(i_file*tileWidth+tileWidth/2, i_rank*tileHeight+tileHeight/2), piece)
            message.draw(win)
        
def main():
    myboard = Board()
    myboard.printBoard()
    win = GraphWin('Chess', WIDTH, HEIGHT)
    drawBoard(myboard, win)
    win.getMouse()
    print(myboard.getTile('a1'))
    print(myboard.getTile(48))
    win.close()

main()