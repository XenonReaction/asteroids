import pygame
import random

from constants import PLAYER_DEATH_SOUND_FILE_PATH
from constants import SHOT_SOUND_FILE_PATH
from constants import ASTEROID_LARGE_DESTRUCTION_SOUND_FILE_PATH
from constants import ASTEROID_MEDIUM_DESTRUCTION_SOUND_FILE_PATH
from constants import ASTEROID_SMALL_DESTRUCTION_SOUNDS_FILE_PATHS
from constants import COLOR_CHANGE_CHORD_FILE_PATHS
from constants import WIN_SOUND_FILE_PATH
from constants import MENU_MOVE_SOUND_FILE_PATH
from constants import MENU_SELECT_SOUND_FILE_PATH

class SoundMixer:
    # Sounds are loaded once and shared by every SoundMixer
    _loaded = False

    def __init__(self):
        if SoundMixer._loaded:
            return

        pygame.mixer.init()

        SoundMixer.PLAYER_DEATH_SOUND = pygame.mixer.Sound(file = PLAYER_DEATH_SOUND_FILE_PATH)
        SoundMixer.SHOT_SOUND = pygame.mixer.Sound(file = SHOT_SOUND_FILE_PATH)
        SoundMixer.ASTEROID_LARGE_DESTRUCTION_SOUND = pygame.mixer.Sound(file = ASTEROID_LARGE_DESTRUCTION_SOUND_FILE_PATH)
        SoundMixer.ASTEROID_MEDIUM_DESTRUCTION_SOUND = pygame.mixer.Sound(file = ASTEROID_MEDIUM_DESTRUCTION_SOUND_FILE_PATH)
        SoundMixer.ASTEROID_SMALL_DESTRUCTION_SOUNDS = []

        for path in ASTEROID_SMALL_DESTRUCTION_SOUNDS_FILE_PATHS:
            SoundMixer.ASTEROID_SMALL_DESTRUCTION_SOUNDS.append(pygame.mixer.Sound(path))

        SoundMixer.COLOR_CHANGE_CHORDS = [pygame.mixer.Sound(path) for path in COLOR_CHANGE_CHORD_FILE_PATHS]
        SoundMixer.WIN_SOUND = pygame.mixer.Sound(file = WIN_SOUND_FILE_PATH)
        SoundMixer.MENU_MOVE_SOUND = pygame.mixer.Sound(file = MENU_MOVE_SOUND_FILE_PATH)
        SoundMixer.MENU_SELECT_SOUND = pygame.mixer.Sound(file = MENU_SELECT_SOUND_FILE_PATH)

        SoundMixer._loaded = True

    def play(self, sound: str) -> None:
        match sound:
            case "player_death":
                self.PLAYER_DEATH_SOUND.play()
            case "shot":
                self.SHOT_SOUND.play()
            case "asteroid_destruction_large":
                self.ASTEROID_LARGE_DESTRUCTION_SOUND.play()
            case "asteroid_destruction_medium":
                self.ASTEROID_MEDIUM_DESTRUCTION_SOUND.play()
            case "asteroid_destruction_small":
                random.choice(self.ASTEROID_SMALL_DESTRUCTION_SOUNDS).play()
            case "win":
                self.WIN_SOUND.play()
            case "menu_move":
                self.MENU_MOVE_SOUND.play()
            case "menu_select":
                self.MENU_SELECT_SOUND.play()
            case _:
                print("Invalid sound call")

    def play_chord(self, color_change: int) -> None:
        # color_change counts from 0 for the first time the asteroids change color
        if color_change < len(self.COLOR_CHANGE_CHORDS):
            self.COLOR_CHANGE_CHORDS[color_change].play()

    def win_length(self) -> float:
        # How many seconds the win sound lasts
        return self.WIN_SOUND.get_length()