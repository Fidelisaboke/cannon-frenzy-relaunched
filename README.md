# Cannon Frenzy - Relaunched

**Cannon Frenzy - Relaunched** is an engaging and fast-paced 2D artillery adventure game built using PyGame. Control a cannon, aim with precision, and hit targets across dynamic environments to achieve high scores.

This project is a modern relaunch and standalone extension of the original [Cannon Frenzy](https://github.com/Twna-Jane/Cannon-Frenzy), featuring a refined codebase, a combo scoring system, and updated visuals.

## Table of Contents

1. [Features](#features)
2. [Setup Instructions](#setup-instructions)
3. [How to Play](#how-to-play)
4. [Project Structure](#project-structure)
5. [License](#license)

## Features

- **Interactive Gameplay**: Precision-based cannon control with physics-driven projectiles.
- **Dynamic Environments**: Battle across different terrains including **Grasslands** and **Deserts** that change as you progress.
- **Combo Scoring System**: Earn bonus points by hitting targets in quick succession without missing.
- **Progressive Difficulty**: Levels increase in complexity with moving targets and limited ammunition.
- **Retro Visuals & Sound**: Immersive pixel-art backgrounds and a curated soundtrack.

## Setup Instructions

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

### Prerequisites

- **Python 3.13+**
- **uv** (Recommended) or **pip**

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Fidelisaboke/cannon-frenzy-relaunched.git
   cd cannon-frenzy-relaunched
   ```

2. **Sync dependencies**:
   Using `uv`, this will automatically create a virtual environment and install all required packages:
   ```bash
   uv sync
   ```

## Basic Usage

To launch the game, simply run:

```bash
uv run cannon-frenzy
```

Alternatively, you can run the module directly:
```bash
uv run python -m cannon_frenzy
```

## How to Play

### Objective
Aim and shoot your cannon to hit all targets in each level. You have a limited number of cannonballs per level—don't run out!

### Controls
- **Arrow Keys (Left/Right)**: Adjust the cannon's angle.
- **Spacebar**: Fire a cannonball.
- **'R' Key**: Restart the game (on Game Over screen).
- **'M' Key**: Return to the Main Menu (on Game Over screen).

### Scoring
- **Base Score**: 10 points per target hit.
- **Combo Bonus**: Each consecutive hit increases your combo. Points are calculated as `10 + 5 * (combo - 1)`. 
- **Streak**: Your maximum combo streak is tracked throughout the game.

## Project Structure

```
.
├── assets/             # Game assets (audio, images)
│   ├── audio/          # Sound effects and music
│   └── images/         # Sprites and backgrounds
├── src/
│   └── cannon_frenzy/  # Main package
│       ├── core/       # Game engine and sound management
│       ├── entities/   # Game objects (Cannon, Ball, Target)
│       ├── scenes/     # UI screens (Menu, Level, Scoreboard)
│       ├── config/     # Constants and level definitions
│       └── utils/      # Helper functions (Path handling)
├── tests/              # Unit tests
├── pyproject.toml      # Project configuration and dependencies
└── uv.lock             # Dependency lockfile
```

## License

This project is licensed under the [MIT License](LICENSE). See the file for details.
