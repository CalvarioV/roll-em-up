import pygame
import random
import sys

# ======================================================
# 1. INITIAL SETUP
# ======================================================
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diamond Roll by Calvario")

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
# 3. GAME CONFIGURATION/ CONSTANTS
# ======================================================
STARTING_BALANCE = 1000
BET_STEP = 50
ROLL_DURATION_MS = 2000
WINNING_NUMBERS = {7, 11}


# ======================================================
# 4. ASSET PATHS
# ======================================================
FONT_PATH = "assets/fonts/Dune_Rise.ttf"
FONT_PATH_TITLE = "assets/fonts/adrip1.ttf"
LOGO_PATH = "assets/images/Logo.png"
MUSIC_PATH = "assets/audio/bg_music.mp3"
ROLL_SFX_PATH = "assets/audio/roll.wav"


# ======================================================
# 5. FONTS + BACKGROUND IMAGE + FADE OVERLAY
# ======================================================
FONT_SMALL = pygame.font.Font(FONT_PATH, 18)
FONT_MEDIUM = pygame.font.Font(FONT_PATH, 26)
FONT_LARGE = pygame.font.Font(FONT_PATH, 36)
FONT_LARGE_TITLE = pygame.font.Font(FONT_PATH_TITLE, 72)

logo_image = pygame.image.load(LOGO_PATH).convert_alpha()
background = pygame.transform.smoothscale(
    logo_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

OVERLAY = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
OVERLAY.fill(BLACK)

overlay_alpha = 255
FADE_SPEED = 1
FINAL_OVERLAY_ALPHA = 200   # 👈 FINAL OPACITY AFTER FADE

# ======================================================
# 5.5 BACKGROUND MUSIC (LOOPING)
# ======================================================
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.65) # 0.0 to 1.0
pygame.mixer.music.play(-1)          # -1 = loop forever

# ======================================================
# 5.5.2 SOUND EFFECTS
# ======================================================
ROLL_SFX = pygame.mixer.Sound(ROLL_SFX_PATH)
ROLL_SFX.set_volume(0.7)  # 0.0 to 1.0

# ======================================================
# 6. GAME STATE VARIABLES
# ======================================================
balance = STARTING_BALANCE
current_bet = BET_STEP
wins = 0
losses = 0

rolling = False
roll_start_time = 0
die_1 = 1
die_2 = 1


result_text = ""
result_color = WHITE
game_over = False



# ======================================================
# 7. UI ELEMENTS (BUTTONS)
# ======================================================
ROLL_BUTTON = pygame.Rect(CENTER_X - 110, SCREEN_HEIGHT - 160, 220, 70)
BET_PLUS_BUTTON = pygame.Rect(CENTER_X + 190, CENTER_Y + 110, 50, 50)
BET_MINUS_BUTTON = pygame.Rect(CENTER_X - 240, CENTER_Y + 110, 50, 50)
PLAY_AGAIN_BUTTON = pygame.Rect(CENTER_X - 140, CENTER_Y + 230, 280, 70)


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
    pygame.draw.rect(screen, BLACK, (x, y, 100, 100), border_radius=16)

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
        pygame.draw.circle(screen, DIAMOND, positions[key], 8)


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
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not rolling and not game_over:
            if ROLL_BUTTON.collidepoint(event.pos) and current_bet <= balance:
                rolling = True
                roll_start_time = pygame.time.get_ticks()
                result_text = "ROLLING..."
                result_color = DIAMOND
                ROLL_SFX.play()

            if BET_PLUS_BUTTON.collidepoint(event.pos):
                if current_bet + BET_STEP <= balance:
                    current_bet += BET_STEP

            if BET_MINUS_BUTTON.collidepoint(event.pos):
                if current_bet > BET_STEP:
                    current_bet -= BET_STEP

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if PLAY_AGAIN_BUTTON.collidepoint(event.pos):
                balance = STARTING_BALANCE
                current_bet = BET_STEP
                wins = 0
                losses = 0
                die_1 = 1
                die_2 = 1
                result_text = ""
                result_color = WHITE
                game_over = False


    # ------------------
    # DICE ANIMATION
    # ------------------
    if rolling:
        die_1, die_2 = roll_dice()

        if pygame.time.get_ticks() - roll_start_time >= ROLL_DURATION_MS:
            rolling = False
            total = die_1 + die_2

            # ------------------
            # SNAKE EYES BONUS
            # ------------------
            if die_1 == 1 and die_2 == 1:
                balance += current_bet * 10
                wins += 1
                result_text = "SNAKE EYES! 10x WIN!"
                result_color = DIAMOND

            # ------------------
            # REGULAR WIN
            # ------------------
            elif total in WINNING_NUMBERS:
                balance += current_bet
                wins += 1
                result_text = "YOU WIN!"
                result_color = GREEN

            # ------------------
            # LOSS
            # ------------------
            else:
                balance -= current_bet
                losses += 1
                result_text = "YOU LOSE!"
                result_color = RED

            # ------------------
            # OUT OF FUNDS CHECK
            # ------------------
            if balance <= 0:
                balance = 0
                result_text = "OUT OF FUNDS"
                result_color = RED
                game_over = True

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

    title = FONT_LARGE_TITLE.render("DIAMOND ROLL", True, GOLD)
    screen.blit(title, title.get_rect(center=(CENTER_X, 60)))

    result = FONT_LARGE.render(result_text, True, result_color)
    screen.blit(result, result.get_rect(center=(CENTER_X, CENTER_Y + 70)))

    info = FONT_SMALL.render(
        f"Balance: ${balance}    Bet: ${current_bet}", True, WHITE
    )
    screen.blit(info, info.get_rect(center=(CENTER_X, CENTER_Y + 130)))

    stats = FONT_SMALL.render(
        f"Wins: {wins}    Losses: {losses}", True, WHITE
    )
    screen.blit(stats, stats.get_rect(center=(CENTER_X, CENTER_Y + 170)))

    if not game_over:
        draw_button(ROLL_BUTTON, "ROLL", mouse_pos)
        draw_button(BET_PLUS_BUTTON, "+", mouse_pos)
        draw_button(BET_MINUS_BUTTON, "-", mouse_pos)
    else:
        draw_button(PLAY_AGAIN_BUTTON, "PLAY AGAIN", mouse_pos)

    pygame.display.flip()
