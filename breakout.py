import pygame
import random

# Initialize Pygame
pygame.init()

# Game dimensions
WIDTH, HEIGHT = 800, 600
TITLE = "Classic Breakout Game"

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)
BRICK_COLORS = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255)]

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
PADDLE_COLOR = BLUE
PADDLE_SPEED = 10

# Ball properties
BALL_DIAMETER = 15
BALL_COLOR = RED
BALL_SPEED_X, BALL_SPEED_Y = 4, -4

# Brick properties
BRICK_WIDTH, BRICK_HEIGHT = 50, 20
BRICK_ROWS, BRICK_COLUMNS = 6, 14

# Wall properties
WALL_THICKNESS = 10
WALL_COLOR = GRAY

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(self.rect.x, WALL_THICKNESS)
        self.rect.x = min(self.rect.x, WIDTH - PADDLE_WIDTH - WALL_THICKNESS)

    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_DIAMETER // 2, HEIGHT // 2 - BALL_DIAMETER // 2, BALL_DIAMETER, BALL_DIAMETER)
        self.dx = BALL_SPEED_X
        self.dy = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)

    def bounce(self, axis):
        if axis == 'x':
            self.dx = -self.dx
        elif axis == 'y':
            self.dy = -self.dy

# Brick class
class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Create bricks
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            x = WALL_THICKNESS + col * (BRICK_WIDTH + 5)
            y = WALL_THICKNESS + row * (BRICK_HEIGHT + 5)
            color = random.choice(BRICK_COLORS)
            bricks.append(Brick(x, y, color))
    return bricks

# Draw walls
def draw_walls():
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, 0, WALL_THICKNESS, HEIGHT))
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))
    pygame.draw.rect(screen, WALL_COLOR, pygame.Rect(0, 0, WIDTH, WALL_THICKNESS))

# Display score
def display_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH - 150, HEIGHT - 50))

# Show game over message
def show_game_over(score, won=False):
    font = pygame.font.Font(None, 48)
    if won:
        text = font.render("You've won the game!", True, WHITE)
    else:
        text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart", True, WHITE)
    rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, GRAY, rect)
    screen.blit(text, (WIDTH // 4 + 50, HEIGHT // 4 + 50))
    screen.blit(score_text, (WIDTH // 4 + 50, HEIGHT // 4 + 150))
    screen.blit(restart_text, (WIDTH // 4 + 50, HEIGHT // 4 + 250))
    pygame.display.flip()

# Main game loop
def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    clock = pygame.time.Clock()
    running = True
    score = 0
    game_over = False
    won = False

    while running:
        screen.fill((0, 0, 0))
        draw_walls()
        paddle.draw()
        ball.draw()
        display_score(score)

        for brick in bricks:
            brick.draw()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    main()  # Restart the game

        if game_over:
            show_game_over(score, won)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-PADDLE_SPEED)
            if keys[pygame.K_RIGHT]:
                paddle.move(PADDLE_SPEED)

            # Move ball
            ball.move()

            # Collision detection
            if ball.rect.colliderect(paddle.rect):
                ball.bounce('y')
                ball.rect.bottom = paddle.rect.top

            if ball.rect.left <= WALL_THICKNESS or ball.rect.right >= WIDTH - WALL_THICKNESS:
                ball.bounce('x')

            if ball.rect.top <= WALL_THICKNESS:
                ball.bounce('y')

            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    bricks.remove(brick)
                    ball.bounce('y')
                    score += 10

            if ball.rect.bottom >= HEIGHT:
                game_over = True

            if not bricks:
                game_over = True
                won = True

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
