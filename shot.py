import pygame

from constants import SHOT_RADIUS
from constants import SHOT_COLOR
from constants import SHOT_LINE_WIDTH
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: "Screen"):
        pygame.draw.circle(screen, SHOT_COLOR, self.position, self.radius, SHOT_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

        # Remove shots once they leave the screen, otherwise every missed shot
        # keeps flying (and being checked against every asteroid) forever
        width, height = pygame.display.get_surface().get_size()
        if not (-self.radius <= self.position.x <= width + self.radius
                and -self.radius <= self.position.y <= height + self.radius):
            self.kill()