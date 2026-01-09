import pygame
import random
import sys

# --------------------
# Initialize
# --------------------
pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diamond Roll 💎")

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
clock = pygame.time.Clock()

# --------------------
# Colors (Diamond Theme)
# --------------------
BLACK = (10, 10, 10)
DIAMOND = (96, 210, 218)   # #60D2DA
GOLD = (212, 175, 55)
WHITE = (240, 240, 240)
RED = (200, 70, 70)
GREEN = (80, 220, 140)

# --------------------
# Fonts
# --------------------
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 42)

# --------------------
# Game State
# --------------------
die1 = 1
die2 = 1

balance = 100
bet = 10

wins = 0
losses = 0

result_text = "PLACE YOUR BET"
result_color = WHITE

rolling = False
roll_start_time = 0
ROLL_DURATION = 600

# --------------------
# Buttons
# --------------------
def make_button(x, y, w, h):
    return pygame.Rect(x, y, w, h)

roll_button = make_button(CENTER_X - 110, HEIGHT - 160, 220, 70)
bet_up = make_button(CENTER_X + 140, CENTER_Y + 110, 50, 50)
bet_down = make_button(CENTER_X - 190, CENTER_Y + 110, 50, 50)

# --------------------
# Functions
# --------------------
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def draw_die(x, y, value):
    pygame.draw.rect(screen, GOLD, (x - 6, y - 6, 112, 112), border_radius=16)
    pygame.draw.rect(screen, WHITE, (x, y, 100, 100), border_radius=16)

    c = (x + 50, y + 50)
    tl = (x + 25, y + 25)
    tr = (x + 75, y + 25)
    bl = (x + 25, y + 75)
    br = (x + 75, y + 75)
    ml = (x + 25, y + 50)
    mr = (x + 75, y + 50)

    pips = {
        1: [c],
        2: [tl, br],
        3: [tl, c, br],
        4: [tl, tr, bl, br],
        5: [tl, tr, c, bl, br],
        6: [tl, ml, bl, tr, mr, br],
    }

    for pip in pips[value]:
        pygame.draw.circle(screen, BLACK, pip, 8)

def draw_button(rect, text, mouse):
    hover = rect.collidepoint(mouse)
    color = DIAMOND if hover else BLACK

    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, GOLD, rect, 3, border_radius=12)

    label = button_font.render(text, True, GOLD)
    screen.blit(label, label.get_rect(center=rect.center))

# --------------------
# Game Loop
# --------------------
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)
    mouse = pygame.mouse.get_pos()

    # ---- Events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not rolling:
            if roll_button.collidepoint(event.pos) and bet > 0 and bet <= balance:
                rolling = True
                roll_start_time = pygame.time.get_ticks()
                result_text = "ROLLING..."
                result_color = DIAMOND

            if bet_up.collidepoint(event.pos) and bet + 10 <= balance:
                bet += 10

            if bet_down.collidepoint(event.pos) and bet > 10:
                bet -= 10

    # ---- Dice Animation ----
    if rolling:
        die1, die2 = roll_dice()

        if pygame.time.get_ticks() - roll_start_time >= ROLL_DURATION:
            rolling = False
            total = die1 + die2

            if total in (1, 5, 7, 11):
                result_text = "SI KEMA CUH!!!"
                result_color = GREEN
                balance += bet
                wins += 1
            else:
                result_text = "NO KEMA CUH!!!"
                result_color = RED
                balance -= bet
                losses += 1

            if balance <= 0:
                balance = 0
                result_text = "NO MORE FERIA!!"

    # ---- Panel ----
    pygame.draw.rect(screen, DIAMOND, (120, 110, WIDTH - 240, HEIGHT - 300), 4, border_radius=20)

    # ---- Dice ----
    dice_y = CENTER_Y - 100
    spacing = 140
    draw_die(CENTER_X - spacing, dice_y, die1)
    draw_die(CENTER_X + spacing - 100, dice_y, die2)

    # ---- Text ----
    title = big_font.render("DIAMOND ROLL 💎", True, GOLD)
    screen.blit(title, title.get_rect(center=(CENTER_X, 60)))

    result = big_font.render(result_text, True, result_color)
    screen.blit(result, result.get_rect(center=(CENTER_X, CENTER_Y + 70)))

    info = font.render(f"Balance: ${balance}    Bet: ${bet}", True, WHITE)
    screen.blit(info, info.get_rect(center=(CENTER_X, CENTER_Y + 130)))

    stats = font.render(f"Wins: {wins}    Losses: {losses}", True, WHITE)
    screen.blit(stats, stats.get_rect(center=(CENTER_X, CENTER_Y + 170)))

    # ---- Buttons ----
    draw_button(roll_button, "ROLL 🎲", mouse)
    draw_button(bet_up, "+", mouse)
    draw_button(bet_down, "-", mouse)

    pygame.display.flip()
