import pygame

from constants import PROGRESS_BAR_COLORS
from constants import PROGRESS_BAR_MAX
from constants import PROGRESS_BAR_HEIGHT
from constants import PROGRESS_BAR_MARGIN
from constants import PROGRESS_BAR_LINE_WIDTH
from constants import PROGRESS_BAR_BACKGROUND_COLOR


class ProgressBar:
    """Bar across the top of the screen that fills up as asteroids are split.

    The bar is split into equal sections, one per color. How full it is decides the
    color of the asteroids.
    """

    def __init__(self) -> None:
        self.count = 0

    def add(self, amount: int) -> None:
        self.count = min(self.count + amount, PROGRESS_BAR_MAX)

    def fraction(self) -> float:
        return self.count / PROGRESS_BAR_MAX

    def section_index(self) -> int:
        # Which section the fill has reached, the last one once full
        index = int(self.fraction() * len(PROGRESS_BAR_COLORS))
        return min(index, len(PROGRESS_BAR_COLORS) - 1)

    def current_color(self) -> str:
        return PROGRESS_BAR_COLORS[self.section_index()]

    def filled_sections(self, up_to: float | None = None) -> list[tuple[str, float, float]]:
        """(color, start, end) of each colored part of the fill, as fractions (0 to 1) of the whole bar.

        Goes up to how full the bar is, or up to `up_to` if it's given.
        """
        if up_to is None:
            up_to = self.fraction()

        sections = []
        section_size = 1 / len(PROGRESS_BAR_COLORS)

        for i, color in enumerate(PROGRESS_BAR_COLORS):
            start = i * section_size
            end = min(start + section_size, up_to)
            if end <= start:
                break
            sections.append((color, start, end))

        return sections

    def draw(self, screen: pygame.Surface) -> None:
        width = screen.get_width() - PROGRESS_BAR_MARGIN * 2
        outline = pygame.Rect(PROGRESS_BAR_MARGIN, PROGRESS_BAR_MARGIN, width, PROGRESS_BAR_HEIGHT)
        corner_radius = PROGRESS_BAR_HEIGHT // 2

        # Dark background for the empty part of the bar
        pygame.draw.rect(screen, PROGRESS_BAR_BACKGROUND_COLOR, outline, border_radius=corner_radius)

        # The fill shows the colors up to how full the bar is, matching the border above it
        screen.blit(self.colored_shape(outline.size, self.fraction()), outline.topleft)

        # The border shows every color from the start
        screen.blit(self.colored_shape(outline.size, 1, PROGRESS_BAR_LINE_WIDTH), outline.topleft)

    def colored_shape(self, size: tuple[int, int], up_to: float, line_width: int = 0) -> pygame.Surface:
        """The bar's colored sections up to `up_to`, cut to the rounded bar shape.

        A `line_width` of 0 gives the whole shape, anything else gives just its outline.
        """
        width, height = size

        # Draw the colors one section at a time
        colors = pygame.Surface(size, pygame.SRCALPHA)
        for color, start, end in self.filled_sections(up_to):
            pygame.draw.rect(colors, color, (start * width, 0, (end - start) * width + 1, height))

        # Cut the colors to the rounded shape so the corners don't stick out
        shape = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(shape, "white", shape.get_rect(), line_width, border_radius=height // 2)
        colors.blit(shape, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        return colors
