import pygame
import random

from constants import MIXER_CHANNELS
from constants import PLAYER_ENGINE_VOLUME
from constants import PLAYER_ENGINE_FADE_MS
from constants import version

class SoundMixer:
    # Sounds are loaded once and shared by every SoundMixer.
    # They're loaded again if the version of the game changes.
    _loaded_version = None
    # The channel the engine sound is looping on, or None while it's off
    _engine_channel = None

    def __init__(self):
        sounds = version()
        if SoundMixer._loaded_version is sounds:
            return

        pygame.mixer.init()
        pygame.mixer.set_num_channels(MIXER_CHANNELS)

        SoundMixer.PLAYER_DEATH_SOUND = pygame.mixer.Sound(file = sounds.PLAYER_DEATH_SOUND_FILE_PATH)
        SoundMixer.SHOT_SOUND = pygame.mixer.Sound(file = sounds.SHOT_SOUND_FILE_PATH)
        SoundMixer.ENGINE_SOUND = pygame.mixer.Sound(file = sounds.ENGINE_SOUND_FILE_PATH)
        SoundMixer.ENGINE_SOUND.set_volume(PLAYER_ENGINE_VOLUME)
        SoundMixer.FIREWORK_SOUND = pygame.mixer.Sound(file = sounds.FIREWORK_SOUND_FILE_PATH)
        SoundMixer.ASTEROID_LARGE_DESTRUCTION_SOUND = pygame.mixer.Sound(file = sounds.ASTEROID_LARGE_DESTRUCTION_SOUND_FILE_PATH)
        SoundMixer.ASTEROID_MEDIUM_DESTRUCTION_SOUND = pygame.mixer.Sound(file = sounds.ASTEROID_MEDIUM_DESTRUCTION_SOUND_FILE_PATH)
        SoundMixer.ASTEROID_SMALL_DESTRUCTION_SOUNDS = []

        for path in sounds.ASTEROID_SMALL_DESTRUCTION_SOUNDS_FILE_PATHS:
            SoundMixer.ASTEROID_SMALL_DESTRUCTION_SOUNDS.append(pygame.mixer.Sound(path))

        SoundMixer.COLOR_CHANGE_CHORDS = [pygame.mixer.Sound(path) for path in sounds.COLOR_CHANGE_CHORD_FILE_PATHS]
        SoundMixer.WIN_SOUND = pygame.mixer.Sound(file = sounds.WIN_SOUND_FILE_PATH)
        SoundMixer.MENU_MOVE_SOUND = pygame.mixer.Sound(file = sounds.MENU_MOVE_SOUND_FILE_PATH)
        SoundMixer.MENU_SELECT_SOUND = pygame.mixer.Sound(file = sounds.MENU_SELECT_SOUND_FILE_PATH)

        SoundMixer._loaded_version = sounds

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
            case "firework":
                self.FIREWORK_SOUND.play()
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

    def engine(self, on: bool) -> None:
        # Called every frame, so the sound only starts or stops when `on` changes
        if on and SoundMixer._engine_channel is None:
            SoundMixer._engine_channel = self.ENGINE_SOUND.play(loops=-1, fade_ms=PLAYER_ENGINE_FADE_MS)
        elif not on and SoundMixer._engine_channel is not None:
            SoundMixer._engine_channel.fadeout(PLAYER_ENGINE_FADE_MS)
            SoundMixer._engine_channel = None
