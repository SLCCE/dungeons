class Egg: 
    def __init__(self, x, y, tile_size, t, offset): 
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.t = t
        self.t.hideturtle()
        self.offset = offset
        self.color = "#59d1b1"
        self._draw_self()
    
    def draw_oval(self, radius_a, radius_b):
        """
        Draws an oval using four arcs.
        radius_a is half the width, radius_b is half the height.
        """
        for _ in range(2):
            self.t.circle(radius_a, 90)
            self.t.circle(radius_b, 90)
    
    def _draw_self(self):
        self.t.up()
        self.t.clear()
        xDestination = self.y * self.tile_size - self.offset[0] + self.tile_size // 2 + self.tile_size // 8
        yDestination = self.x * self.tile_size - self.offset[1] + self.tile_size // 4 - self.tile_size // 8
        self.t.goto(xDestination, yDestination)
        self.t.pendown()
        self.t.fillcolor(self.color)
        self.t.begin_fill()
        self.draw_oval(self.tile_size * 0.25, self.tile_size * 0.5)
        self.t.end_fill()
        self.t.penup()
    
    def clear(self):
        self.t.clear()
