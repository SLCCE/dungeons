class UI():
    def __init__(self, x, y, tile_size, t):
        # what do we want x and y to represent?
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.t = t
        self.t.up()
    
    def _draw_self(self):
        self.t.color("white")
        self.t.fillcolor("white")

        self.t.goto(self.x - 4 * self.tile_size, self.y)
        self.t.begin_fill()
        self.t.seth()
        self.t.end_fill()
