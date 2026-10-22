# Asteroids

An Asteroids game made with Python and pygame that runs in the browser.

**Play it here: https://xenonreaction.github.io/asteroids/**

Click the page once it loads to start (browsers need a click before they play sound).

## How to play

Shoot asteroids to fill the progress bar at the top of the screen. Every asteroid you split adds to the bar, and filling it wins the game. As the bar fills, the asteroids change color and come at you faster and more often. Touching an asteroid sends you back to the main menu.

## Controls

| Action | Keys |
| --- | --- |
| Turn | A / D or Left / Right |
| Move forward / backward | W / S or Up / Down |
| Shoot | Space |
| Pause | Escape |
| Move between menu options | W / A / S / D or arrow keys |
| Pick a menu option | Space or Enter (or click) |

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
