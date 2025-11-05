import pygame
import random
import sys
import math

#Initialization
pygame.init()
pygame.font.init()
pygame.mixer.init()

GAME_TITLE = "Pong Revilla"

#fullscreen
try:
    infoObject = pygame.display.Info()
    SCREEN_WIDTH = infoObject.current_w
    SCREEN_HEIGHT = infoObject.current_h
except pygame.error:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (50, 200, 50)
RED = (200, 50, 50)     
YELLOW = (255, 255, 0)#highlit

# Game Objects
PADDLE_WIDTH = 25
PADDLE_HEIGHT = 100
BALL_SIZE = 30
PADDLE_SPEED = 12
WINNING_SCORE = 5

# Difficulty levels
DIFFICULTIES = {
    "Easy": 4,
    "Medium": 6,
    "Hard": 8
}

# Progressive Speed Constants
SPEED_INCREASE_INTERVAL = 1440 # Every 1440 frames = 10 seconds at 144 FPS
SPEED_INCREASE_AMOUNT = 0.6  #ball speed 

# Avatar 
AVATAR_STYLES = [
    ("Lebron James", (255, 69, 0), "LJ"),      # Red-Orange
    ("Martha stewart", (0, 100, 255), "MS"),    # Blue
    ("george floyd", YELLOW, "GF"),        # Yellow
    ("Bhuhstt", (0, 128, 0), "B"),       # Green
    ("Micahel Jordan", (75, 0, 130), "MJ"),     # Indigo/Purple
]
AVATAR_OPTIONS = len(AVATAR_STYLES)

# Asset
game_assets = {
    'fonts': {},
    'images': {},
    'sounds': {
        # Initialize placeholders
        'paddle_hit': None,
        'wall_hit': None,
        'score': None,
        'victory': None,
    }
}

def create_background_asset():
    """dark, textured background surface beacause i cant make image asset fucking work"""
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_surface.fill(BLACK)
    
    for x in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(bg_surface, DARK_GREY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 50):
        pygame.draw.line(bg_surface, DARK_GREY, (0, y), (SCREEN_WIDTH, y))
        
    game_assets['images']['background'] = bg_surface

def load_assets():
    """Loads all game assets into the containers."""
    print("Loading assets...")
    # Fonts 
    fonts = ['Press Start 2P', 'Consolas', 'Courier New', 'Monaco']
    for font_name in fonts:
        if font_name.lower() in [f.lower() for f in pygame.font.get_fonts()]:
            game_assets['fonts']['title'] = pygame.font.SysFont(font_name, 40) 
            game_assets['fonts']['score'] = pygame.font.SysFont(font_name, 32)
            game_assets['fonts']['menu'] = pygame.font.SysFont(font_name, 24)
            game_assets['fonts']['input'] = pygame.font.SysFont(font_name, 20)
            game_assets['fonts']['small'] = pygame.font.SysFont(font_name, 16)
            print(f"Using font: {font_name}")
            break
    else:
        # Fallback
        print("Using fallback monospace font")
        game_assets['fonts']['title'] = pygame.font.SysFont('monospace', 40, bold=True)
        game_assets['fonts']['score'] = pygame.font.SysFont('monospace', 32, bold=True)
        game_assets['fonts']['menu'] = pygame.font.SysFont('monospace', 24)
        game_assets['fonts']['input'] = pygame.font.SysFont('monospace', 20)
        game_assets['fonts']['small'] = pygame.font.SysFont('monospace', 16)
    
    #  background asset
    create_background_asset()

    try:
        #  synthesized sound
        sample_rate = 44100
        duration = 0.1  # 100ms
        samples = int(duration * sample_rate)
        
        #  paddle hit sound 
        paddle_buffer = bytearray()
        for i in range(samples):
            value = int(127 * math.sin(2 * 3.14 * 880 * i / sample_rate))  # 880 Hz tone
            paddle_buffer.extend([abs(value), abs(value)])  # Stereo sound
        game_assets['sounds']['paddle_hit'] = pygame.mixer.Sound(buffer=bytes(paddle_buffer))
        
        # wall hit sound
        wall_buffer = bytearray()
        for i in range(samples):
            value = int(127 * math.sin(2 * 3.14 * 440 * i / sample_rate))  # 440 Hz tone
            wall_buffer.extend([abs(value), abs(value)])  # Stereo sound
        game_assets['sounds']['wall_hit'] = pygame.mixer.Sound(buffer=bytes(wall_buffer))
        
        # score sound
        score_buffer = bytearray()
        for i in range(samples):
            freq = 440 + (i * 440 / samples)  
            value = int(127 * math.sin(2 * 3.14 * freq * i / sample_rate))
            score_buffer.extend([abs(value), abs(value)])  # Stereo sound
        game_assets['sounds']['score'] = pygame.mixer.Sound(buffer=bytes(score_buffer))
        
        #  victory sound 
        victory_duration = 0.5  
        victory_samples = int(victory_duration * sample_rate)
        victory_buffer = bytearray()
        
        #  victory sound 
        for i in range(victory_samples):
            time = i / sample_rate
         
            freq1 = 440 + (i * 440 / victory_samples)
      
            freq2 = 660 + (i * 220 / victory_samples)
         
            value = int(127 * 0.6 * math.sin(2 * math.pi * freq1 * time) +
                       127 * 0.4 * math.sin(2 * math.pi * freq2 * time))
            victory_buffer.extend([abs(value), abs(value)])
        
        game_assets['sounds']['victory'] = pygame.mixer.Sound(buffer=bytes(victory_buffer))
        
        # volumes
        game_assets['sounds']['paddle_hit'].set_volume(0.3)
        game_assets['sounds']['wall_hit'].set_volume(0.3)
        game_assets['sounds']['score'].set_volume(0.4)
        game_assets['sounds']['victory'].set_volume(0.5)  
        
    except pygame.error as e:
        print(f"Warning: Failed to create placeholder sound buffers. Sound will be disabled. Error: {e}")


def play_sound(sound_name):
    """Plays a sound from the asset container if it exists and is loaded."""
    if sound_name in game_assets['sounds'] and game_assets['sounds'][sound_name] is not None:
        game_assets['sounds'][sound_name].play() 
    else:
        pass

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()


load_assets()


pygame.mouse.set_visible(True)

game_state = "MAIN_MENU" 
current_difficulty = "Medium"
progressive_speed_enabled = False 

ball_speed_base = DIFFICULTIES[current_difficulty] 
speed_increase_counter = 0 

#Menu Selection Variables
MAIN_MENU_OPTIONS = 6 
main_menu_selection = 0 

GAME_OVER_OPTIONS = 2
game_over_selection = 0 

PAUSE_MENU_OPTIONS = 3
pause_menu_selection = 0


player1_name = ""
player2_name = ""
current_input_text = ""
active_input_player = 1 
input_prompt = "Player 1, enter your name and press SPACE to confirm:"

player1_avatar_index = 0
player2_avatar_index = 1
avatar_select_selection = 0
active_select_player = 1 
avatar_prompt_message = "" 

# Objects
player1 = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

#Variables
player1_score = 0
player2_score = 0
player1_speed = 0
player2_speed = 0
#random direction
ball_speed_x = ball_speed_base * random.choice((1, -1))
ball_speed_y = ball_speed_base * random.choice((1, -1))
winner_text = ""



def draw_text(text, font, color, surface, x, y, center=False):

    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def highlight_button(rect, surface, is_selected):
    """highlight box """
    if is_selected:
        pygame.draw.rect(surface, YELLOW, rect.inflate(10, 8), 2, 5) # Draw yellow border

def reset_ball():
    """Resets the ball"""
    global ball_speed_x, ball_speed_y, ball_speed_base, speed_increase_counter
    
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Reset speedcounter
    speed_increase_counter = 0 
    
    # new speeds based on the current base speed
    ball_speed_y = ball_speed_base * random.choice((1, -1))
    ball_speed_x = ball_speed_base * random.choice((1, -1))

def reset_game():
    global player1_score, player2_score, winner_text
    global player1_speed, player2_speed
    
    player1_score = 0
    player2_score = 0
    winner_text = ""
    player1_speed = 0
    player2_speed = 0
    player1.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    player2.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    
    reset_ball()


def draw_main_menu():
    """ main menu screen"""
#background asset
    if 'background' in game_assets['images']:
        screen.blit(game_assets['images']['background'], (0, 0))
    else:
        screen.fill(BLACK) 
    
    title_font = game_assets['fonts']['title']
    menu_font = game_assets['fonts']['menu']
    small_font = game_assets['fonts']['small']
    
    draw_text(GAME_TITLE, title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 1 // 10, center=True)
    
    #Start Game Button
    start_rect = draw_text("Start Game", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 10, center=True)
    highlight_button(start_rect, screen, main_menu_selection == 0)
    
    #Difficulty 
    draw_text("Select Base Difficulty:", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 10 + 20, center=True)
    
    # 1 Easy
    easy_color = GREY if current_difficulty != "Easy" else GREEN
    easy_rect = draw_text("Easy", menu_font, easy_color, screen, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT * 4 // 10 + 70, center=True)
    highlight_button(easy_rect, screen, main_menu_selection == 1)
    
    # 2. Medium
    medium_color = GREY if current_difficulty != "Medium" else GREEN
    medium_rect = draw_text("Medium", menu_font, medium_color, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 4 // 10 + 70, center=True)
    highlight_button(medium_rect, screen, main_menu_selection == 2)
    
    # 3 Hard
    hard_color = GREY if current_difficulty != "Hard" else GREEN
    hard_rect = draw_text("Hard", menu_font, hard_color, screen, SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT * 4 // 10 + 70, center=True)
    highlight_button(hard_rect, screen, main_menu_selection == 3)
    
    # 4. Progressive Speed 
    speed_text = f"Progressive Speed: {'ON' if progressive_speed_enabled else 'OFF'}"
    speed_color = GREEN if progressive_speed_enabled else RED
    speed_rect = draw_text(speed_text, menu_font, speed_color, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 5 // 10 + 120, center=True)
    highlight_button(speed_rect, screen, main_menu_selection == 4)
    
    # 5. Quit Button
    quit_rect = draw_text("Quit (Esc)", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 9 // 10, center=True)
    highlight_button(quit_rect, screen, main_menu_selection == 5)

    # Controls guide
    controls_y = SCREEN_HEIGHT * 6 // 10 + 90
    draw_text("CONTROLS:", menu_font, WHITE, screen, SCREEN_WIDTH // 2, controls_y, center=True)

    draw_text("Player 1 (Left Paddle): W (Up), S (Down)", small_font, GREY, screen, SCREEN_WIDTH // 2, controls_y + 40, center=True)
    draw_text("Player 2 (Right Paddle): UP ARROW, DOWN ARROW", small_font, GREY, screen, SCREEN_WIDTH // 2, controls_y + 65, center=True)
    draw_text("Pause/Resume: P key", small_font, GREY, screen, SCREEN_WIDTH // 2, controls_y + 90, center=True)
    draw_text("Menu Selection: W/S (Up/Down), SPACE/Click", small_font, GREY, screen, SCREEN_WIDTH // 2, controls_y + 115, center=True)

    return start_rect, easy_rect, medium_rect, hard_rect, speed_rect, quit_rect

def draw_get_names_screen():
    """Draws the screen for player name input."""
    if 'background' in game_assets['images']:
        screen.blit(game_assets['images']['background'], (0, 0))
    else:
        screen.fill(BLACK) 
        
    menu_font = game_assets['fonts']['menu']
    
    draw_text(input_prompt, menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
    
    input_rect = draw_text(current_input_text, menu_font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    pygame.draw.rect(screen, GREEN, input_rect.inflate(10, 8), 2, 5)

    if int(pygame.time.get_ticks() / 500) % 2 == 0:
        draw_text("|", menu_font, GREEN, screen, input_rect.right + 5, SCREEN_HEIGHT // 2, center=False)

def draw_avatar_select_screen():
    """ avatar selection screen."""
    global avatar_prompt_message
    if 'background' in game_assets['images']:
        screen.blit(game_assets['images']['background'], (0, 0))
    else:
        screen.fill(BLACK)
    
    title_font = game_assets['fonts']['title']
    menu_font = game_assets['fonts']['menu']
    small_font = game_assets['fonts']['small']

    # Title
    p_name = player1_name if active_select_player == 1 else player2_name
    draw_text(f"{p_name}, Select Your Y/N:", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 1 // 10, center=True)
    
    # Instructions
    prompt_color = RED if avatar_prompt_message else GREY
    prompt_text = avatar_prompt_message if avatar_prompt_message else "Use A/D to cycle, SPACE to confirm."
    draw_text(prompt_text, small_font, prompt_color, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 10, center=True)


    # Avatars
    AVATAR_RADIUS = 50
    AVATAR_FONT = game_assets['fonts']['title']
    
    # starting X position to center the group of avatars
    AVATAR_GAP = 300
    group_width = AVATAR_OPTIONS * AVATAR_GAP
    start_x = SCREEN_WIDTH // 2 - group_width // 2 + AVATAR_GAP // 2 # Center point of the first avatar

    for i in range(AVATAR_OPTIONS):
        name, color, initial = AVATAR_STYLES[i]
        
        #position for each avatar
        center_x = start_x + (i * AVATAR_GAP)
        center_y = SCREEN_HEIGHT // 2
        center_pos = (center_x, center_y)

        # circle
        pygame.draw.circle(screen, color, center_pos, AVATAR_RADIUS)
        
        # initial
        draw_text(initial, AVATAR_FONT, WHITE, screen, center_x, center_y, center=True)
        
        #name
        draw_text(name, menu_font, WHITE, screen, center_x, center_y + AVATAR_RADIUS + 20, center=True)
        
        rect = pygame.Rect(center_x - AVATAR_RADIUS, center_y - AVATAR_RADIUS, AVATAR_RADIUS * 2, AVATAR_RADIUS * 2)
        
        # 1. Highlight selection
        if i == avatar_select_selection:
            pygame.draw.rect(screen, YELLOW, rect.inflate(10, 10), 4, 10)
        
        # 2. Indicate taken avatar
        if active_select_player == 2 and i == player1_avatar_index:
            #   border when taken 
            pygame.draw.rect(screen, RED, rect.inflate(10, 10), 4, 10) # Red border
            draw_text("TAKEN", small_font, RED, screen, center_x, center_y + AVATAR_RADIUS - 10, center=True)


    # Show current confirmed selections
    p1_name_text = f"P1: {player1_name} ({AVATAR_STYLES[player1_avatar_index][0]})"
    draw_text(p1_name_text, menu_font, AVATAR_STYLES[player1_avatar_index][1], screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT * 9 // 10, center=True)
    
    # Only show P2's name and confirmed avatar if it's confirmed
    p2_avatar_name = AVATAR_STYLES[player2_avatar_index][0] if active_select_player == 2 else "..."
    p2_name_display = player2_name if player2_name else "..."
    p2_name_text = f"P2: {p2_name_display} ({p2_avatar_name})"
    draw_text(p2_name_text, menu_font, AVATAR_STYLES[player2_avatar_index][1], screen, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT * 9 // 10, center=True)

def draw_pause_menu():
    """pause menu"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    screen.blit(overlay, (0, 0))
    
    title_font = game_assets['fonts']['title']
    menu_font = game_assets['fonts']['menu']
    
    #Title
    draw_text("Paused", title_font, WHITE, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, center=True)
    
    # 0. Resume
    resume_rect = draw_text("Resume (P)", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, center=True)
    highlight_button(resume_rect, screen, pause_menu_selection == 0)
    
    # 1. Restart
    restart_rect = draw_text("Restart Game", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 0, center=True)
    highlight_button(restart_rect, screen, pause_menu_selection == 1)

    # 2. Main Menu
    menu_rect = draw_text("Main Menu", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True)
    highlight_button(menu_rect, screen, pause_menu_selection == 2)
    
    return resume_rect, restart_rect, menu_rect

def draw_game_over():
    """the game."""
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    screen.blit(overlay, (0, 0))

    title_font = game_assets['fonts']['title']
    menu_font = game_assets['fonts']['menu']
    
    draw_text(winner_text, title_font, GREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
    
    draw_text("Care for another?", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
    
    #Yes
    # Define rects to ensure they exist for the return statement, even if they're not fully rendered yet.
    play_again_button = draw_text("Yes", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True)
    highlight_button(play_again_button, screen, game_over_selection == 0)

    #No
    main_menu_button_go = draw_text("No", menu_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120, center=True)
    highlight_button(main_menu_button_go, screen, game_over_selection == 1)
    
    return play_again_button, main_menu_button_go

def draw_game_elements():
    """elements of main game"""
    # Draw the custom background first
    if 'background' in game_assets['images']:
        screen.blit(game_assets['images']['background'], (0, 0))
    else:
        screen.fill(BLACK) # Fallback
    
    score_font = game_assets['fonts']['score']
    menu_font = game_assets['fonts']['menu']
    small_font = game_assets['fonts']['small']

    #center line
    pygame.draw.aaline(screen, GREY, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    
    # paddles 
    pygame.draw.rect(screen, RED, player1) 
    pygame.draw.rect(screen, YELLOW, player2) 
    
    # Ball 
    pygame.draw.ellipse(screen, WHITE, ball) 
    
    #Scoreboard 
    
    AVATAR_RADIUS = 15
    AVATAR_FONT = game_assets['fonts']['small']
    
    # Player 1
    p1_name = player1_name if player1_name else "Player 1"
    
    # Avatar
    _, color1, initial1 = AVATAR_STYLES[player1_avatar_index]
    avatar1_center = (SCREEN_WIDTH * 1 // 4 - 80, 50) 
    pygame.draw.circle(screen, color1, avatar1_center, AVATAR_RADIUS)
    draw_text(initial1, AVATAR_FONT, WHITE, screen, avatar1_center[0], avatar1_center[1], center=True)
    
    #Name and Score
    draw_text(p1_name, menu_font, WHITE, screen, SCREEN_WIDTH * 1 // 4, 20, center=True)
    draw_text(str(player1_score), score_font, WHITE, screen, SCREEN_WIDTH * 1 // 4, 60, center=True)

    # Player 2
    p2_name = player2_name if player2_name else "Player 2"

    #Avatar
    _, color2, initial2 = AVATAR_STYLES[player2_avatar_index]
    avatar2_center = (SCREEN_WIDTH * 3 // 4 + 80, 50) 
    pygame.draw.circle(screen, color2, avatar2_center, AVATAR_RADIUS)
    draw_text(initial2, AVATAR_FONT, WHITE, screen, avatar2_center[0], avatar2_center[1], center=True)
    
    #Name and Score
    draw_text(p2_name, menu_font, WHITE, screen, SCREEN_WIDTH * 3 // 4, 20, center=True)
    draw_text(str(player2_score), score_font, WHITE, screen, SCREEN_WIDTH * 3 // 4, 60, center=True)

#Logic 

def handle_paddle_movement():
#paddle positions update
    player1.y += player1_speed
    player2.y += player2_speed
    
    if player1.top <= 0: player1.top = 0
    if player1.bottom >= SCREEN_HEIGHT: player1.bottom = SCREEN_HEIGHT
        
    if player2.top <= 0: player2.top = 0
    if player2.bottom >= SCREEN_HEIGHT: player2.bottom = SCREEN_HEIGHT

def paddle_collision_check(paddle, ball_rect):
   
#edge detection.
    global ball_speed_x, ball_speed_y

    if ball_rect.colliderect(paddle):
        play_sound('paddle_hit') # SOUND
        
        # overlap
        overlap_x = min(ball_rect.right, paddle.right) - max(ball_rect.left, paddle.left)
        overlap_y = min(ball_rect.bottom, paddle.bottom) - max(ball_rect.top, paddle.top)

        # collision  vertical 
        if overlap_y < overlap_x and abs(ball_speed_y) > 0.5:
            
            # Vertical Hit
            ball_speed_y *= -1
            
            # anti ball clipping to the bsck
            if ball_rect.centery < paddle.centery:
                ball_rect.bottom = paddle.top # when the ball hit top edge lets move ball above
            else:
                ball_rect.top = paddle.bottom # same here but bottom edge, move ball below

        else:
            # Horizontal Hit
            ball_speed_x *= -1
            
           
            if ball_speed_x < 0: # Moving left, hit right paddle front
                ball_rect.right = paddle.left
            else: # Moving right, hit left paddle front
                ball_rect.left = paddle.right

#some variation to speed 
            ball_speed_y += random.uniform(-0.5, 0.5)
            # minimum vertical speed
            if abs(ball_speed_y) < 1: ball_speed_y = 1 if ball_speed_y > 0 else -1

def handle_ball_movement():
#Updates ball position and handles collisions
    global ball_speed_x, ball_speed_y, player1_score, player2_score
    global game_state, winner_text, speed_increase_counter
    
    #Progressive Speed
    if game_state == "PLAYING" and progressive_speed_enabled:
        speed_increase_counter += 1
        if speed_increase_counter >= SPEED_INCREASE_INTERVAL:
# Increase magnitude of current speeds
            if ball_speed_x != 0:
                ball_speed_x += (ball_speed_x / abs(ball_speed_x)) * SPEED_INCREASE_AMOUNT
            if ball_speed_y != 0:
                ball_speed_y += (ball_speed_y / abs(ball_speed_y)) * SPEED_INCREASE_AMOUNT
                
            speed_increase_counter = 0

            #max speed
            max_speed = 20
            if abs(ball_speed_x) > max_speed: 
                ball_speed_x = max_speed * (ball_speed_x / abs(ball_speed_x))
            if abs(ball_speed_y) > max_speed: 
                ball_speed_y = max_speed * (ball_speed_y / abs(ball_speed_y))

    
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Wall collision only top and bottom though
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
        play_sound('wall_hit') # SOUND
        
    # Scoring
    if ball.left <= 0:
        player2_score += 1
        play_sound('score') # SOUND
        if player2_score >= WINNING_SCORE:
            p2_name = player2_name if player2_name else "Player 2"
            winner_text = f"{p2_name} Wins!"
            game_state = "GAME_OVER"
            pygame.mouse.set_visible(True) # Show cursor
            play_sound('victory')  #victory sound
        reset_ball()
        
    if ball.right >= SCREEN_WIDTH:
        player1_score += 1
        play_sound('score') # SOUND
        if player1_score >= WINNING_SCORE:
            p1_name = player1_name if player1_name else "Player 1"
            winner_text = f"{p1_name} Wins!"
            game_state = "GAME_OVER"
            pygame.mouse.set_visible(True) # Show cursor
            play_sound('victory')#victory sound
        reset_ball()

    # PADDLE COLLISION
    paddle_collision_check(player1, ball)
    paddle_collision_check(player2, ball)

#Main Game Loop
running = True
try:
    # variables to hold button rectangles for using keyboard nav
    start_rect, easy_rect, medium_rect, hard_rect, speed_rect, quit_rect = [pygame.Rect(0, 0, 1, 1)] * MAIN_MENU_OPTIONS
    resume_rect, restart_rect, menu_rect = [pygame.Rect(0, 0, 1, 1)] * PAUSE_MENU_OPTIONS
    play_again_button, main_menu_button_go = [pygame.Rect(0, 0, 1, 1)] * GAME_OVER_OPTIONS
    difficulty_keys = list(DIFFICULTIES.keys()) 

    while running:
 #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #quit key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
# KEYBOARD MENU NAVIGATION
            if event.type == pygame.KEYDOWN:
                if game_state == "MAIN_MENU":
                    
                # W/S 
                    if event.key == pygame.K_s: 
                        main_menu_selection = (main_menu_selection + 1) % MAIN_MENU_OPTIONS
                    elif event.key == pygame.K_w: 
                        main_menu_selection = (main_menu_selection - 1) % MAIN_MENU_OPTIONS
                        
            # A/D 
                    elif main_menu_selection in [1, 2, 3]:
                        try:
                            current_index = difficulty_keys.index(current_difficulty)
                        except ValueError:
                            current_index = 1# medium 

                        if event.key == pygame.K_a: # Left
                            new_index = (current_index - 1) % len(difficulty_keys)
                            current_difficulty = difficulty_keys[new_index]
                        elif event.key == pygame.K_d: # Right
                            new_index = (current_index + 1) % len(difficulty_keys)
                            current_difficulty = difficulty_keys[new_index]
                            
                        
                        if current_difficulty == "Easy": main_menu_selection = 1
                        elif current_difficulty == "Medium": main_menu_selection = 2
                        elif current_difficulty == "Hard": main_menu_selection = 3

                    # SPACE for click or enter
                    elif event.key == pygame.K_SPACE:
                        if main_menu_selection == 0: #Start
                            player1_name = ""
                            player2_name = ""
                            current_input_text = ""
                            active_input_player = 1
                            input_prompt = "Player 1, enter your name and press SPACE to confirm:"
                            game_state = "GET_NAMES"
                            pygame.mouse.set_visible(True)
                        elif main_menu_selection == 4: # Progressive Speed Toggle 
                            progressive_speed_enabled = not progressive_speed_enabled
                        elif main_menu_selection == 5: # Quit
                            running = False

                elif game_state == "PAUSED":
                    if event.key == pygame.K_s: # Down
                        pause_menu_selection = (pause_menu_selection + 1) % PAUSE_MENU_OPTIONS
                    elif event.key == pygame.K_w: # Up
                        pause_menu_selection = (pause_menu_selection - 1) % PAUSE_MENU_OPTIONS
         # SPACE for click or enter
                    elif event.key == pygame.K_SPACE:
                        if pause_menu_selection == 0: # Resume -> PLAYING
                            game_state = "PLAYING"
                            pygame.mouse.set_visible(False)
                        elif pause_menu_selection == 1: # Restart -> PLAYING
                            reset_game()
                            game_state = "PLAYING"
                            pygame.mouse.set_visible(False)
                        elif pause_menu_selection == 2: #Menu
                            game_state = "MAIN_MENU"
                            pygame.mouse.set_visible(True) # cursor visiblelity

                elif game_state == "GAME_OVER":
                    if event.key == pygame.K_s: # Down
                        game_over_selection = (game_over_selection + 1) % GAME_OVER_OPTIONS
                    elif event.key == pygame.K_w: # Up
                        game_over_selection = (game_over_selection - 1) % GAME_OVER_OPTIONS
        # SPACE for click or enter
                    elif event.key == pygame.K_SPACE:
                        if game_over_selection == 0: # Yes (Play Again) -> PLAYING
                            reset_game()
                            game_state = "PLAYING"
                            pygame.mouse.set_visible(False)
                        elif game_over_selection == 1: # No (Main Menu)
                            game_state = "MAIN_MENU"
                            pygame.mouse.set_visible(True) # Ensure visible

            #MOUSE CLICK EVENTS redundancy
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if game_state == "MAIN_MENU":
                    if start_rect.collidepoint(mouse_pos):
                        player1_name = ""
                        player2_name = ""
                        current_input_text = ""
                        active_input_player = 1
                        input_prompt = "Player 1, enter your name and press SPACE to confirm:"
                        game_state = "GET_NAMES"
                    elif easy_rect.collidepoint(mouse_pos):
                        current_difficulty = "Easy"
                    elif medium_rect.collidepoint(mouse_pos):
                        current_difficulty = "Medium"
                    elif hard_rect.collidepoint(mouse_pos):
                        current_difficulty = "Hard"
                    elif speed_rect.collidepoint(mouse_pos):
                        progressive_speed_enabled = not progressive_speed_enabled
                    elif quit_rect.collidepoint(mouse_pos):
                        running = False
            
                elif game_state == "PAUSED":
                    if resume_rect.collidepoint(mouse_pos):
                        game_state = "PLAYING"
                        pygame.mouse.set_visible(False)
                    elif restart_rect.collidepoint(mouse_pos):
                        reset_game()
                        game_state = "PLAYING"
                        pygame.mouse.set_visible(False)
                    elif menu_rect.collidepoint(mouse_pos):
                        game_state = "MAIN_MENU"

                elif game_state == "GAME_OVER":
                    if play_again_button.collidepoint(mouse_pos):
                        reset_game()
                        game_state = "PLAYING"
                        pygame.mouse.set_visible(False)
                    elif main_menu_button_go.collidepoint(mouse_pos):
                        game_state = "MAIN_MENU"
            
            #GET NAMES 
            elif game_state == "GET_NAMES":
                if event.type == pygame.KEYDOWN:
                  # SPACE for click or enter
                    if event.key == pygame.K_SPACE and current_input_text.strip() != "":
                        # Consume the SPACE character if it was just typed
                        if event.unicode == ' ':
                            current_input_text = current_input_text[:-1]

                        if active_input_player == 1:
                            player1_name = current_input_text.strip()
                            active_input_player = 2
                            current_input_text = ""
                            input_prompt = "Player 2, enter your name and press SPACE to confirm:"
                        elif active_input_player == 2:
                            player2_name = current_input_text.strip()
                            
            #  Avatar Select
                            active_select_player = 1
                            avatar_select_selection = player1_avatar_index 
                            avatar_prompt_message = "" 
                            game_state = "AVATAR_SELECT"
                            
                    elif event.key == pygame.K_BACKSPACE:
                        current_input_text = current_input_text[:-1]
                    elif event.key != pygame.K_RETURN and len(current_input_text) < 15: 
                        current_input_text += event.unicode
            elif game_state == "AVATAR_SELECT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        avatar_prompt_message = ""

                    if event.key == pygame.K_a: # Left
                        avatar_select_selection = (avatar_select_selection - 1) % AVATAR_OPTIONS
                    elif event.key == pygame.K_d: # Right
                        avatar_select_selection = (avatar_select_selection + 1) % AVATAR_OPTIONS
                    elif event.key == pygame.K_SPACE:
                        if active_select_player == 1:
                            player1_avatar_index = avatar_select_selection
                            active_select_player = 2
                            # Start P2 selection but moved from P1 choice
                            avatar_select_selection = (player1_avatar_index + 1) % AVATAR_OPTIONS 
                        elif active_select_player == 2:
                            # 1. duplicate avatar is a no-no
                            if avatar_select_selection == player1_avatar_index:
                                avatar_prompt_message = f"'{AVATAR_STYLES[avatar_select_selection][0]}' is already taken by Player 1! Choose another element."
                            else:
                                print(f"P2 selected {AVATAR_STYLES[avatar_select_selection][0]}. Starting game...") 
                                player2_avatar_index = avatar_select_selection
                                
                                # 2. base speed based on difficulty 
                                ball_speed_base = DIFFICULTIES[current_difficulty] 
                                
                                # 3. Start Game
                                reset_game()
                                game_state = "PLAYING"
                                pygame.mouse.set_visible(False) #gide cursor 
                                avatar_prompt_message = ""

            #Paddle Controls and Pause
            elif game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = "PAUSED"
                        player1_speed = 0
                        player2_speed = 0
                        pygame.mouse.set_visible(True) # show cursir again
                        
                    # Player 1
                    if event.key == pygame.K_w: player1_speed = -PADDLE_SPEED 
                    if event.key == pygame.K_s: player1_speed = PADDLE_SPEED  
                    
                    # Player 2
                    if event.key == pygame.K_UP: player2_speed = -PADDLE_SPEED 
                    if event.key == pygame.K_DOWN: player2_speed = PADDLE_SPEED  
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1_speed = 0
                    # Player 2
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2_speed = 0
        
# Game State
        
        if game_state == "MAIN_MENU":
            # mouse click checking
            start_rect, easy_rect, medium_rect, hard_rect, speed_rect, quit_rect = draw_main_menu()
            
        elif game_state == "GET_NAMES":
            draw_get_names_screen()
        
        elif game_state == "AVATAR_SELECT":
            draw_avatar_select_screen()
            
        elif game_state == "PLAYING":  # Game runs only in the 'PLAYING' state
            handle_paddle_movement()
            handle_ball_movement()
            draw_game_elements()
            
        elif game_state == "PAUSED":
            draw_game_elements() 
            resume_rect, restart_rect, menu_rect = draw_pause_menu()
            
        elif game_state == "GAME_OVER":
            draw_game_elements()
            play_again_button, main_menu_button_go = draw_game_over()

    
        pygame.display.flip()
        
        #Frame Rateeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        clock.tick(144)

finally:
    #Quit
    pygame.quit()
    sys.exit()

