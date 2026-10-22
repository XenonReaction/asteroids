import random

import pygame

from constants import STAR_DENSITY
from constants import STAR_MIN_RADIUS
from constants import STAR_MAX_RADIUS
from constants import STAR_MIN_OPACITY
from constants import STAR_MAX_OPACITY


class Starfield:
    """Random white dots for the background.

    Star positions are stored as fractions of the screen size (0 to 1), so the same
    stars stretch to fit if the window is resized instead of being regenerated.
    """

    def __init__(self, width: int, height: int) -> None:
        count = int(width * height * STAR_DENSITY)

        # Each star is (x fraction, y fraction, radius, opacity)
        self.stars = [
            (
                random.random(),
                random.random(),
                # Squaring the random number makes small stars more common than big ones
                STAR_MIN_RADIUS + (STAR_MAX_RADIUS - STAR_MIN_RADIUS) * random.random() ** 2,
                random.randint(STAR_MIN_OPACITY, STAR_MAX_OPACITY),
            )
            for _ in range(count)
        ]

        # Stars are drawn once onto this surface and reused every frame
        self.surface: pygame.Surface | None = None

    def draw(self, screen: pygame.Surface) -> None:
        if self.surface is None or self.surface.get_size() != screen.get_size():
            self.surface = self.render(screen.get_size())

        screen.blit(self.surface, (0, 0))

    def render(self, size: tuple[int, int]) -> pygame.Surface:
        width, height = size
        surface = pygame.Surface(size)
        surface.fill("black")

        for x, y, radius, opacity in self.stars:
            # White at some opacity over black is just a shade of gray
            color = (opacity, opacity, opacity)
            position = (x * width, y * height)

            # pygame draws nothing for circles smaller than 1, so those become a single pixel
            if radius < 1:
                surface.set_at((int(position[0]), int(position[1])), color)
            else:
                pygame.draw.circle(surface, color, position, radius)

        return surface
