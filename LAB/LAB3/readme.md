# Bullet Frenzy 3D

![OpenGL](https://img.shields.io/badge/OpenGL-3D%20Game-blue) ![License](https://img.shields.io/badge/License-MIT-green)

A 3D arcade-style shooter game built with Python and OpenGL. Defend against relentless enemies while managing your ammo and lives!

## Game Description
Control a 3D character in an arena-style environment. Shoot incoming enemies to score points while avoiding collisions. Features multiple camera angles, pulsating enemies, and cheat modes.

**Key Mechanics:**
- Limited lives (5) and bullet allowance (10 missed shots)
- Progressive difficulty with faster enemies as score increases
- First-person and third-person perspectives
- Auto-aim cheat system

## Features
- 🎮 3D character with articulated arms and rotating gun
- 👾 5+ pulsating enemies with pursuit AI
- 🔫 Projectile bullet system with collision detection
- 🕹️ Two camera modes (FPS style and orbiting third-person)
- 💣 Cheat mode with auto-rotation and auto-fire
- 📊 Real-time HUD showing score/lives
- 🎯 Simple physics-based movement

## Controls
| Key | Action |
|-----|--------|
| W   | Move forward |
| S   | Move backward |
| A/D | Rotate character/gun |
| Mouse Left | Fire bullet |
| Mouse Right | Toggle camera |
| C   | Toggle cheat mode |
| V   | Camera mode (cheat only) |
| R   | Reset game |
| Arrows | Adjust camera angle/height |

## Installation
1. **Requirements:**
   - Python 3.x
   - OpenGL/GLUT libraries

2. **Install dependencies:**
   ```bash
   pip install PyOpenGL PyOpenGL-accelerate
