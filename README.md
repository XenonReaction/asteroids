# Asteroids

An Asteroids game made with Python and pygame that runs in the browser.

**Play it here: https://xenonreaction.github.io/asteroids/**

Click the page once it loads to start (browsers need a click before they play sound).

## How to play

Shoot asteroids to fill the progress bar at the top of the screen. Every asteroid you split adds to the bar, and filling it wins the game. As the bar fills, the asteroids change color and come at you faster and more often. Touching an asteroid sends you back to the main menu.

## Settings

Pick **SETTINGS** on the main menu to set the difficulty. Each setting has a row of squares numbered 1 (easiest) to 10 (hardest), and all of them start at 1. Move the yellow cursor to a number and press Space or Enter to choose it. The chosen number is filled in white.

| Setting | What it changes | 1 | 10 |
| --- | --- | --- | --- |
| Number of asteroids | How often new asteroids appear | half as often as normal | 2.8x as often |
| Asteroid speed | How fast new asteroids move | 0.6x normal speed | 2.35x as fast |
| Asteroid destruction value | How much each split fills the bar | 10 points (50 splits to win) | 1 point (500 splits to win) |

These stack with the speed-up that happens as the bar fills. Settings last until you reload the page.

When you win, your score is the three settings added together, out of 30. Harder settings give a higher score.

## Controls

| Action | Keys |
| --- | --- |
| Turn | A / D or Left / Right |
| Move forward / backward | W / S or Up / Down |
| Shoot | Space |
| Pause | Escape |
| Move between menu options | W / A / S / D or arrow keys |
| Pick a menu option | Space or Enter |
| Move along a setting's numbers | A / D or Left / Right |
| Choose a setting's number | Space or Enter |
| Leave the settings screen | Escape, or pick Back |

## Running it on your computer

Requires Python 3.13 or newer.

```bash
uv sync
uv run main.py
```

Or without uv:

```bash
pip install pygame==2.6.1
python main.py
```

## How the web version works

Every push to `main` runs a GitHub Actions workflow (`.github/workflows/pages.yml`) that packages the game for the browser with [pygbag](https://github.com/pygame-web/pygbag) and publishes it to GitHub Pages.

To try the browser version locally before pushing:

```bash
pip install pygbag
pygbag .
```

Then open http://localhost:8000.

Sound files must be `.ogg`. pygbag refuses to build if any `.mp3` files are in the project.
