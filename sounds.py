import pygame
import random

from constants import PLAYER_DEATH_SOUND_FILE_PATH
from constants import SHOT_SOUND_FILE_PATH
from constants import ASTEROID_DESTRUCTION_SOUNDS_FILE_PATHS

class SoundMixer:
    
    def __init__(self):
        
        pygame.mixer.init()

        self.PLAYER_DEATH_SOUND = pygame.mixer.Sound(file = PLAYER_DEATH_SOUND_FILE_PATH)
        self.SHOT_SOUND = pygame.mixer.Sound(file = SHOT_SOUND_FILE_PATH)
        self.ASTEROID_DESTRUCTION_SOUNDS = []

        for path in ASTEROID_DESTRUCTION_SOUNDS_FILE_PATHS:
            self.ASTEROID_DESTRUCTION_SOUNDS.append(pygame.mixer.Sound(path))

    def play(self, sound: str) -> None:
        match sound:
            case "player_death":
                self.PLAYER_DEATH_SOUND.play()
            case "shot":
                self.SHOT_SOUND.play()
            case "asteroid_destruction":
                random.choice(self.ASTEROID_DESTRUCTION_SOUNDS).play()
            case _:
                print("Invalid sound call")