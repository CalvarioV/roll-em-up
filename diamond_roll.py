import pygame
import random
import sys

# ======================================================
# 1. INITIAL SETUP
# ======================================================
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diamond Roll")

CLOCK = pygame.time.Clock()
FPS = 60

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


# ======================================================
# 2. COLORS & THEME
# ======================================================
BLACK = (10, 10, 10)
DIAMOND = (96, 210, 218)   # #60D2DA
GOLD = (212, 175, 55)
WHITE = (240, 240, 240)
RED = (200, 70, 70)
GREEN = (80, 220, 140)


# ======================================================
# 3. GAME CONFIGURATION
# ======================================================
STARTING_BALANCE = 1000
BET_STEP = 50
ROLL_DURATION_MS = 1000
WINNING_NUMBERS = {7, 11}


# ======================================================
# 4. FONTS
# ======================================================
FONT_SMALL = pygame.font.SysFont(None, 24)
FONT_MEDIUM = pygame.font.SysFont(None, 34)
FONT_LARGE = pygame.font.SysFont("Adrip1", 72)


# ======================================================
# 5. BACKGROUND IMAGE + FADE OVERLAY
# ======================================================
logo_image = pygame.image.load("Logo.png").convert_alpha()
background = pygame.transform.smoothscale(
    logo_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

OVERLAY = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
OVERLAY.fill(BLACK)

overlay_alpha = 255
FADE_SPEED = 1
FINAL_OVERLAY_ALPHA = 200   # 👈 FINAL OPACITY AFTER FADE


# ======================================================
# 6. GAME STATE VARIABLES
# ======================================================
die_1 = 1
die_2 = 1

balance = STARTING_BALANCE
current_bet = BET_STEP

wins = 0
losses = 0

result_text = "PLACE YOUR BET"
result_color = WHITE

rolling = False
roll_start_time = 0


# ======================================================
# 7. UI ELEMENTS (BUTTONS)
# ======================================================
ROLL_BUTTON = pygame.Rect(CENTER_X - 110, SCREEN_HEIGHT - 160, 220, 70)
BET_PLUS_BUTTON = pygame.Rect(CENTER_X + 140, CENTER_Y + 110, 50, 50)
BET_MINUS_BUTTON = pygame.Rect(CENTER_X - 190, CENTER_Y + 110, 50, 50)


# ======================================================
# 8. HELPER FUNCTIONS
# ======================================================
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)


def draw_button(rect, text, mouse_pos):
    hover = rect.collidepoint(mouse_pos)
    fill = DIAMOND if hover else BLACK

    pygame.draw.rect(screen, fill, rect, border_radius=12)
    pygame.draw.rect(screen, GOLD, rect, 3, border_radius=12)

    label = FONT_MEDIUM.render(text, True, GOLD)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_die(x, y, value):
    pygame.draw.rect(screen, GOLD, (x - 6, y - 6, 112, 112), border_radius=16)
    pygame.draw.rect(screen, WHITE, (x, y, 100, 100), border_radius=16)

    positions = {
        "c":  (x + 50, y + 50),
        "tl": (x + 25, y + 25),
        "tr": (x + 75, y + 25),
        "bl": (x + 25, y + 75),
        "br": (x + 75, y + 75),
        "ml": (x + 25, y + 50),
        "mr": (x + 75, y + 50),
    }

    pip_map = {
        1: ["c"],
        2: ["tl", "br"],
        3: ["tl", "c", "br"],
        4: ["tl", "tr", "bl", "br"],
        5: ["tl", "tr", "c", "bl", "br"],
        6: ["tl", "ml", "bl", "tr", "mr", "br"]
    }

    for key in pip_map[value]:
        pygame.draw.circle(screen, BLACK, positions[key], 8)


# ======================================================
# 9. MAIN GAME LOOP
# ======================================================
running = True
while running:
    CLOCK.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    # ------------------
    # EVENTS
    # ------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not rolling:
            if ROLL_BUTTON.collidepoint(event.pos) and current_bet <= balance:
                rolling = True
                roll_start_time = pygame.time.get_ticks()
                result_text = "ROLLING..."
                result_color = DIAMOND

            if BET_PLUS_BUTTON.collidepoint(event.pos):
                if current_bet + BET_STEP <= balance:
                    current_bet += BET_STEP

            if BET_MINUS_BUTTON.collidepoint(event.pos):
                if current_bet > BET_STEP:
                    current_bet -= BET_STEP

    # ------------------
    # DICE ANIMATION
    # ------------------
    if rolling:
        die_1, die_2 = roll_dice()

        if pygame.time.get_ticks() - roll_start_time >= ROLL_DURATION_MS:
            rolling = False
            total = die_1 + die_2

            if total in WINNING_NUMBERS:
                balance += current_bet
                wins += 1
                result_text = "YOU WIN!"
                result_color = GREEN
            else:
                balance -= current_bet
                losses += 1
                result_text = "YOU LOSE!"
                result_color = RED

            if balance <= 0:
                balance = 0
                result_text = "OUT OF FUNDS"

    # ------------------
    # FADE-IN EFFECT
    # ------------------
    if overlay_alpha > FINAL_OVERLAY_ALPHA:
        overlay_alpha = max(
            FINAL_OVERLAY_ALPHA,
            overlay_alpha - FADE_SPEED
        )
        OVERLAY.set_alpha(overlay_alpha)

    # ------------------
    # DRAWING
    # ------------------
    screen.blit(background, (0, 0))
    screen.blit(OVERLAY, (0, 0))

    pygame.draw.rect(
        screen,
        DIAMOND,
        (120, 110, SCREEN_WIDTH - 240, SCREEN_HEIGHT - 300),
        4,
        border_radius=20
    )

    draw_die(CENTER_X - 140, CENTER_Y - 100, die_1)
    draw_die(CENTER_X + 40, CENTER_Y - 100, die_2)

    title = FONT_LARGE.render("DIAMOND ROLL 💎", True, GOLD)
    screen.blit(title, title.get_rect(center=(CENTER_X, 60)))

    result = FONT_LARGE.render(result_text, True, result_color)
    screen.blit(result, result.get_rect(center=(CENTER_X, CENTER_Y + 70)))

    info = FONT_MEDIUM.render(
        f"Balance: ${balance}    Bet: ${current_bet}", True, WHITE
    )
    screen.blit(info, info.get_rect(center=(CENTER_X, CENTER_Y + 130)))

    stats = FONT_SMALL.render(
        f"Wins: {wins}    Losses: {losses}", True, WHITE
    )
    screen.blit(stats, stats.get_rect(center=(CENTER_X, CENTER_Y + 170)))

    draw_button(ROLL_BUTTON, "ROLL 🎲", mouse_pos)
    draw_button(BET_PLUS_BUTTON, "+", mouse_pos)
    draw_button(BET_MINUS_BUTTON, "-", mouse_pos)

    pygame.display.flip()
