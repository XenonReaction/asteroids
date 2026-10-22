import asyncio
import random
from collections.abc import Callable

import pygame

from constants import FRAMES_PER_SECOND
from constants import PLAYER_RADIUS
from constants import ASTEROID_MAX_RADIUS
from constants import INTRO_FLY_IN_SECONDS
from constants import INTRO_SHIP_STOP_X
from constants import INTRO_ASTEROID_X
from constants import INTRO_ASTEROID_DRIFT_SPEED
from constants import INTRO_SHOOT_DELAY_SECONDS
from constants import INTRO_ASTEROID_PUSH_SPEED
from constants import INTRO_FLY_OFF_DELAY_SECONDS
from constants import INTRO_FLY_OFF_ACCELERATION
from constants import INTRO_FADE_OUT_SECONDS
from constants import WIN_ASTEROID_FADE_SECONDS
from constants import WIN_SPIN_CIRCLES
from constants import WIN_SPIN_DEGREES_PER_SECOND
from constants import WIN_SPIN_SPEED
from constants import WIN_FLY_OFF_ACCELERATION
from constants import WIN_FIREWORK_MIN_GAP_SECONDS
from constants import WIN_FIREWORK_MAX_GAP_SECONDS
from display import fit_to_window
from starfield import Starfield
from settings import Settings
from progress_bar import ProgressBar
from player import Player
from asteroid import Asteroid
from shot import Shot
from exhaust import Exhaust
from firework import Firework

# The parts of the cutscene, in order
FLY_IN = "fly in"
AIM = "aim"
SHOOTING = "shooting"
WAIT = "wait"
FLY_OFF = "fly off"
FADE_OUT = "fade out"
SPIN = "spin"

# The ship's rotation when its nose points to the right
FACING_RIGHT = -90


async def intro_cutscene(fps_clock: pygame.time.Clock, background: Starfield) -> bool:
    """The ship flies in from the left, shoots an asteroid, and flies off to the right.

    Any key or click skips it. Returns False if the window was closed.
    """

    # Initialize groups, effects are the exhaust dots
    updatable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    effects = pygame.sprite.Group()

    # The ship is moved by the cutscene instead of the keyboard, so it isn't in `updatable`
    Player.containers = ()
    Asteroid.containers = (asteroids, updatable)
    Shot.containers = (shots, updatable)
    Exhaust.containers = (effects, updatable)

    # Empty bar, so the ship is unfilled and the asteroid is the first color
    progress_bar = ProgressBar()
    Player.progress_bar = progress_bar
    Asteroid.progress_bar = progress_bar
    Asteroid.settings = Settings()

    width, height = pygame.display.get_surface().get_size()

    # The ship starts just off the left side, facing right
    start_x = -PLAYER_RADIUS * 2
    stop_x = width * INTRO_SHIP_STOP_X
    player = Player(start_x, height/2)
    player.rotation = FACING_RIGHT
    forward = pygame.Vector2(0, 1).rotate(player.rotation)

    # The biggest kind of asteroid, drifting toward the ship
    target = Asteroid(width * INTRO_ASTEROID_X, height/2, ASTEROID_MAX_RADIUS)
    target.velocity = -forward * INTRO_ASTEROID_DRIFT_SPEED

    phase = FLY_IN
    phase_time = 0.0  # seconds since the current part started
    fly_off_speed = 0.0

    def draw(screen: pygame.Surface) -> None:
        for asteroid in asteroids:
            asteroid.draw(screen)
        for effect in effects:
            effect.draw(screen)
        for shot in shots:
            shot.draw(screen)
        player.draw(screen)

    def next_phase(name: str) -> None:
        nonlocal phase, phase_time
        phase = name
        phase_time = 0.0

    # Reset the clock so loading time doesn't count as one big frame
    fps_clock.tick()

    while True:
        dt = fps_clock.tick(FRAMES_PER_SECOND)/1000
        phase_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.sound_mixer.engine(False)
                return False
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                player.sound_mixer.engine(False)
                return True

        screen = fit_to_window()
        moving = False

        if phase == FLY_IN:
            # Slow down smoothly as the ship reaches its stopping point
            progress = min(phase_time / INTRO_FLY_IN_SECONDS, 1)
            player.position.x = start_x + (stop_x - start_x) * (1 - (1 - progress) ** 3)
            moving = True
            if progress >= 1:
                next_phase(AIM)

        elif phase == AIM:
            if phase_time >= INTRO_SHOOT_DELAY_SECONDS:
                player.shoot()
                next_phase(SHOOTING)

        elif phase == SHOOTING:
            for shot in shots:
                if target.alive() and shot.collides_with(target):
                    shot.kill()
                    # Knock the pieces away from the ship as it breaks
                    target.velocity = forward * INTRO_ASTEROID_PUSH_SPEED
                    target.split()
            # Move on once the shot has hit (or flown off screen)
            if not shots:
                next_phase(WAIT)

        elif phase == WAIT:
            if phase_time >= INTRO_FLY_OFF_DELAY_SECONDS:
                next_phase(FLY_OFF)

        elif phase == FLY_OFF:
            fly_off_speed += INTRO_FLY_OFF_ACCELERATION * dt
            player.position += forward * fly_off_speed * dt
            off_screen = player.position.x > width + player.radius * 2
            moving = not off_screen
            # Wait for the exhaust to finish before fading out
            if off_screen and not effects:
                next_phase(FADE_OUT)

        elif phase == FADE_OUT:
            if phase_time >= INTRO_FADE_OUT_SECONDS:
                return True

        if moving:
            player.exhaust(dt, reversing=False)
        player.sound_mixer.engine(moving)

        updatable.update(dt)

        background.draw(screen)
        if phase == FADE_OUT:
            # Whatever is left fades away together on a see-through layer
            layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            draw(layer)
            layer.set_alpha(int(255 * (1 - phase_time / INTRO_FADE_OUT_SECONDS)))
            screen.blit(layer, (0, 0))
        else:
            draw(screen)

        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)


async def win_cutscene(
    fps_clock: pygame.time.Clock,
    player: Player,
    shots: pygame.sprite.Group,
    effects: pygame.sprite.Group,
    draw_frame: Callable[[pygame.Surface, float, float], None],
) -> bool:
    """The ship flies in circles, turns to face right, and flies off, launching fireworks the whole time.

    `effects` is the group the ship's exhaust and fireworks go into. `draw_frame` gets the
    screen, how far the asteroids have faded out, and how far the win message has faded in,
    both from 0 to 1. The win sound plays as the message starts fading in.
    Returns False if the window was closed.
    """
    width = pygame.display.get_surface().get_width()

    # Fly the full circles, then keep turning until the ship faces right
    turn_left = WIN_SPIN_CIRCLES * 360 + (FACING_RIGHT - player.rotation) % 360

    phase = SPIN
    elapsed = 0.0
    message_start = 0.0  # when the ship starts flying right
    message_seconds = player.sound_mixer.win_length()
    speed = WIN_SPIN_SPEED
    firework_timer = 0.0

    # Reset the clock so the freeze before this doesn't count as one big frame
    fps_clock.tick()

    while True:
        dt = fps_clock.tick(FRAMES_PER_SECOND)/1000
        elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.sound_mixer.engine(False)
                return False

        screen = fit_to_window()

        if phase == SPIN:
            # Turning while flying forward makes the ship go around in a circle
            turn = min(WIN_SPIN_DEGREES_PER_SECOND * dt, turn_left)
            player.rotation += turn
            turn_left -= turn
            if turn_left <= 0:
                # Facing right, head off and start fading in the message
                player.rotation = FACING_RIGHT
                phase = FLY_OFF
                message_start = elapsed
                player.sound_mixer.play("win")
        else:
            speed += WIN_FLY_OFF_ACCELERATION * dt

        forward = pygame.Vector2(0, 1).rotate(player.rotation)
        player.position += forward * speed * dt
        on_screen = player.position.x < width + player.radius * 2

        if on_screen:
            player.exhaust(dt, reversing=False)

            # Fireworks shoot out the back every so often
            firework_timer -= dt
            if firework_timer <= 0:
                Firework(player.position - forward * player.radius, -forward)
                firework_timer = random.uniform(WIN_FIREWORK_MIN_GAP_SECONDS, WIN_FIREWORK_MAX_GAP_SECONDS)
        player.sound_mixer.engine(on_screen)

        shots.update(dt)
        effects.update(dt)

        asteroid_fade = min(elapsed / WIN_ASTEROID_FADE_SECONDS, 1)
        message_fade = min((elapsed - message_start) / message_seconds, 1) if phase == FLY_OFF else 0
        draw_frame(screen, asteroid_fade, message_fade)

        pygame.display.flip()

        # Done once the ship is gone, the last firework has faded, and the message is all the way in
        if phase == FLY_OFF and not on_screen and not effects and message_fade >= 1 and asteroid_fade >= 1:
            return True

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)
