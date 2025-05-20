from random import randint
from time import sleep
from turtle import *

from Sprite import Sprite
from test.FallingPlatform import FallingPlatform


def dist_chek(self, enother_sprite):
    return self.distance(enother_sprite) > 50


player = Sprite(0, - 100, 5, "turtle", "green")
player.left(90)

scr = player.getscreen()
scr.listen()

scr.onkey(player.move_left, "Left")
scr.onkey(player.move_right, "Right")

bonuse = Sprite(randint(-200, 200), 230, 5, "circle", "yellow")
bonuse.setheading(-90)
dist_chek_going = True
while dist_chek_going:
    platform1 = FallingPlatform(randint(-300, 300), 230, 5)
    platform1.setheading(-90)

    platform2 = FallingPlatform(randint(-300, 300), randint(200, 300), 5)
    platform2.setheading(-90)

    platform3 = FallingPlatform(randint(-300, 300), randint(200, 300), 5)
    platform3.setheading(-90)

    platform4 = FallingPlatform(randint(-300, 300), randint(200, 300), 5)
    platform4.setheading(-90)

    platform5 = FallingPlatform(randint(-300, 300), randint(200, 300), 5)
    platform5.setheading(-90)

    if (dist_chek(platform1, platform2) == True
            and dist_chek(platform1, platform3) == True
            and dist_chek(platform1, platform4) == True
            and dist_chek(platform1, platform5) == True
            and dist_chek(platform2, platform3) == True
            and dist_chek(platform2, platform4) == True
            and dist_chek(platform2, platform5) == True
            and dist_chek(platform3, platform4) == True
            and dist_chek(platform3, platform5) == True
            and dist_chek(platform4, platform5)):
        break

game_going = True
while game_going:
    bonuse.forward(1)
    platform1.forward(randint(1, 5))
    platform2.forward(randint(1, 5))
    platform3.forward(randint(1, 5))
    platform4.forward(randint(1, 5))
    platform5.forward(randint(1, 5))
    if player.is_collide(bonuse):
        print("player has collide!")
        bonuse.goto(randint(-200, 200), 230)
    if player.is_collide(platform1) or player.is_collide(platform2) or player.is_collide(
            platform3) or player.is_collide(platform4) or player.is_collide(platform5):
        break
    if player.xcor() > 300 or player.xcor() < -300:
        break
