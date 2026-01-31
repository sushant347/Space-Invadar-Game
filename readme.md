# Space Invader Game
Space Invader is a classic arcade game where players control a spaceship to defend against waves of alien invaders. The objective is to shoot down the aliens while avoiding their attacks. The game features simple controls, retro graphics, and increasing difficulty levels as players progress.

## 🎮 Play Online
Play the game directly in your browser: [Play Space Invader](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/)

## Features
- Classic arcade gameplay
- Retro graphics and sound effects
- Power-ups and special weapons
- Multiple levels with increasing difficulty
- High score tracking

## How to Play
1. Use the arrow keys to move your spaceship left and right.
2. Press the spacebar to shoot at the alien invaders.
3. Avoid enemy fire and prevent the aliens from reaching the bottom of the screen.
4. Collect power-ups to enhance your weapons and defenses.
5. Aim for a high score by defeating as many aliens as possible.

## Installation (Local)
1. Download the game files from the repository.
2. Open the main.py file using Python 3.x.
3. Run the game and enjoy!

## 🌐 Web Hosting with pygbag

This game is configured to run in the browser using **pygbag**.

### Test Locally
```bash
pip install pygbag
pygbag "space invader game"
```
Then open `http://localhost:8000` in your browser.

### Build for Deployment
```bash
pygbag --build "space invader game"
```
The built files will be in `space invader game/build/web/`