import pygame

from constants import PLAYER_RADIUS
from constants import PLAYER_COLOR
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from constants import PLAYER_SHOOT_SPEED
from constants import PLAYER_SHOOT_COOLDWON_SECONDS
from constants import LINE_WIDTH

from sounds import SoundMixer
from progress_bar import ProgressBar

from circleshape import CircleShape
from shot import Shot


def clip_to_band(points: list[pygame.Vector2], origin: pygame.Vector2, direction: pygame.Vector2,
                 low: float, high: float) -> list[pygame.Vector2]:
    """Cut a polygon down to the part that is between `low` and `high` distance along `direction` from `origin`."""
    # Cut once at the low end and once at the high end
    for limit, keep_beyond in ((low, True), (high, False)):
        def inside(point: pygame.Vector2) -> float:
            # Positive when the point is on the side being kept
            distance = (point - origin).dot(direction) - limit
            return distance if keep_beyond else -distance

        clipped = []
        for i, point in enumerate(points):
            next_point = points[(i + 1) % len(points)]
            here, there = inside(point), inside(next_point)
            if here >= 0:
                clipped.append(point)
            # The edge crosses the cut line, so add the point where it crosses
            if (here >= 0) != (there >= 0):
                clipped.append(point + (next_point - point) * (here / (here - there)))
        points = clipped

    return points


class Player(CircleShape):
    # Set by the game, the ship fills with its colors as the bar fills
    progress_bar: ProgressBar

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cool_down_timer = 0
        self.sound_mixer = SoundMixer()

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: "Screen") -> None:
        # Fill the ship like the progress bar, starting at the back and moving toward the nose
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        back = self.position - forward * self.radius
        length = self.radius * 2

        for color, start, end in self.progress_bar.filled_sections():
            band = clip_to_band(self.triangle(), back, forward, start * length, end * length)
            if len(band) >= 3:
                pygame.draw.polygon(screen, color, band)

        pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-1 * dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-1 * dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.cool_down_timer -= dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        if self.cool_down_timer <= 0:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0,1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity *= PLAYER_SHOOT_SPEED
            self.cool_down_timer = PLAYER_SHOOT_COOLDWON_SECONDS
            self.sound_mixer.play("shot")
