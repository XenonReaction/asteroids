import pygame

from constants import PLAYER_DEATH_SOUND_FILE_PATH
from constants import SHOT_SOUND_FILE_PATH
from constants import ASTEROID_DESTRUCTION_SOUNDS_FILE_PATHS

pygame.mixer.init()

PLAYER_DEATH_SOUND = pygame.mixer.Sound(file = PLAYER_DEATH_SOUND_FILE_PATH)
SHOT_SOUND = pygame.mixer.Sound(file = SHOT_SOUND_FILE_PATH)
ASTEROID_DESTRUCTION_SOUND = pygame.mixer.Sound(file = ASTEROID_DESTRUCTION_SOUNDS_FILE_PATHS[0])