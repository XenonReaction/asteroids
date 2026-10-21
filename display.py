import sys

import pygame

from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT

# True when running in the browser (pygbag)
IS_WEB = sys.platform == "emscripten"

if IS_WEB:
    # pygbag adds a `window` attribute here that gives access to the browser window
    import platform


def _browser_size() -> tuple[int, int]:
    return (int(platform.window.innerWidth), int(platform.window.innerHeight))


def create_screen() -> pygame.Surface:
    if IS_WEB:
        screen = pygame.display.set_mode(_browser_size())
        # Ask the page to re-fit the canvas to the new size
        platform.window.window_resize()
        return screen

    # On desktop the window can be resized by dragging its edges
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)


def fit_to_window() -> pygame.Surface:
    """Call once per frame. Resizes the screen if the browser window changed size."""
    screen = pygame.display.get_surface()

    # Desktop windows resize themselves, the browser canvas needs to be told
    if IS_WEB and screen.get_size() != _browser_size():
        screen = create_screen()

    return screen
