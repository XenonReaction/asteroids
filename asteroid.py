import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_COLOR
from constants import ASTEROID_LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import SCREEN_HEIGHT
from constants import SCREEN_WIDTH
from logger import log_event

class Asteroid(CircleShape):
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: "Screen"):
        pygame.draw.circle(screen, ASTEROID_COLOR, self.position, self.radius, ASTEROID_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()

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