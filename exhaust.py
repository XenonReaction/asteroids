import random

import pygame

from constants import EXHAUST_MIN_SPEED
from constants import EXHAUST_MAX_SPEED
from constants import EXHAUST_SPREAD_DEGREES
from constants import EXHAUST_MIN_LIFETIME_SECONDS
from constants import EXHAUST_MAX_LIFETIME_SECONDS
from constants import EXHAUST_MIN_RADIUS
from constants import EXHAUST_MAX_RADIUS
from circleshape import CircleShape


class Exhaust(CircleShape):
    """A white dot that drifts away from the ship's engine and fades out."""

    def __init__(self, position: pygame.Vector2, direction: pygame.Vector2) -> None:
        super().__init__(position.x, position.y, random.uniform(EXHAUST_MIN_RADIUS, EXHAUST_MAX_RADIUS))

        # Point roughly along `direction`, a little to either side at random
        spread = random.uniform(-EXHAUST_SPREAD_DEGREES, EXHAUST_SPREAD_DEGREES)
        self.velocity = direction.rotate(spread) * random.uniform(EXHAUST_MIN_SPEED, EXHAUST_MAX_SPEED)

        self.lifetime = random.uniform(EXHAUST_MIN_LIFETIME_SECONDS, EXHAUST_MAX_LIFETIME_SECONDS)
        self.age = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        # White fading toward black, like the background stars
        brightness = int(255 * (1 - self.age / self.lifetime))
        pygame.draw.circle(screen, (brightness, brightness, brightness), self.position, self.radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
