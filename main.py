import pygame

from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from constants import FRAMES_PER_SECOND
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    # Print statements to confirm main() is being called
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame
    pygame.init()

    # Initialize groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Set static container fields
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    # Initialize AsteroidField
    asteroidfield = AsteroidField()

    # Initialize Clock
    fps_clock = pygame.time.Clock()
    dt = 0.0

    # Initialize Player
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # Initialize Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game loop
    while True: 
        # This logs the game state for review
        log_state()

        # Some variable we will use later
        dt = fps_clock.tick(FRAMES_PER_SECOND)/1000

        # For loop use to check for game events that need to be handled
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Draw screen background
        screen.fill("black")

        # Draw player
        updatable.update(dt)
        for sprite in drawable:
            sprite.draw(screen)

        # Flip? I don't remember what this does
        pygame.display.flip()

# Don't remember what this does. It shows up a lot in python programs
if __name__ == "__main__":
    main()
