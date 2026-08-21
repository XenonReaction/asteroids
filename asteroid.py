import pygame

from circleshape import CircleShape
from constants import ASTEROID_COLOR
from constants import ASTEROID_LINE_WIDTH
from constants import SCREEN_HEIGHT
from constants import SCREEN_WIDTH

class Asteroid(CircleShape):
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: "Screen"):
        pygame.draw.circle(screen, ASTEROID_COLOR, self.position, self.radius, ASTEROID_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt