# Screen (starting window size on desktop, the browser uses the page size)
SCREEN_WIDTH = 3200
SCREEN_HEIGHT = 1200
FRAMES_PER_SECOND = 60

# Sound
MIXER_CHANNELS = 32  # how many sounds can play at once (pygame's default is 8)

# Player
PLAYER_RADIUS = 20
PLAYER_COLOR = "white"
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDWON_SECONDS = 0.3
LINE_WIDTH = 2
PLAYER_ENGINE_VOLUME = 0.4  # 0 is silent, 1 is full volume
PLAYER_ENGINE_FADE_MS = 150  # how long the engine sound takes to fade in and out

# Exhaust (dots that shoot out behind the ship, or in front of it when reversing)
EXHAUST_DOTS_PER_SECOND = 40  # on average, the time between dots is random
EXHAUST_MIN_SPEED = 30
EXHAUST_MAX_SPEED = 80
EXHAUST_SPREAD_DEGREES = 25  # how far to each side of straight back a dot can go
EXHAUST_MIN_LIFETIME_SECONDS = 0.2
EXHAUST_MAX_LIFETIME_SECONDS = 0.5
EXHAUST_MIN_RADIUS = 1
EXHAUST_MAX_RADIUS = 2.5

# Fireworks (launched out of the back of the ship when you win, in one of the asteroid colors at random)
FIREWORK_LAUNCH_SPEED = 350
FIREWORK_LAUNCH_SPREAD_DEGREES = 20  # how far to each side of straight back the rocket can go
FIREWORK_FUSE_SECONDS = 0.8  # how long the rocket flies before it bursts
FIREWORK_ROCKET_RADIUS = 3
FIREWORK_ROCKET_DRAG = 1.5  # how quickly the rocket slows down (bigger slows faster)
FIREWORK_TRAIL_SPARKS_PER_SECOND = 60  # sparks the rocket leaves behind as it flies
FIREWORK_TRAIL_LIFETIME_SECONDS = 0.3
FIREWORK_BURST_SPARKS = 70
FIREWORK_BURST_SPEED = 220  # fastest a burst spark starts out
FIREWORK_SPARK_DRAG = 1.5
FIREWORK_SPARK_GRAVITY = 40  # burst sparks slowly droop down
FIREWORK_SPARK_MIN_LIFETIME_SECONDS = 0.8
FIREWORK_SPARK_MAX_LIFETIME_SECONDS = 1.4
FIREWORK_SPARK_RADIUS = 2

# Shot
SHOT_RADIUS = 5
SHOT_COLOR = "white"
SHOT_LINE_WIDTH = 2

# Asteroid
ASTEROID_LINE_WIDTH = 2
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
# How much more often asteroids spawn, and how much faster they move, once the bar is full
ASTEROID_MAX_SPAWN_MULTIPLIER = 3
ASTEROID_MAX_SPEED_MULTIPLIER = 2
ASTEROID_MIN_CRATERS = 3
ASTEROID_MAX_CRATERS = 5
ASTEROID_CRATER_MIN_SIZE = 1/10  # fraction of the asteroid's radius
ASTEROID_CRATER_MAX_SIZE = 1/5
ASTEROID_CRATER_LINE_WIDTH = 1

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
MENU_TITLE_FONT_SIZE = 160
MENU_SUBTITLE_FONT_SIZE = 64  # smaller line under a title, like the score on the win screen
MENU_TEXT_COLOR = "white"
MENU_START_ASTEROIDS = 10
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

# Settings (difficulty, every setting goes from 1 for easiest to 10 for hardest)
SETTING_MIN = 1
SETTING_MAX = 10
# How often asteroids spawn and how fast they move at setting 1 and setting 10,
# compared to normal. Settings in between are spread evenly from one to the other.
SETTINGS_ASTEROID_AMOUNT_EASIEST = 0.5  # half as many asteroids
SETTINGS_ASTEROID_AMOUNT_HARDEST = 2.8
SETTINGS_ASTEROID_SPEED_EASIEST = 0.6
SETTINGS_ASTEROID_SPEED_HARDEST = 2.35
SETTINGS_FONT_SIZE = 44
SETTINGS_SQUARE_SIZE = 56
SETTINGS_SQUARE_GAP = 10  # space between squares
SETTINGS_SQUARE_LINE_WIDTH = 2
SETTINGS_LABEL_GAP = 40  # space between a label and its squares
SETTINGS_ROW_SPACING = 30  # space between rows
SETTINGS_CHOSEN_COLOR = "white"  # fill of the square for each setting's current value
SETTINGS_CURSOR_COLOR = "yellow"  # border of the square the cursor is on
SETTINGS_CURSOR_LINE_WIDTH = 4
SETTINGS_INACTIVE_TEXT_COLOR = "gray60"  # labels of the rows the cursor isn't on

# Intro cutscene (plays once when the game opens, any key or click skips it)
INTRO_FLY_IN_SECONDS = 1.5
INTRO_SHIP_STOP_X = 0.25  # where the ship stops, as a fraction of the screen width
INTRO_ASTEROID_X = 0.6  # where the asteroid starts
INTRO_ASTEROID_DRIFT_SPEED = 20  # the asteroid drifts slowly toward the ship
INTRO_SHOOT_DELAY_SECONDS = 0.4  # pause between the ship stopping and shooting
INTRO_ASTEROID_PUSH_SPEED = 120  # the shot knocks the pieces away from the ship
INTRO_FLY_OFF_DELAY_SECONDS = 0.5  # pause between the asteroid breaking and the ship flying off
INTRO_FLY_OFF_ACCELERATION = 800  # the ship speeds up off the right side of the screen
INTRO_FADE_OUT_SECONDS = 0.8  # whatever is left fades away before the menu appears
MENU_FADE_IN_SECONDS = 1.5

# Win sequence
WIN_FREEZE_SECONDS = 1  # everything stops before the win cutscene starts
WIN_ASTEROID_FADE_SECONDS = 3  # the asteroids slowly fade away while the ship celebrates
WIN_SPIN_CIRCLES = 3  # full circles the ship flies before heading off to the right
WIN_SPIN_DEGREES_PER_SECOND = 300
WIN_SPIN_SPEED = 400  # how fast the ship flies around its circles
WIN_FLY_OFF_ACCELERATION = 600  # the ship speeds up off the right side of the screen
WIN_FIREWORK_MIN_GAP_SECONDS = 0.25  # time between fireworks is random, between these two
WIN_FIREWORK_MAX_GAP_SECONDS = 0.6
WIN_HOLD_SECONDS = 2  # message stays up on its own before the buttons appear

# Win code, 4 letters in the bottom right of the win screen that stand for the exact settings played on
WIN_CODE_LETTERS = 4
# The codes are shuffled so similar settings don't get similar codes. Changing these changes
# every code. The multiplier must not be divisible by 2 or 13, or two settings could share a code.
WIN_CODE_MULTIPLIER = 7919
WIN_CODE_OFFSET = 123457
WIN_CODE_FONT_SIZE = 48
WIN_CODE_MARGIN = 20  # gap between the code and the bottom right corner


# =============================================================================
# Game versions
#
# Sounds and messages can be different in each version of the game. Everything
# above this line is shared by every version.
#
# Game code reads these through version(), for example version().WIN_TITLE, so
# it always gets the values for the version that is playing.
# =============================================================================

class OriginalVersion:
    # Sounds
    PLAYER_DEATH_SOUND_FILE_PATH = "./resources/sounds/8_bit_fireball.ogg"
    SHOT_SOUND_FILE_PATH = "./resources/sounds/8_bit_laser.ogg"
    ENGINE_SOUND_FILE_PATH = "./resources/sounds/engine_hum.ogg"  # loops while moving
    FIREWORK_SOUND_FILE_PATH = "./resources/sounds/8_bit_explosion_01.ogg"  # when a firework bursts
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
    MENU_MOVE_SOUND_FILE_PATH = "./resources/sounds/8_bit_move_beep.ogg"
    MENU_SELECT_SOUND_FILE_PATH = "./resources/sounds/8_bit_select_beep.ogg"

    # Main menu messages
    MENU_TITLE = "Asteroids"
    MENU_BUTTON_TEXT = "START"
    MENU_SETTINGS_TEXT = "SETTINGS"

    # Settings menu messages
    SETTINGS_TITLE = "Settings"
    SETTINGS_ASTEROID_AMOUNT_TEXT = "Number of asteroids"
    SETTINGS_ASTEROID_SPEED_TEXT = "Asteroid speed"
    SETTINGS_DESTRUCTION_VALUE_TEXT = "Asteroid destruction value"
    SETTINGS_BACK_TEXT = "Back"

    # Pause and win menu messages
    PAUSE_TITLE = "Paused"
    PAUSE_CONTINUE_TEXT = "Continue?"
    PAUSE_QUIT_TEXT = "Quit"
    WIN_TITLE = "You win!"
    # {score} and {max_score} are filled in with the numbers
    WIN_SCORE_TEXT = "Score: {score} / {max_score}"
    WIN_PLAY_AGAIN_TEXT = "Play again?"
    WIN_EXIT_TEXT = "Exit"


class BeckhamVersion(OriginalVersion):
    # Beckham's Version. Everything starts as a copy of the original version.
    # Replace each value with Beckham's sounds and messages as they're ready.
    # Anything deleted from here falls back to the original version's value.
    # Sound files must be .ogg (the web version won't build with .mp3 files).

    # Sounds
    PLAYER_DEATH_SOUND_FILE_PATH = "./resources/sounds/8_bit_fireball.ogg"
    SHOT_SOUND_FILE_PATH = "./resources/sounds/8_bit_laser.ogg"
    ENGINE_SOUND_FILE_PATH = "./resources/sounds/engine_hum.ogg"  # loops while moving
    FIREWORK_SOUND_FILE_PATH = "./resources/sounds/8_bit_explosion_01.ogg"  # when a firework bursts
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
    MENU_MOVE_SOUND_FILE_PATH = "./resources/sounds/8_bit_move_beep.ogg"
    MENU_SELECT_SOUND_FILE_PATH = "./resources/sounds/8_bit_select_beep.ogg"

    # Main menu messages
    MENU_TITLE = "Asteroids"
    MENU_BUTTON_TEXT = "START"
    MENU_SETTINGS_TEXT = "SETTINGS"

    # Settings menu messages
    SETTINGS_TITLE = "Settings"
    SETTINGS_ASTEROID_AMOUNT_TEXT = "Number of asteroids"
    SETTINGS_ASTEROID_SPEED_TEXT = "Asteroid speed"
    SETTINGS_DESTRUCTION_VALUE_TEXT = "Asteroid destruction value"
    SETTINGS_BACK_TEXT = "Back"

    # Pause and win menu messages
    PAUSE_TITLE = "Paused"
    PAUSE_CONTINUE_TEXT = "Continue?"
    PAUSE_QUIT_TEXT = "Quit"
    WIN_TITLE = "You win!"
    # {score} and {max_score} are filled in with the numbers
    WIN_SCORE_TEXT = "Score: {score} / {max_score}"
    WIN_PLAY_AGAIN_TEXT = "Play again?"
    WIN_EXIT_TEXT = "Exit"


# The version that is playing. There's no in-game switch yet.
# To try Beckham's Version, change this to BeckhamVersion.
ACTIVE_VERSION = OriginalVersion


def version() -> type[OriginalVersion]:
    """The version that is playing.

    Code calls this every time it needs a sound or message, instead of copying
    ACTIVE_VERSION once, so changing ACTIVE_VERSION while the game runs works.
    """
    return ACTIVE_VERSION
