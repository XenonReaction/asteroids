import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_COLOR
from constants import ASTEROID_LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from logger import log_event

from sounds import SoundMixer

class Asteroid(CircleShape):
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.sound_mixer = SoundMixer()

    def draw(self, screen: "Screen"):
        pygame.draw.circle(screen, ASTEROID_COLOR, self.position, self.radius, ASTEROID_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

        # Remove asteroids that drift far off screen so they don't pile up forever
        width, height = pygame.display.get_surface().get_size()
        margin = ASTEROID_MAX_RADIUS * 2
        if not (-margin <= self.position.x <= width + margin
                and -margin <= self.position.y <= height + margin):
            self.kill()

    def split(self) -> None:
        self.kill()

        self.sound_mixer.play("asteroid_destruction")

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")

        rand_angle = random.uniform(20, 50)

        vector_1 = pygame.math.Vector2.rotate(self.velocity, rand_angle)
        vector_2 = pygame.math.Vector2.rotate(self.velocity, -rand_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid_1.velocity = vector_1*1.2
        asteroid_2.velocity = vector_2*1.2