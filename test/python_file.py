import pygame
from random import randint

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
day_color = (103, 161, 253)
night_color = (10, 10, 60)

clock = pygame.time.Clock()
mw = pygame.display.set_mode((500, 500))

class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def draw(self):
        if self.fill_color:
            pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Label(Area):
    def set_text(self, text, fsize=12, text_color=BLACK):
        self.image = pygame.font.Font(None, fsize).render(text, True, text_color)

    def draw_all(self, shift_x, shift_y):
        self.draw()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

class ImageLabel(Area):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height)
        self.set_image(image_path)

    def set_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width, self.rect.height))
        except pygame.error as e:
            print(f"Не вдалося завантажити зображення: {image_path}")
            raise SystemExit(e)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

def get_background_color(level):
    cycle_level = level % 12
    if cycle_level <= 6:
        t = cycle_level / 6
    else:
        t = (12 - cycle_level) / 6
    r = int(day_color[0] * t + night_color[0] * (1 - t))
    g = int(day_color[1] * t + night_color[1] * (1 - t))
    b = int(day_color[2] * t + night_color[2] * (1 - t))
    return (r, g, b)

def is_night(level):
    return (level % 12) > 6

def get_star_count(level):
    cycle = level % 12
    if cycle <= 6:
        return 0
    t = abs(cycle - 9) / 3
    return int(10 + (1 - t) * 20)

def generate_stars(n):
    return [(randint(0, 500), randint(0, 500)) for _ in range(n)]

score = 0
level = 1
upgrade_cost = 10
click = randint(0, 3)
game_over = False

score_text = Label(10, 0, 300, 50, day_color)
score_text.set_text(f"Рахунок: {score} | Рівень: {level}", 28)

cards = []
x = 40
card_width = 100
card_height = 100
card_spacing = 20
for i in range(4):
    new_card = ImageLabel(x, 100, card_width, card_height, "buttons_PNG148.png")
    cards.append(new_card)
    x += card_width + card_spacing

upgrade_button = Label(150, 420, 200, 50, (100, 200, 100))
upgrade_button.set_text(f"Покращити ({upgrade_cost})", 30, BLACK)

move_timer = 0
move_delay = 20
stars = []

star_update_timer = 0
star_update_delay = 120

while True:
    if not game_over:
        back = get_background_color(level)
        mw.fill(back)

        if is_night(level):
            star_update_timer += 1
            if star_update_timer >= star_update_delay:
                star_count = get_star_count(level)
                stars = generate_stars(star_count)
                star_update_timer = 0

            for star in stars:
                pygame.draw.circle(mw, WHITE, star, 1)

        move_delay = 14 if is_night(level) else 20

        score_text.fill_color = back
        score_text.set_text(f"Рахунок: {score} | Рівень: {level}", 28)
        score_text.draw_all(10, 10)

        upgrade_button.draw()
        upgrade_button.set_text(f"Покращити ({upgrade_cost})", 30, BLACK)
        upgrade_button.draw_all(30, 10)

        move_timer += 1
        if move_timer >= move_delay:
            new_click = click
            while new_click == click:
                new_click = randint(0, 3)
            click = new_click
            move_timer = 0

        for i in range(4):
            if i == click:
                cards[i].set_image("Red-Click-Here-Button-PNG.png")
            else:
                cards[i].set_image("buttons_PNG148.png")
            cards[i].draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for i in range(4):
                    if cards[i].collidepoint(x, y):
                        if i == click:
                            score += 1 * level
                            new_click = click
                            while new_click == click:
                                new_click = randint(0, 3)
                            click = new_click
                            move_timer = 0
                        else:
                            score -= 1 * level

                if upgrade_button.collidepoint(x, y):
                    if score >= upgrade_cost:
                        score -= upgrade_cost
                        level += 1
                        upgrade_cost += 25

        if score <= -100:
            game_over = True

    else:
        mw.fill((20, 20, 20))
        font = pygame.font.Font(None, 48)
        text = font.render("Ви програли! Натисніть Enter, щоб вийти.", True, WHITE)
        mw.blit(text, (30, 220))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                exit()

    pygame.display.update()
    clock.tick(40)
