# Screen (starting window size on desktop, the browser uses the page size)
SCREEN_WIDTH = 3200
SCREEN_HEIGHT = 1200
FRAMES_PER_SECOND = 60

# Player
PLAYER_RADIUS = 20
PLAYER_COLOR = "white"
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDWON_SECONDS = 0.3
PLAYER_DEATH_SOUND_FILE_PATH = "./resources/sounds/8_bit_fireball.ogg"
LINE_WIDTH = 2

# Shot
SHOT_RADIUS = 5
SHOT_COLOR = "white"
SHOT_LINE_WIDTH = 2
SHOT_SOUND_FILE_PATH = "./resources/sounds/8_bit_laser.ogg"

# Asteroid
ASTEROID_LINE_WIDTH = 2
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPLIT_POINTS = 5  # added to the progress bar each time an asteroid splits
# How much more often asteroids spawn, and how much faster they move, once the bar is full
ASTEROID_MAX_SPAWN_MULTIPLIER = 3
ASTEROID_MAX_SPEED_MULTIPLIER = 2
ASTEROID_MIN_CRATERS = 3
ASTEROID_MAX_CRATERS = 5
ASTEROID_CRATER_MIN_SIZE = 1/10  # fraction of the asteroid's radius
ASTEROID_CRATER_MAX_SIZE = 1/5
ASTEROID_CRATER_LINE_WIDTH = 1
ASTEROID_LARGE_DESTRUCTION_SOUND_FILE_PATH = "./resources/sounds/8_bit_explosion_09.ogg"
ASTEROID_MEDIUM_DESTRUCTION_SOUND_FILE_PATH = "./resources/sounds/8_bit_explosion_11.ogg"
ASTEROID_SMALL_DESTRUCTION_SOUNDS_FILE_PATHS = [
    "./resources/sounds/8_bit_explosion_01.ogg",
    "./resources/sounds/8_bit_explosion_03.ogg",
    "./resources/sounds/8_bit_explosion_10.ogg"
]
# One chord per asteroid color change, in order (purple -> blue plays the first one)
COLOR_CHANGE_CHORD_FILE_PATHS = [
    "./resources/sounds/chord_c_major.ogg",
    "./resources/sounds/chord_d_minor.ogg",
    "./resources/sounds/chord_e_minor.ogg",
    "./resources/sounds/chord_g_major.ogg",
    "./resources/sounds/chord_a_major.ogg"
]
WIN_SOUND_FILE_PATH = "./resources/sounds/8_bit_win.ogg"

# Progress bar (asteroids take the color of the section the bar has filled up to)
PROGRESS_BAR_COLORS = ["purple", "blue", "green", "yellow", "orange", "red"]
PROGRESS_BAR_MAX = 500
PROGRESS_BAR_HEIGHT = 20
PROGRESS_BAR_MARGIN = 20  # gap between the bar and the screen edges
PROGRESS_BAR_LINE_WIDTH = 2
PROGRESS_BAR_BACKGROUND_COLOR = "gray20"

# Background stars
STAR_DENSITY = 0.0001  # stars per pixel of screen
STAR_MIN_RADIUS = 0.5
STAR_MAX_RADIUS = 3
STAR_MIN_OPACITY = 40  # 0 is invisible, 255 is fully white
STAR_MAX_OPACITY = 255

# Main menu
MENU_TITLE = "Asteroids"
MENU_TITLE_FONT_SIZE = 160
MENU_TEXT_COLOR = "white"
MENU_START_ASTEROIDS = 10
MENU_BUTTON_TEXT = "START"
MENU_BUTTON_FONT_SIZE = 56
MENU_BUTTON_WIDTH = 260
MENU_BUTTON_HEIGHT = 80
MENU_BUTTON_PADDING = 30  # space on each side of the longest label
MENU_BUTTON_SPACING = 20  # gap between buttons
MENU_BUTTON_LINE_WIDTH = 3
MENU_BUTTON_SELECTED_COLOR = "gray20"
MENU_BUTTON_BOB_PIXELS = 12
MENU_BUTTON_BOB_SPEED = 2
MENU_OVERLAY_OPACITY = 160  # how dark the game gets behind the pause and win menus (0-255)

# Pause and win menus
PAUSE_TITLE = "Paused"
PAUSE_CONTINUE_TEXT = "Continue?"
PAUSE_QUIT_TEXT = "Quit"
WIN_TITLE = "You win!"
WIN_PLAY_AGAIN_TEXT = "Play again?"
WIN_EXIT_TEXT = "Exit"
WIN_FREEZE_SECONDS = 1  # everything stops before the message starts fading in
WIN_HOLD_SECONDS = 2  # message stays up on its own before the buttons appear
