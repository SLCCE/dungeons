class Gate: 
    def __init__(self, color, x, y, size, t, offset):
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.t = t
        self.t.hideturtle()
        self.offset = offset
        self._draw_self()

    def _draw_self(self): 
        #drawing
        self.t.up()
        self.t.goto(self.y * self.size - self.offset[0], self.x * self.size - self.offset[1])
        self.t.down()
        self.t.pensize(10)
        self.t.pencolor(self.color)
        self.t.left(45)
        self.t.fd(self.size * (2 ** 0.5))

    def getColor(self):
        return self.color
