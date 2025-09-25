# 🏚️ Scarebnb - Haunted Mansion Adventure

A thrilling 3D horror-adventure game built with Python and OpenGL where you explore a haunted mansion, collect treasures, and battle supernatural entities.

![Game Genre](https://img.shields.io/badge/Genre-Horror%20Adventure-red)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenGL](https://img.shields.io/badge/OpenGL-Required-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 📖 Overview

Welcome to **Scarebnb**, where your worst nightmares come to life! Navigate through a sprawling haunted mansion filled with multiple interconnected rooms, each harboring its own dark secrets. Your mission: collect 5 precious treasures while avoiding or defeating 10 hostile ghosts that roam the corridors. But beware—once you've gathered all treasures, you'll face the ultimate challenge: a terrifying boss battle that will test your survival skills!

## 🎮 Game Features

### 🏰 **Immersive 3D Environment**
- **Multi-room mansion** with 7 distinct rooms and connecting hallways
- **Realistic 3D graphics** rendered with OpenGL
- **Dynamic lighting** and atmospheric effects
- **Detailed textures** including wooden floors, cobwebs, and haunting decorations

### 👻 **Supernatural Entities**
- **10 AI-driven ghosts** that actively hunt the player
- **Intelligent ghost behavior** - they track and chase you throughout the mansion
- **Pulsating ghost animations** with glowing red eyes
- **Epic boss battle** with unique attack patterns and projectiles

### 🎯 **Combat System**
- **Laser shooting mechanics** - left-click to fire
- **Strategic combat** - defeat ghosts to clear your path
- **Boss battle** with health system and multiple attack phases
- **Player health system** - start with 5 lives

### 🏆 **Treasure Hunt**
- **5 treasures** scattered throughout the mansion
- **Score tracking system**
- **Progressive difficulty** - boss fight unlocks after collecting all treasures
- **Victory conditions** - defeat the boss to win

### 🎮 **Advanced Controls**
- **WASD movement** system for smooth navigation
- **Mouse-controlled shooting** with directional aiming
- **Jumping mechanics** with spacebar
- **Multiple camera modes** including first-person view
- **Cheat mode** for testing and exploration

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x installed on your system
- OpenGL libraries (included in the OpenGL.zip file)

### Installation Steps

1. **Download the game files** to your desired directory

2. **Extract OpenGL dependencies**:
   ```
   📁 Extract OpenGL.zip to the game directory
   📁 Place Scarebnb.py inside the extracted OpenGL folder
   ```
   
   **⚠️ IMPORTANT**: The game file (`Scarebnb.py`) **MUST** be placed inside the extracted OpenGL folder for the game to run properly. The OpenGL libraries are essential dependencies that the game requires to function.

3. **Verify your directory structure**:
   ```
   📁 Your Game Folder/
   ├── 📁 OpenGL/ (extracted from OpenGL.zip)
   │   ├── 📄 Scarebnb.py (place the game file here)
   │   ├── 📁 GL/
   │   ├── 📁 GLUT/
   │   ├── 📁 GLU/
   │   └── ... (other OpenGL files)
   └── 📄 README.md
   ```

4. **Run the game**:
   ```bash
   cd path/to/OpenGL/folder
   python Scarebnb.py
   ```

## 🎮 Controls

| Key/Action | Function |
|------------|----------|
| **W** | Move forward |
| **A** | Move left |
| **S** | Move backward |
| **D** | Move right |
| **Spacebar** | Jump |
| **Left Mouse Click** | Fire laser |
| **Right Mouse Click** | Toggle first-person camera mode |
| **C** | Toggle cheat mode |
| **R** | Restart game |
| **Arrow Keys** | Adjust camera position |

## 🎯 Gameplay Guide

### Objective
1. **Explore the mansion** - Navigate through 7 interconnected rooms
2. **Collect treasures** - Find and collect all 5 treasures scattered throughout
3. **Survive ghost encounters** - Use your laser to defeat the 10 roaming ghosts
4. **Boss battle** - Once all treasures are collected, face the final boss
5. **Victory** - Defeat the boss to win the game!

### Survival Tips
- 💡 **Use your laser strategically** - ghosts will chase you relentlessly
- 💡 **Explore thoroughly** - treasures are hidden in different rooms
- 💡 **Manage your health** - you start with 5 lives, use them wisely
- 💡 **Learn the mansion layout** - knowing escape routes can save your life
- 💡 **Save your strength for the boss** - the final battle is challenging

### Rooms & Areas
- **Room 1**: Central hub with cobweb decorations
- **Multiple interconnected rooms** with unique themes and layouts
- **L-shaped corridors** connecting different areas
- **Hidden passages** and strategic vantage points

## 🛠️ Technical Specifications

### Built With
- **Python 3.x** - Core game logic and mechanics
- **PyOpenGL** - 3D graphics rendering and visualization
- **GLUT** - Window management and user input handling
- **GLU** - Advanced OpenGL utilities and camera management

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.6 or higher
- **Memory**: 512 MB RAM minimum
- **Graphics**: OpenGL-compatible graphics card
- **Storage**: 50 MB available space

### Performance Features
- **Optimized rendering** for smooth gameplay
- **Efficient collision detection** system
- **Dynamic object management** for ghosts and projectiles
- **Real-time lighting calculations**

## 🎨 Game Architecture

### Core Components
- **3D Rendering Engine** - Custom OpenGL implementation
- **Physics System** - Collision detection and movement
- **AI System** - Ghost behavior and pathfinding
- **Game State Management** - Score, lives, and progression tracking
- **Audio-Visual Effects** - Atmospheric rendering and animations

### Game Entities
- **Player Character** - Controllable protagonist with health system
- **Ghost Entities** - AI-driven enemies with pursuit behavior
- **Treasure Objects** - Collectible items with scoring system
- **Boss Entity** - Final challenge with unique attack patterns
- **Environmental Objects** - Walls, floors, decorative elements

## 🔧 Troubleshooting

### Common Issues

**Game won't start:**
- Ensure `Scarebnb.py` is placed inside the extracted OpenGL folder
- Verify Python 3.x is installed and accessible via command line
- Check that all OpenGL dependencies are properly extracted

**Graphics issues:**
- Update your graphics drivers
- Ensure your system supports OpenGL
- Try running in compatibility mode if on older systems

**Performance issues:**
- Close unnecessary background applications
- Lower system resolution if needed
- Ensure adequate system resources are available

## 🎮 Game Modes

### Standard Mode
- Full gameplay experience with all challenges
- 5 lives, 10 ghosts, 5 treasures, and boss battle
- Complete mansion exploration

### Cheat Mode (Press 'C')
- Enhanced testing and exploration capabilities
- Useful for learning the mansion layout
- Developer mode for advanced users

## 🏆 Scoring System

- **Treasure Collection**: Track your progress (X/5 treasures)
- **Survival**: Monitor remaining lives
- **Boss Battle**: Health tracking during final confrontation
- **Victory Condition**: Defeat the boss after collecting all treasures

## 🤝 Contributing

This is a complete single-player game project. Feel free to:
- Report bugs or issues
- Suggest gameplay improvements
- Create mods or extensions
- Share gameplay experiences

## 📝 License

This project is available for educational and personal use. Please respect the original work when sharing or modifying.

## 🎯 Credits

**Scarebnb** - A haunting adventure that combines classic horror elements with modern 3D gaming technology. Created with passion for immersive gameplay and atmospheric horror experiences.

---

*Ready to face your fears? Enter the Scarebnb mansion... if you dare! 👻*

**⚠️ Remember: Extract OpenGL.zip and place Scarebnb.py inside the OpenGL folder before running!**