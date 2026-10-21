# Screen
SCREEN_WIDTH = 3200
SCREEN_HEIGHT = 1200
FRAMES_PER_SECOND = 60

# Player
PLAYER_RADIUS = 20
PLAYER_COLOR = "blue"
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
ASTEROID_COLOR = "red"
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_DESTRUCTION_SOUNDS_FILE_PATHS = [
    "./resources/sounds/8_bit_explosion_01.ogg",
    "./resources/sounds/8_bit_explosion_03.ogg",
    "./resources/sounds/8_bit_explosion_09.ogg",
    "./resources/sounds/8_bit_explosion_10.ogg",
    "./resources/sounds/8_bit_explosion_11.ogg"
]
