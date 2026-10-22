from dataclasses import dataclass

import pygame

from constants import SETTING_MIN
from constants import SETTING_MAX
from constants import SETTINGS_ASTEROID_AMOUNT_EASIEST
from constants import SETTINGS_ASTEROID_AMOUNT_HARDEST
from constants import SETTINGS_ASTEROID_SPEED_EASIEST
from constants import SETTINGS_ASTEROID_SPEED_HARDEST
from constants import SETTINGS_FONT_SIZE
from constants import SETTINGS_SQUARE_SIZE
from constants import SETTINGS_SQUARE_GAP
from constants import SETTINGS_SQUARE_LINE_WIDTH
from constants import SETTINGS_LABEL_GAP
from constants import SETTINGS_ROW_SPACING
from constants import SETTINGS_CHOSEN_COLOR
from constants import SETTINGS_CURSOR_COLOR
from constants import SETTINGS_CURSOR_LINE_WIDTH
from constants import SETTINGS_INACTIVE_TEXT_COLOR
from constants import MENU_TEXT_COLOR
from constants import MENU_BUTTON_WIDTH
from constants import MENU_BUTTON_HEIGHT
from constants import MENU_BUTTON_LINE_WIDTH
from constants import MENU_BUTTON_SELECTED_COLOR
from constants import version
from menu import get_font
from menu import UP_KEYS
from menu import DOWN_KEYS
from menu import LEFT_KEYS
from menu import RIGHT_KEYS
from menu import SELECT_KEYS
from sounds import SoundMixer


def between(easiest: float, hardest: float, setting: int) -> float:
    """The value for a setting, spread evenly from `easiest` at 1 to `hardest` at 10."""
    fraction = (setting - SETTING_MIN) / (SETTING_MAX - SETTING_MIN)
    return easiest + (hardest - easiest) * fraction


@dataclass
class Settings:
    """Difficulty picked in the settings menu. Every setting goes from 1 (easiest) to 10 (hardest)."""

    asteroid_amount: int = SETTING_MIN
    asteroid_speed: int = SETTING_MIN
    destruction_value: int = SETTING_MIN

    def spawn_multiplier(self) -> float:
        # How many times more often asteroids spawn than normal
        return between(SETTINGS_ASTEROID_AMOUNT_EASIEST, SETTINGS_ASTEROID_AMOUNT_HARDEST, self.asteroid_amount)

    def speed_multiplier(self) -> float:
        # How many times faster asteroids move than normal
        return between(SETTINGS_ASTEROID_SPEED_EASIEST, SETTINGS_ASTEROID_SPEED_HARDEST, self.asteroid_speed)

    def split_points(self) -> int:
        # Setting 1 is worth the most (10 points per split) and setting 10 the least (1 point),
        # so a higher setting is always harder
        return SETTING_MAX + 1 - self.destruction_value

    def score(self) -> int:
        # Harder settings give a higher score
        return self.asteroid_amount + self.asteroid_speed + self.destruction_value

    @staticmethod
    def max_score() -> int:
        return SETTING_MAX * len(SETTING_ROWS)


# The Settings attribute each row changes, in order from top to bottom
SETTING_ROWS = ["asteroid_amount", "asteroid_speed", "destruction_value"]


def setting_labels() -> list[str]:
    # The label shown for each row, in the same order as SETTING_ROWS
    return [
        version().SETTINGS_ASTEROID_AMOUNT_TEXT,
        version().SETTINGS_ASTEROID_SPEED_TEXT,
        version().SETTINGS_DESTRUCTION_VALUE_TEXT,
    ]


class SettingsMenu:
    """A label and a row of numbered squares (1 to 10) for each setting, then a Back button.

    W / S or Up / Down move between rows. A / D or Left / Right move the cursor along a row,
    and Space or Enter sets that row to the number the cursor is on.
    """

    # Returned by handle_event when the player leaves the settings menu
    BACK = "back"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.sound_mixer = SoundMixer()
        self.select_row(0)

    def on_back(self) -> bool:
        return self.row == len(SETTING_ROWS)

    def value(self, row: int) -> int:
        return getattr(self.settings, SETTING_ROWS[row])

    def select_row(self, row: int) -> None:
        # One row per setting, plus the Back button
        self.row = row % (len(SETTING_ROWS) + 1)

        # The cursor starts on the row's current value
        if not self.on_back():
            self.cursor = self.value(self.row)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Returns SettingsMenu.BACK when the player leaves the settings menu."""
        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            self.sound_mixer.play("menu_select")
            return self.BACK

        if event.key in UP_KEYS:
            self.select_row(self.row - 1)
            self.sound_mixer.play("menu_move")
        elif event.key in DOWN_KEYS:
            self.select_row(self.row + 1)
            self.sound_mixer.play("menu_move")
        elif not self.on_back() and event.key in LEFT_KEYS and self.cursor > SETTING_MIN:
            self.cursor -= 1
            self.sound_mixer.play("menu_move")
        elif not self.on_back() and event.key in RIGHT_KEYS and self.cursor < SETTING_MAX:
            self.cursor += 1
            self.sound_mixer.play("menu_move")
        elif event.key in SELECT_KEYS:
            self.sound_mixer.play("menu_select")
            if self.on_back():
                return self.BACK
            setattr(self.settings, SETTING_ROWS[self.row], self.cursor)

        return None

    def draw(self, screen: pygame.Surface, top: float) -> None:
        """Draw the rows in a column, with the first one centered at `top`."""
        screen_width = screen.get_width()
        labels = setting_labels()
        square_count = SETTING_MAX - SETTING_MIN + 1

        # Everything shrinks together on narrow screens so the rows still fit
        label_width = max(get_font(SETTINGS_FONT_SIZE).size(label)[0] for label in labels)
        squares_width = square_count * SETTINGS_SQUARE_SIZE + (square_count - 1) * SETTINGS_SQUARE_GAP
        full_width = label_width + SETTINGS_LABEL_GAP + squares_width
        scale = min(1.0, screen_width * 0.95 / full_width)

        font = get_font(int(SETTINGS_FONT_SIZE * scale))
        square_size = SETTINGS_SQUARE_SIZE * scale
        square_gap = SETTINGS_SQUARE_GAP * scale
        row_step = square_size + SETTINGS_ROW_SPACING * scale

        label_width = max(font.size(label)[0] for label in labels)
        left = (screen_width - full_width * scale) / 2
        squares_left = left + label_width + SETTINGS_LABEL_GAP * scale

        for i, label in enumerate(labels):
            center_y = top + i * row_step
            active = i == self.row

            # The label of the row being changed is brighter than the others
            label_color = MENU_TEXT_COLOR if active else SETTINGS_INACTIVE_TEXT_COLOR
            text = font.render(label, True, label_color)
            screen.blit(text, text.get_rect(midleft=(left, center_y)))

            for number in range(SETTING_MIN, SETTING_MAX + 1):
                square = pygame.Rect(0, 0, square_size, square_size)
                square.midleft = (squares_left + (number - SETTING_MIN) * (square_size + square_gap), center_y)

                # The current value is filled in, the cursor gets a thick colored border
                chosen = number == self.value(i)
                under_cursor = active and number == self.cursor

                fill = SETTINGS_CHOSEN_COLOR if chosen else ("gray30" if under_cursor else "black")
                pygame.draw.rect(screen, fill, square)

                if under_cursor:
                    pygame.draw.rect(screen, SETTINGS_CURSOR_COLOR, square, max(1, int(SETTINGS_CURSOR_LINE_WIDTH * scale)))
                else:
                    pygame.draw.rect(screen, MENU_TEXT_COLOR, square, max(1, int(SETTINGS_SQUARE_LINE_WIDTH * scale)))

                number_color = "black" if chosen else MENU_TEXT_COLOR
                number_text = font.render(str(number), True, number_color)
                screen.blit(number_text, number_text.get_rect(center=square.center))

        # Back button, filled gray while it's selected
        back = pygame.Rect(0, 0, MENU_BUTTON_WIDTH * scale, MENU_BUTTON_HEIGHT * scale)
        back.center = (screen_width / 2, top + len(SETTING_ROWS) * row_step + MENU_BUTTON_HEIGHT * scale / 2)
        pygame.draw.rect(screen, MENU_BUTTON_SELECTED_COLOR if self.on_back() else "black", back)
        pygame.draw.rect(screen, MENU_TEXT_COLOR, back, MENU_BUTTON_LINE_WIDTH)
        back_text = font.render(version().SETTINGS_BACK_TEXT, True, MENU_TEXT_COLOR)
        screen.blit(back_text, back_text.get_rect(center=back.center))
