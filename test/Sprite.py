from turtle import *

class Sprite(Turtle):
    def __init__(self, x, y, step=5, shape="turtle", color="black"):
        super().__init__()
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.color(color)
        self.shape(shape)
        self.step = step

    def is_collide(self, sprite):
        distance = self.distance(sprite.xcor(), sprite.ycor())
        if distance < 30:
            return True
        else:
            return False

    def move_left(self):
        self.goto(self.xcor() - self.step, self.ycor())

    def move_right(self):
        self.goto(self.xcor() + self.step, self.ycor())
