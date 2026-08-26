import turtle
# import Character
from . import Tile
from pathlib import Path

class Board:
    def __init__(self, path):
        self.boardState = []
        self.good = (-1, -1)
        self.bad = (-1, -1)
        self.load_board(path)
        self.rows = len(self.boardState)
        self.cols = len(self.boardState[0])

        print(self.rows, self.cols)
        # self.bad_guy_turtle = turtle.Turtle()
        # self.good_guy_turtle = turtle.Turtle()
        self.square_size = 75
        self.board_width = self.cols * self.square_size
        self.board_height = self.rows * self.square_size

        # screen = turtle.Screen()
        # screen.setup(self.board_width + 200, self.board_height + 200)
        # turtle.speed(0)
        # self.draw_board()
        # self.draw_bad_guy(self.bad[0], self.bad[1])
        # self.draw_good_guy(self.good[0], self.good[1])
        # turtle.done()
    
    def __str__(self):
        # return str((self.rows, self.cols, "state:", self.boardState))
        ret = ""
        for i in range(self.rows):
            cur = ""
            for j in range(self.cols):
                cur += str(self.boardState[i][j].getStatus())
                cur += ' '
            ret += cur + '\n'
        return ret
    
    def get_tile(self, row, col):
        return self.boardState[row][col]
    
    def load_board(self, path):
        project_root = Path(__file__).resolve().parent.parent
        full_path = (project_root / path).resolve()
        with open(full_path, "r") as fin:
            # print(self.good, self.bad)
            lines = fin.readlines()
            boardState = []
            for (lineNumber, line) in enumerate(lines):
                currentRow = []
                numbers = list(map(str, line.strip().split()))
                # print(numbers)
                for (colNumber, num) in enumerate(numbers):
                    status = int(num[0])
                    if len(num) > 1:
                        entity = num[1]
                        # ex. traps
                        # if entity == "g":
                        #     self.good = (lineNumber, colNumber)
                        # if entity == "b":
                        #     self.bad = (lineNumber, colNumber)
                        t = Tile.Tile(status, entity)
                    else:
                        t = Tile.Tile(status, None)
                    currentRow.append(t)
                boardState.append(currentRow)
            # print(boardState[0][0].getStatus())
            boardState = boardState[::-1]
            self.boardState = boardState
    
    def draw_board(self):
        turtle.clear()
        for i in range(self.rows):
            for j in range(self.cols):
                # offset so board is centered
                x = -self.board_width // 2 + j * self.square_size
                y = -self.board_height // 2 + i * self.square_size
                self.draw_square(x, y, self.boardState[i][j].getStatus())
      
    def draw_square(self, x, y, fill):
        if fill:
            if fill == 1:
                turtle.fillcolor("black")
            elif fill == 2:
                turtle.fillcolor("gold")
            turtle.begin_fill()
            turtle.up()
            turtle.goto(x, y)
            turtle.down()
            for _ in range(4):
                turtle.fd(self.square_size)
                turtle.left(90)
            turtle.end_fill()
        else:
            turtle.up()
            turtle.goto(x, y)
            turtle.down()
            for _ in range(4):
                turtle.fd(self.square_size)
                turtle.left(90)
    
    def draw_bad_guy(self, row, col):
        t1 = self.bad_guy_turtle
        t1.clear()
        # compute center of grid cell
        x = -self.board_width // 2 + col * self.square_size + self.square_size // 2
        y = -self.board_height // 2 + row * self.square_size + self.square_size // 2
        t1.up()
        t1.goto(x, y - 30)  # offset so circle is centered
        t1.down()
        turtle.begin_fill()
        t1.color("red")
        t1.circle(30)
        turtle.end_fill()
        t1.color("black")

    def draw_good_guy(self, row, col):
        x = -self.board_width // 2 + col * self.square_size + self.square_size // 2
        y = -self.board_height // 2 + row * self.square_size + self.square_size // 2
        turtle.up()
        turtle.goto(x, y - 30)
        turtle.down()
        turtle.begin_fill()
        turtle.color("green")
        turtle.circle(30)
        turtle.end_fill()
        turtle.color("black")

    def clear_entities(self):
        for i in range(self.rows):
            for j in range(self.cols):
                ent = self.boardState[i][j].getEntity()
                if ent:
                    ent.t.clear()

# test = [[1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 0, 0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 1],
#         [1, 0, 0, 0, 0, 0, 0, 1],
#         [1, 0, 1, 0, 0, 0, 0, 1],
#         [1, 0, 1, 0, 0, 0, 0, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1]]

if __name__ == "__main__":
    b = Board("maps/map1.txt")
