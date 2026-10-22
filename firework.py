import random

import pygame

from constants import PROGRESS_BAR_COLORS
from constants import FIREWORK_LAUNCH_SPEED
from constants import FIREWORK_LAUNCH_SPREAD_DEGREES
from constants import FIREWORK_FUSE_SECONDS
from constants import FIREWORK_ROCKET_RADIUS
from constants import FIREWORK_ROCKET_DRAG
from constants import FIREWORK_TRAIL_SPARKS_PER_SECOND
from constants import FIREWORK_TRAIL_LIFETIME_SECONDS
from constants import FIREWORK_BURST_SPARKS
from constants import FIREWORK_BURST_SPEED
from constants import FIREWORK_SPARK_DRAG
from constants import FIREWORK_SPARK_GRAVITY
from constants import FIREWORK_SPARK_MIN_LIFETIME_SECONDS
from constants import FIREWORK_SPARK_MAX_LIFETIME_SECONDS
from constants import FIREWORK_SPARK_RADIUS
from circleshape import CircleShape
from sounds import SoundMixer


class Spark(CircleShape):
    """A colored dot that slows down and fades out. Fireworks are made of these."""

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, color: str,
                 radius: float, lifetime: float, gravity: float = 0) -> None:
        super().__init__(position.x, position.y, radius)
        self.velocity = pygame.Vector2(velocity)
        self.color = pygame.Color(color)
        self.lifetime = lifetime
        self.gravity = gravity
        self.age = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        # Fade toward black, like the exhaust dots
        faded = self.color.lerp("black", min(self.age / self.lifetime, 1))
        pygame.draw.circle(screen, faded, self.position, self.radius)

    def update(self, dt: float) -> None:
        self.velocity *= max(0, 1 - FIREWORK_SPARK_DRAG * dt)
        self.velocity.y += self.gravity * dt
        self.position += self.velocity * dt

        self.age += dt
        if self.age >= self.lifetime:
            self.kill()


class Firework(CircleShape):
    """A rocket that flies off in `direction`, leaving a trail, then bursts into sparks.

    The color is picked at random from the asteroid colors.
    """

    def __init__(self, position: pygame.Vector2, direction: pygame.Vector2) -> None:
        super().__init__(position.x, position.y, FIREWORK_ROCKET_RADIUS)
        spread = random.uniform(-FIREWORK_LAUNCH_SPREAD_DEGREES, FIREWORK_LAUNCH_SPREAD_DEGREES)
        self.velocity = direction.rotate(spread) * FIREWORK_LAUNCH_SPEED
        self.color = random.choice(PROGRESS_BAR_COLORS)
        self.fuse = FIREWORK_FUSE_SECONDS
        self.trail_timer = 0.0
        self.sound_mixer = SoundMixer()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update(self, dt: float) -> None:
        self.velocity *= max(0, 1 - FIREWORK_ROCKET_DRAG * dt)
        self.position += self.velocity * dt

        # Leave a trail of short-lived sparks behind the rocket
        self.trail_timer -= dt
        while self.trail_timer <= 0:
            drift = pygame.Vector2(random.uniform(5, 20), 0).rotate(random.uniform(0, 360))
            Spark(self.position, drift, self.color, FIREWORK_SPARK_RADIUS / 2, FIREWORK_TRAIL_LIFETIME_SECONDS)
            self.trail_timer += random.expovariate(FIREWORK_TRAIL_SPARKS_PER_SECOND)

        self.fuse -= dt
        if self.fuse <= 0:
            self.burst()

    def burst(self) -> None:
        self.kill()
        self.sound_mixer.play("firework")

        for _ in range(FIREWORK_BURST_SPARKS):
            # Square root spreads the sparks evenly through the circle instead of bunching at the middle
            speed = FIREWORK_BURST_SPEED * random.random() ** 0.5
            velocity = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
            lifetime = random.uniform(FIREWORK_SPARK_MIN_LIFETIME_SECONDS, FIREWORK_SPARK_MAX_LIFETIME_SECONDS)
            Spark(self.position, velocity, self.color, FIREWORK_SPARK_RADIUS, lifetime, FIREWORK_SPARK_GRAVITY)
