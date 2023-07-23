import pygame
import random 

def key_handle(key, old_dir):
    if key == pygame.K_UP:
        if old_dir == "down":
            return "down"
        else:
            return "up"
    if key == pygame.K_DOWN:
        if old_dir == "up":
            return "up"
        else:
            return "down"
    if key == pygame.K_LEFT:
        if old_dir == "right":
            return "right"
        else:
            return "left"
    if key == pygame.K_RIGHT:
        if old_dir == "left":
            return "left"
        else:
            return "right"

def display_lose(score, high_score):
    screen.fill("black")
    font = pygame.font.Font('freesansbold.ttf', 32)
    loss_text = font.render('   You lose!', True, "red", "black")
    score_text = font.render(f'Final score: {score}', True, "red", "black")
    high_score_text = font.render(f'High score: {high_score}', True, "red", "black")

    score_text_box = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    loss_text_pos = (score_text_box.left, score_text_box.top - loss_text.get_rect().height)
    high_score_text_pos = (score_text_box.left, score_text_box.bottom)

    screen.blit(score_text, score_text_box)
    screen.blit(loss_text, loss_text_pos)
    screen.blit(high_score_text, high_score_text_pos)

def render_score(score):
    font = pygame.font.Font('freesansbold.ttf', 14)
    score_text = font.render(f'Score: {score}', True, "red", "black")
    score_text_box = score_text.get_rect()
    score_text_box.topright = (WIDTH - 20, 20)
    screen.blit(score_text, score_text_box)

def render_title():
    screen.fill("black")
    title_font = pygame.font.Font('freesansbold.ttf', 48)
    secondary_font = pygame.font.Font('freesansbold.ttf', 24)
    title = title_font.render('Snake!', True, "red", "black")
    message = secondary_font.render('Press enter to begin', True, "red", "black")

    title_box = title.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    message_box = message.get_rect(center=(WIDTH / 2, 0.8*HEIGHT))

    screen.blit(title, title_box)
    screen.blit(message, message_box)
    pygame.display.flip()



def should_exit(action):
    if action.type == pygame.QUIT:
        return True
    elif action.type == pygame.KEYDOWN:
        if action.key == pygame.K_q or action.key == pygame.K_ESCAPE:
            return True
    else:
        return False
    
def intersect(snake, entity, tolerance):
    x_align = (snake.head.x <= entity.x + tolerance and snake.head.x >= entity.x - tolerance) 
    y_align = (snake.head.y <= entity.y + tolerance and snake.head.y >= entity.y - tolerance) 
    
    return (x_align and y_align)

class Fruit:
    def __init__(self):
        self.x = random.randint(30, WIDTH - 30)
        self.y = random.randint(30, HEIGHT - 30)
        self.size = 20

    def draw(self):
        pygame.draw.rect(screen, "green", pygame.Rect(self.x, self.y, self.size, self.size))

class Square: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color = pygame.Color(255, 0, 0)

    def recolor(self, c):
        self.color = c
    
    def move(self, x, y):
        self.x += x
        self.y += y
        
    def draw(self):
        body = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, body)

class Snake:
    def __init__(self):
        self.head = Square(WIDTH / 2, HEIGHT / 2)
        self.direction = "right"
        self.body = []
        self.dead = False

    def move(self):
        delta = 300 * TIME_STEP
        self.body.insert(0, Square(self.head.x, self.head.y ))
        if self.direction == "up":
            self.head.y -= delta
        if self.direction == "down":
            self.head.y += delta
        if self.direction == "left":
            self.head.x -= delta
        if self.direction == "right":
            self.head.x += delta
        self.body.pop(len(self.body) - 1)

    def grow(self):
        if self.body:
            last = self.body[len(self.body) - 1]
        else:
            last = Square(self.head.x, self.head.y)

        if self.direction == "up":
            growth = Square(last.x, last.y + last.size)
        elif self.direction == "down":
            growth = Square(last.x, last.y - last.size)
        elif self.direction == "left":
            growth = Square(last.x - last.size, last.y)
        else:
            growth = Square(last.x + last.size, last.y)

        self.body.append(growth)

    def draw(self):
        self.head.draw()
        for square in self.body:
            square.draw()

    def is_dead(self):
        out_of_bounds = (self.head.x < 0 or self.head.x > WIDTH or self.head.y < 0 or self.head.y > HEIGHT)
        
        tangled = False
        for square in self.body:
            tangled = tangled or intersect(self, square, 0)
        
        self.dead = (out_of_bounds or tangled)
        return self.dead

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.running = True 
        self.lost = False
        self.high_score = 0

        self.TIME_STEP = 0
        self.SPEED_INCREASE = 0
        self.STARTING_SPEED = 1000

        self.clock = pygame.time.Clock()


    def run(self):
        while self.running:
            if not self.lost:
                snake = self.snake
                screen.fill("black")

                # poll for events
                for action in pygame.event.get():
                    if should_exit(action):
                        running = False
                    elif action.type == pygame.KEYDOWN:
                        snake.direction = key_handle(action.key, snake.direction)

                snake.move()

                self.lost = snake.is_dead()

                if intersect(snake, self.fruit, 15):
                    self.fruit = Fruit()
                    snake.grow()
                    if self.SPEED_INCREASE <= self.STARTING_SPEED / 25:
                        self.SPEED_INCREASE += 1

                # Renders
                snake.draw()
                self.fruit.draw()
                render_score(len(snake.body))
                pygame.display.flip()

                # limits FPS to 60. dt is delta time in seconds since last frame, used for framerate-independent physics.
                TIME_STEP = self.clock.tick(60) / (self.STARTING_SPEED - 25*self.SPEED_INCREASE)
            else: 
                if len(snake.body) > self.high_score:
                    self.high_score = len(snake.body)

                display_lose(len(snake.body), self.high_score)
                pygame.display.flip()

                for action in pygame.event.get():
                    if should_exit(action):
                        self.running = False
                    if action.type == pygame.KEYDOWN:
                        if action.key == pygame.K_RETURN:
                            pygame.event.clear()
                            self.snake = Snake()
                            self.fruit = Fruit()
                            self.SPEED_INCREASE = 0
                            self.lost = False


# pygame setup
pygame.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake!')


game = Game()
while True:
    render_title()
    for action in pygame.event.get():
        if should_exit(action):
            running = False
        if action.type == pygame.KEYDOWN:
            if action.key == pygame.K_RETURN:
                game.run()
