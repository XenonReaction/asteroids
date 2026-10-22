import random
from collections.abc import Callable

import pygame
from asteroid import Asteroid
from constants import *
from progress_bar import ProgressBar

# Each edge is (direction asteroids move in, function giving a spawn point from
# a 0-1 position along the edge and the current screen width and height)
Edge = tuple[pygame.Vector2, Callable[[float, int, int], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group
    # Set by the game, asteroids come more often and faster as it fills
    progress_bar: ProgressBar

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y, width, height: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * height),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y, width, height: pygame.Vector2(
                width + ASTEROID_MAX_RADIUS, y * height
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x, width, height: pygame.Vector2(x * width, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x, width, height: pygame.Vector2(
                x * width, height + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        # Goes from 0 to 1 as the progress bar fills
        difficulty = self.progress_bar.fraction()
        spawn_multiplier = 1 + difficulty * (ASTEROID_MAX_SPAWN_MULTIPLIER - 1)
        speed_multiplier = 1 + difficulty * (ASTEROID_MAX_SPEED_MULTIPLIER - 1)

        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS / spawn_multiplier:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100) * speed_multiplier
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            width, height = pygame.display.get_surface().get_size()
            position = edge[1](random.uniform(0, 1), width, height)
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)