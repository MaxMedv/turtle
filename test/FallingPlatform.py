from test.Sprite import Sprite


class FallingPlatform(Sprite):
    def __init__(self, x, y, step=5, width=50, height=10, color="red"):
        super().__init__(x, y, step, "square", color)
        self.shapesize(stretch_wid=height // 10, stretch_len=width // 10)
        self.y_speed = 5