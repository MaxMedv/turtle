from turtle import *
from random import randint

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
        return distance < 30

    def move_left(self):
        self.goto(self.xcor() - self.step, self.ycor())

    def move_right(self):
        self.goto(self.xcor() + self.step, self.ycor())

class FallingPlatform(Sprite):
    def __init__(self, x, y, step=5, width=50, height=10, color="red"):
        super().__init__(x, y, step, "square", color)
        self.shapesize(stretch_wid=height // 10, stretch_len=width // 10)
        self.y_speed = 5

    def move(self):
        self.goto(self.xcor(), self.ycor() - self.y_speed)
        if self.ycor() < -250:
            self.goto(randint(-300, 300), 250)

class Bonus(Sprite):
    def __init__(self, x, y, step=5, color="yellow"):
        super().__init__(x, y, step, "circle", color)
        self.y_speed = 5

    def move(self):
        self.goto(self.xcor(), self.ycor() - self.y_speed)
        if self.ycor() < -250:
            self.goto(randint(-200, 200), 250)

def check_bonus_position(bonus, platforms, min_distance=100):
    for platform in platforms:
        if abs(bonus.xcor() - platform.xcor()) < min_distance and abs(bonus.ycor() - platform.ycor()) < min_distance:
            bonus.goto(randint(-300, 300), randint(200, 300))
            check_bonus_position(bonus, platforms)

def draw_boundaries():
    boundary = Turtle()
    boundary.speed(0)
    boundary.penup()
    boundary.goto(-350, 300)
    boundary.pendown()
    boundary.color("black")
    boundary.width(5)
    for _ in range(2):
        boundary.forward(700)
        boundary.right(90)
        boundary.forward(600)
        boundary.right(90)
    boundary.hideturtle()

player = Sprite(0, -100, 5, "turtle", "green")
player.left(90)

scr = player.getscreen()
scr.listen()

left_pressed = False
right_pressed = False

def press_left():
    global left_pressed
    left_pressed = True

def release_left():
    global left_pressed
    left_pressed = False

def press_right():
    global right_pressed
    right_pressed = True

def release_right():
    global right_pressed
    right_pressed = False

def move_player():
    if left_pressed:
        player.move_left()
    if right_pressed:
        player.move_right()
    scr.ontimer(move_player, 30)

scr.onkeypress(press_left, "Left")
scr.onkeyrelease(release_left, "Left")
scr.onkeypress(press_right, "Right")
scr.onkeyrelease(release_right, "Right")

bonus = Bonus(randint(-200, 200), 230)

platforms = []
platform_count = 10

def create_platform():
    if len(platforms) < platform_count:
        platform = FallingPlatform(randint(-300, 300), 230)
        platforms.append(platform)
    scr.ontimer(create_platform, 2000)

draw_boundaries()
create_platform()
move_player()

def exit_game():
    scr.bye()

scr.onkey(exit_game, "Return")

game_going = True

def game_loop():
    global game_going

    if not game_going:
        end = Turtle()
        end.hideturtle()
        end.penup()
        end.goto(0, 0)
        end.color("red")
        end.write("Гра закінчена", align="center", font=("Arial", 24, "bold"))
        end.goto(0, -40)
        end.color("black")
        end.write("Натисніть Enter, щоб вийти", align="center", font=("Arial", 16, "normal"))
        return

    bonus.move()
    check_bonus_position(bonus, platforms)

    if player.is_collide(bonus):
        bonus.goto(randint(-200, 200), 230)

    for platform in platforms:
        platform.move()
        if player.is_collide(platform):
            game_going = False

    if player.xcor() > 350 or player.xcor() < -350 or player.ycor() > 300 or player.ycor() < -300:
        game_going = False

    scr.ontimer(game_loop, 30)

game_loop()
scr.mainloop()
