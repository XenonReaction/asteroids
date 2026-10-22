import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
from constants import ASTEROID_MIN_CRATERS
from constants import ASTEROID_MAX_CRATERS
from constants import ASTEROID_CRATER_MIN_SIZE
from constants import ASTEROID_CRATER_MAX_SIZE
from constants import ASTEROID_CRATER_LINE_WIDTH
from logger import log_event
from progress_bar import ProgressBar
from settings import Settings

from sounds import SoundMixer

class Asteroid(CircleShape):
    # Set by the game, splits fill it up and it decides what color asteroids are
    progress_bar: ProgressBar
    # Set by the game, decides how much each split adds to the progress bar
    settings: Settings

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.sound_mixer = SoundMixer()
        self.craters = self.make_craters()

    def make_craters(self) -> list[tuple[pygame.Vector2, float]]:
        """Pick crater circles (offset from center, radius) that don't touch each other or the edge."""
        craters = []
        count = random.randint(ASTEROID_MIN_CRATERS, ASTEROID_MAX_CRATERS)

        # Try random spots until enough craters fit, giving up after a while just in case
        for _ in range(100):
            if len(craters) == count:
                break

            crater_radius = random.uniform(self.radius * ASTEROID_CRATER_MIN_SIZE, self.radius * ASTEROID_CRATER_MAX_SIZE)

            # Furthest from the center the crater can be and still leave a gap before the outline
            max_distance = self.radius - ASTEROID_LINE_WIDTH - crater_radius - 1
            offset = pygame.Vector2(random.uniform(0, max_distance), 0).rotate(random.uniform(0, 360))

            # Keep a gap between this crater and every other crater
            if all(offset.distance_to(other_offset) > crater_radius + other_radius + 1
                   for other_offset, other_radius in craters):
                craters.append((offset, crater_radius))

        return craters

    def draw(self, screen: "Screen"):
        # Fill with black first so asteroids hide what's behind them, then draw the outline
        color = self.progress_bar.current_color()
        pygame.draw.circle(screen, "black", self.position, self.radius)
        pygame.draw.circle(screen, color, self.position, self.radius, ASTEROID_LINE_WIDTH)

        for offset, crater_radius in self.craters:
            pygame.draw.circle(screen, color, self.position + offset, crater_radius, ASTEROID_CRATER_LINE_WIDTH)

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

        # Play a chord whenever this split changes the asteroids' color
        old_section = self.progress_bar.section_index()
        self.progress_bar.add(self.settings.split_points())
        new_section = self.progress_bar.section_index()
        if new_section != old_section:
            self.sound_mixer.play_chord(new_section - 1)

        # Each asteroid size has its own explosion sound
        if self.radius >= ASTEROID_MAX_RADIUS:
            self.sound_mixer.play("asteroid_destruction_large")
        elif self.radius > ASTEROID_MIN_RADIUS:
            self.sound_mixer.play("asteroid_destruction_medium")
        else:
            self.sound_mixer.play("asteroid_destruction_small")

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