import asyncio
import functools
import math
import random
import pygame

from constants import FRAMES_PER_SECOND
from constants import ASTEROID_KINDS
from constants import ASTEROID_MIN_RADIUS
from constants import MENU_TITLE
from constants import MENU_TITLE_FONT_SIZE
from constants import MENU_TEXT_COLOR
from constants import MENU_START_ASTEROIDS
from constants import MENU_BUTTON_TEXT
from constants import MENU_BUTTON_FONT_SIZE
from constants import MENU_BUTTON_WIDTH
from constants import MENU_BUTTON_HEIGHT
from constants import MENU_BUTTON_LINE_WIDTH
from constants import MENU_BUTTON_HOVER_COLOR
from constants import MENU_BUTTON_BOB_PIXELS
from constants import MENU_BUTTON_BOB_SPEED
from display import create_screen
from display import fit_to_window
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from sounds import SoundMixer


# Fonts are slow to create, so keep one per size
@functools.cache
def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font(None, size)


async def main():
    # Print statements to confirm main() is being called
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")

    # Initialize pygame
    pygame.init()

    # Initialize Screen
    screen = create_screen()
    print(f"Screen size: {screen.get_width()}x{screen.get_height()}")

    # Initialize Clock
    fps_clock = pygame.time.Clock()

    # Game cycle: main menu -> play until the player dies -> back to the main menu
    while True:
        if not await main_menu(fps_clock):
            return
        if not await play(fps_clock):
            return


async def main_menu(fps_clock: pygame.time.Clock) -> bool:
    """Show the main menu until START is pressed. Returns False if the window was closed."""

    # Initialize groups, the menu only has asteroids floating in the background
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroidfield = AsteroidField()

    # Start with some asteroids already on screen so the menu isn't empty
    width, height = pygame.display.get_surface().get_size()
    for _ in range(MENU_START_ASTEROIDS):
        radius = ASTEROID_MIN_RADIUS * random.randint(1, ASTEROID_KINDS)
        asteroid = Asteroid(random.uniform(0, width), random.uniform(0, height), radius)
        asteroid.velocity = pygame.Vector2(random.randint(40, 100), 0).rotate(random.uniform(0, 360))

    # Reset the clock so time spent elsewhere doesn't count as one big frame
    fps_clock.tick()
    elapsed = 0.0

    # Menu loop
    while True:
        dt = fps_clock.tick(FRAMES_PER_SECOND)/1000
        elapsed += dt

        screen = fit_to_window()
        width, height = screen.get_size()

        # The START button sits under the title and slowly bobs up and down
        button = pygame.Rect(0, 0, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        bob = math.sin(elapsed * MENU_BUTTON_BOB_SPEED) * MENU_BUTTON_BOB_PIXELS
        button.center = (width/2, height*0.55 + bob)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button.collidepoint(event.pos):
                return True
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return True

        updatable.update(dt)

        # Draw background asteroids
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)

        # Draw title, shrinking it on narrow screens so it still fits
        title_font = get_font(min(MENU_TITLE_FONT_SIZE, width // 5))
        title = title_font.render(MENU_TITLE, True, MENU_TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(width/2, height*0.3)))

        # Draw button, filled in while the mouse is over it
        if button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, MENU_BUTTON_HOVER_COLOR, button)
        pygame.draw.rect(screen, MENU_TEXT_COLOR, button, MENU_BUTTON_LINE_WIDTH)
        label = get_font(MENU_BUTTON_FONT_SIZE).render(MENU_BUTTON_TEXT, True, MENU_TEXT_COLOR)
        screen.blit(label, label.get_rect(center=button.center))

        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)


async def play(fps_clock: pygame.time.Clock) -> bool:
    """Play one game until the player dies. Returns False if the window was closed."""

    # Initialize groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Initialize a SoundMixer object
    sound_mixer = SoundMixer()

    # Set class attributes to group objects for updating, drawing, and collision detection
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    # Initialize AsteroidField to spawn asteroids from random screen edges
    asteroidfield = AsteroidField()

    # Initialize Player in the middle of the screen
    width, height = pygame.display.get_surface().get_size()
    player = Player(width/2, height/2)

    # Reset the clock so time spent in the menu doesn't count as one big frame
    fps_clock.tick()
    dt = 0.0

    # Game loop
    while True:
        # This logs the game state for review
        log_state()

        # Some variable we will use later
        dt = fps_clock.tick(FRAMES_PER_SECOND)/1000

        # For loop use to check for game events that need to be handled
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Escape quits back to the main menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

        screen = fit_to_window()

        # Draw screen background
        screen.fill("black")

        # Draw all sprites
        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                sound_mixer.play("player_death")
                log_event("player_hit")
                print("Game over!")
                await asyncio.sleep(2)
                return True

            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        for sprite in drawable:
            sprite.draw(screen)

        # Flip? I don't remember what this does
        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)

# Don't remember what this does. It shows up a lot in python programs
if __name__ == "__main__":
    asyncio.run(main())
