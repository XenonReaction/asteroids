import asyncio
import functools
import math
from collections.abc import Callable

import pygame

from constants import FRAMES_PER_SECOND
from constants import MENU_TITLE_FONT_SIZE
from constants import MENU_TEXT_COLOR
from constants import MENU_BUTTON_FONT_SIZE
from constants import MENU_BUTTON_WIDTH
from constants import MENU_BUTTON_HEIGHT
from constants import MENU_BUTTON_PADDING
from constants import MENU_BUTTON_SPACING
from constants import MENU_BUTTON_LINE_WIDTH
from constants import MENU_BUTTON_SELECTED_COLOR
from constants import MENU_BUTTON_BOB_PIXELS
from constants import MENU_BUTTON_BOB_SPEED
from constants import MENU_OVERLAY_OPACITY
from display import fit_to_window
from sounds import SoundMixer

# Keys for moving around menus and picking an option
UP_KEYS = (pygame.K_UP, pygame.K_w)
DOWN_KEYS = (pygame.K_DOWN, pygame.K_s)
LEFT_KEYS = (pygame.K_LEFT, pygame.K_a)
RIGHT_KEYS = (pygame.K_RIGHT, pygame.K_d)
PREVIOUS_KEYS = UP_KEYS + LEFT_KEYS
NEXT_KEYS = DOWN_KEYS + RIGHT_KEYS
SELECT_KEYS = (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER)


# Fonts are slow to create, so keep one per size
@functools.cache
def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font(None, size)


def draw_title(screen: pygame.Surface, text: str, center_y: float, opacity: int = 255) -> None:
    width = screen.get_width()
    title = get_font(MENU_TITLE_FONT_SIZE).render(text, True, MENU_TEXT_COLOR)

    # Shrink the title on narrow screens so it still fits
    if title.get_width() > width * 0.9:
        title = get_font(int(MENU_TITLE_FONT_SIZE * width * 0.9 / title.get_width())).render(text, True, MENU_TEXT_COLOR)

    title.set_alpha(opacity)
    screen.blit(title, title.get_rect(center=(width/2, center_y)))


def draw_shade(screen: pygame.Surface, opacity: int = MENU_OVERLAY_OPACITY) -> None:
    """Darken everything drawn so far so a menu on top stands out."""
    shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, opacity))
    screen.blit(shade, (0, 0))


async def timed_screen(
    fps_clock: pygame.time.Clock,
    seconds: float,
    draw_frame: Callable[[pygame.Surface, float], None],
) -> bool:
    """Show an animation for `seconds`. Nothing moves unless `draw_frame` moves it.

    `draw_frame` gets the screen and how far along the animation is, from 0 to 1.
    Returns False if the window was closed.
    """
    fps_clock.tick()
    elapsed = 0.0

    while elapsed < seconds:
        elapsed += fps_clock.tick(FRAMES_PER_SECOND)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen = fit_to_window()
        draw_frame(screen, min(elapsed / seconds, 1))

        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)

    return True


class ButtonMenu:
    """A column of buttons, moved between with WASD / arrow keys and picked with Space / Enter."""

    def __init__(self, options: list[str], bob: bool = False) -> None:
        self.options = options
        self.selected = 0
        self.bob = bob
        self.elapsed = 0.0
        self.sound_mixer = SoundMixer()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Returns the option that was picked, if any."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key in PREVIOUS_KEYS:
            self.selected = (self.selected - 1) % len(self.options)
            self.sound_mixer.play("menu_move")
        elif event.key in NEXT_KEYS:
            self.selected = (self.selected + 1) % len(self.options)
            self.sound_mixer.play("menu_move")
        elif event.key in SELECT_KEYS:
            self.sound_mixer.play("menu_select")
            return self.options[self.selected]

        return None

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def draw(self, screen: pygame.Surface, top: float) -> None:
        """Draw the buttons in a column, with the first one centered at `top`."""
        font = get_font(MENU_BUTTON_FONT_SIZE)
        labels = [font.render(option, True, MENU_TEXT_COLOR) for option in self.options]

        # All buttons are the same width, wide enough for the longest label
        width = max(MENU_BUTTON_WIDTH, max(label.get_width() for label in labels) + MENU_BUTTON_PADDING * 2)

        # Buttons can slowly bob up and down together
        bob = math.sin(self.elapsed * MENU_BUTTON_BOB_SPEED) * MENU_BUTTON_BOB_PIXELS if self.bob else 0

        for i, label in enumerate(labels):
            button = pygame.Rect(0, 0, width, MENU_BUTTON_HEIGHT)
            button.center = (screen.get_width()/2, top + bob + i * (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING))

            # Filled black so things behind don't show through, gray for the selected option
            fill = MENU_BUTTON_SELECTED_COLOR if i == self.selected else "black"
            pygame.draw.rect(screen, fill, button)
            pygame.draw.rect(screen, MENU_TEXT_COLOR, button, MENU_BUTTON_LINE_WIDTH)
            screen.blit(label, label.get_rect(center=button.center))


async def menu_screen(
    fps_clock: pygame.time.Clock,
    draw_scene: Callable[[pygame.Surface], None],
    title: str,
    options: list[str],
    escape_option: str | None = None,
) -> str | None:
    """Show a menu over the dimmed, frozen game until an option is picked.

    Pressing Escape picks `escape_option` if one is given. Returns None if the window was closed.
    """
    menu = ButtonMenu(options)

    while True:
        fps_clock.tick(FRAMES_PER_SECOND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if escape_option and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.sound_mixer.play("menu_select")
                return escape_option
            choice = menu.handle_event(event)
            if choice:
                return choice

        screen = fit_to_window()
        height = screen.get_height()

        # Draw the game underneath, darkened so the menu stands out
        draw_scene(screen)
        draw_shade(screen)

        draw_title(screen, title, height*0.35)
        menu.draw(screen, height*0.55)

        pygame.display.flip()

        # Hand control back to the browser each frame so the page doesn't freeze
        await asyncio.sleep(0)
