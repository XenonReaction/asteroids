import asyncio
import random
import pygame

from constants import FRAMES_PER_SECOND
from constants import ASTEROID_KINDS
from constants import ASTEROID_MIN_RADIUS
from constants import MENU_TITLE
from constants import MENU_START_ASTEROIDS
from constants import MENU_OVERLAY_OPACITY
from constants import MENU_BUTTON_TEXT
from constants import MENU_SETTINGS_TEXT
from constants import SETTINGS_TITLE
from constants import SETTINGS_BACK_TEXT
from constants import PAUSE_TITLE
from constants import PAUSE_CONTINUE_TEXT
from constants import PAUSE_QUIT_TEXT
from constants import WIN_TITLE
from constants import WIN_PLAY_AGAIN_TEXT
from constants import WIN_EXIT_TEXT
from constants import WIN_FREEZE_SECONDS
from constants import WIN_HOLD_SECONDS
from display import create_screen
from display import fit_to_window
from menu import ButtonMenu
from menu import draw_title
from menu import draw_shade
from menu import menu_screen
from menu import timed_screen
from starfield import Starfield
from settings import Settings
from settings import SettingsMenu
from progress_bar import ProgressBar
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from sounds import SoundMixer

# What play() can end with
BACK_TO_MENU = "menu"
PLAY_AGAIN = "play again"
WINDOW_CLOSED = "closed"


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

    # Difficulty, changed in the settings menu and kept until the page is reloaded
    settings = Settings()

    # Game cycle: main menu -> play until the player dies, wins, or quits -> back to the main menu
    while True:
        # New background each time the main menu loads, kept for the games that follow
        background = Starfield(*pygame.display.get_surface().get_size())

        if not await main_menu(fps_clock, background, settings):
            return

        result = PLAY_AGAIN
        while result == PLAY_AGAIN:
            result = await play(fps_clock, background, settings)

        if result == WINDOW_CLOSED:
            return


async def main_menu(fps_clock: pygame.time.Clock, background: Starfield, settings: Settings) -> bool:
    """Show the main menu until START is picked. Returns False if the window was closed.

    SETTINGS opens the settings menu in place of the buttons, and changes are saved into `settings`.
    """

    # Initialize groups, the menu only has asteroids floating in the background
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    # Menu asteroids never split, so they keep the empty bar's color and speed
    menu_progress_bar = ProgressBar()
    Asteroid.progress_bar = menu_progress_bar
    AsteroidField.progress_bar = menu_progress_bar

    # Menu asteroids always use the easiest settings so the menu stays calm
    Asteroid.settings = Settings()
    AsteroidField.settings = Asteroid.settings

    asteroidfield = AsteroidField()

    # Start with some asteroids already on screen so the menu isn't empty
    width, height = pygame.display.get_surface().get_size()
    for _ in range(MENU_START_ASTEROIDS):
        radius = ASTEROID_MIN_RADIUS * random.randint(1, ASTEROID_KINDS)
        asteroid = Asteroid(random.uniform(0, width), random.uniform(0, height), radius)
        asteroid.velocity = pygame.Vector2(random.randint(40, 100), 0).rotate(random.uniform(0, 360))

    # The buttons sit under the title and slowly bob up and down
    menu = ButtonMenu([MENU_BUTTON_TEXT, MENU_SETTINGS_TEXT], bob=True)
    settings_menu = SettingsMenu(settings)
    showing_settings = False

    # Reset the clock so time spent elsewhere doesn't count as one big frame
    fps_clock.tick()

    # Menu loop
    while True:
        dt = fps_clock.tick(FRAMES_PER_SECOND)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if showing_settings:
                if settings_menu.handle_event(event) == SETTINGS_BACK_TEXT:
                    showing_settings = False
            else:
                choice = menu.handle_event(event)
                if choice == MENU_BUTTON_TEXT:
                    return True
                if choice == MENU_SETTINGS_TEXT:
                    showing_settings = True

        screen = fit_to_window()
        height = screen.get_height()

        updatable.update(dt)
        menu.update(dt)

        # Draw background stars and asteroids
        background.draw(screen)
        for sprite in drawable:
            sprite.draw(screen)

        if showing_settings:
            draw_title(screen, SETTINGS_TITLE, height*0.2)
            settings_menu.draw(screen, height*0.4)
        else:
            draw_title(screen, MENU_TITLE, height*0.3)
            menu.draw(screen, height*0.55)

        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)


async def play(fps_clock: pygame.time.Clock, background: Starfield, settings: Settings) -> str:
    """Play one game. Returns BACK_TO_MENU, PLAY_AGAIN, or WINDOW_CLOSED."""

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

    # Each game starts with an empty progress bar
    progress_bar = ProgressBar()
    Asteroid.progress_bar = progress_bar
    AsteroidField.progress_bar = progress_bar
    Player.progress_bar = progress_bar

    # Use the difficulty picked in the settings menu
    Asteroid.settings = settings
    AsteroidField.settings = settings

    # Initialize AsteroidField to spawn asteroids from random screen edges
    asteroidfield = AsteroidField()

    # Initialize Player in the middle of the screen
    width, height = pygame.display.get_surface().get_size()
    player = Player(width/2, height/2)

    def draw_game(screen: pygame.Surface, asteroid_opacity: int = 255) -> None:
        background.draw(screen)

        if asteroid_opacity == 255:
            for asteroid in asteroids:
                asteroid.draw(screen)
        else:
            # Fading asteroids are drawn together on a see-through layer
            layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            for asteroid in asteroids:
                asteroid.draw(layer)
            layer.set_alpha(asteroid_opacity)
            screen.blit(layer, (0, 0))

        # Player and shots go on top of the asteroids
        for sprite in drawable:
            if sprite not in asteroids:
                sprite.draw(screen)

        # Draw the progress bar last so it's on top of everything
        progress_bar.draw(screen)

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
                return WINDOW_CLOSED

            # Escape pauses the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choice = await menu_screen(fps_clock, draw_game, PAUSE_TITLE,
                                           [PAUSE_CONTINUE_TEXT, PAUSE_QUIT_TEXT],
                                           escape_option=PAUSE_CONTINUE_TEXT)
                if choice is None:
                    return WINDOW_CLOSED
                if choice == PAUSE_QUIT_TEXT:
                    return BACK_TO_MENU

                # Don't count the time spent paused
                fps_clock.tick()

        screen = fit_to_window()

        # Update all sprites
        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                sound_mixer.play("player_death")
                log_event("player_hit")
                print("Game over!")
                await asyncio.sleep(2)
                return BACK_TO_MENU

            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        # Filling the bar wins the game
        if progress_bar.fraction() >= 1:
            log_event("player_won")

            # Everything freezes in place for a moment
            if not await timed_screen(fps_clock, WIN_FREEZE_SECONDS, lambda screen, t: draw_game(screen)):
                return WINDOW_CLOSED

            # While the win sound plays, the asteroids fade out and the message fades in
            def fade(screen: pygame.Surface, t: float) -> None:
                draw_game(screen, asteroid_opacity=int(255 * (1 - t)))
                draw_shade(screen, int(MENU_OVERLAY_OPACITY * t))
                draw_title(screen, WIN_TITLE, screen.get_height()*0.35, opacity=int(255 * t))

            sound_mixer.play("win")
            if not await timed_screen(fps_clock, sound_mixer.win_length(), fade):
                return WINDOW_CLOSED

            # The asteroids have faded away
            for asteroid in asteroids:
                asteroid.kill()

            # Hold on the message before showing the buttons
            def hold(screen: pygame.Surface, t: float) -> None:
                draw_game(screen)
                draw_shade(screen)
                draw_title(screen, WIN_TITLE, screen.get_height()*0.35)

            if not await timed_screen(fps_clock, WIN_HOLD_SECONDS, hold):
                return WINDOW_CLOSED

            choice = await menu_screen(fps_clock, draw_game, WIN_TITLE,
                                       [WIN_PLAY_AGAIN_TEXT, WIN_EXIT_TEXT])
            if choice is None:
                return WINDOW_CLOSED
            if choice == WIN_PLAY_AGAIN_TEXT:
                return PLAY_AGAIN
            return BACK_TO_MENU

        draw_game(screen)

        # Flip? I don't remember what this does
        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)

# Don't remember what this does. It shows up a lot in python programs
if __name__ == "__main__":
    asyncio.run(main())
