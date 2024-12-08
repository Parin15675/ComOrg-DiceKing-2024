# Dice King

**Dice King** is an interactive dice-based adventure game that combines elements of exploration and combat. Developed as a project for the **Computer Organization and Architecture** course, the game provides a unique experience with strategic gameplay, sensor-based controls, and engaging animations.

---

## Presentation And Gameplay

[![Watch the Presentation](https://img.shields.io/badge/Presentation-Link-blue?style=for-the-badge&logo=google-drive)]([https://your-link-to-presentation.com](https://drive.google.com/drive/folders/141Z3nKOT2puuXSoEX6pt6OOSbPpRyGGw?usp=sharing))

---

## Project Overview

Dice King allows players to roll dice to navigate a board, face enemies, and battle a challenging boss using Raspberry Pi hardware for an immersive experience.

### Key Features:
- **Exploration Phase**: Navigate a tile-based map using dice rolls, encountering enemies and collecting items.
- **Combat Phase**: Engage in battles using precise accelerometer-based aiming to defeat enemies.
- **Boss Battle**: Defeat a powerful boss at the end of the journey with extended combat mechanics.
- **Interactive Feedback**: LEDs display player health, while a buzzer provides audio cues for actions like dice rolls and combat events.
![comOrg_gameplay1](https://github.com/user-attachments/assets/6fe72e26-975f-4d1d-86ad-8c3793711cdc)
![comOrg_gameplay2](https://github.com/user-attachments/assets/f709d670-625a-4335-85a0-916b0b004d57)
![comOrg_gameplay3](https://github.com/user-attachments/assets/50e2f577-c2d9-457b-9628-588583fc86d2)
![comOrg_gameplay4](https://github.com/user-attachments/assets/f3c234bd-e7bb-44fa-8cc6-477d4231c26c)
---

## Gameplay Mechanics

### Exploration Phase:
- Roll a dice to determine movement across the board.
- Encounter enemies, heal with items, and strategically plan your path.

### Combat Phase:
- Use the accelerometer to aim at targets during battles.
- Attack regular enemies (5 hits to defeat) and the boss (10 hits to defeat).

### Additional Features:
- **Real-Time Controls**: GPIO interrupts ensure immediate responsiveness for button presses and accelerometer inputs.
- **Dynamic Animations**: Smooth animations for characters and dice rolls using Pygame.

---

## System Architecture

The system is built around a **Raspberry Pi** and **Pygame**, integrating hardware components like:
- **MPU6050 Accelerometer**: For gesture-based input in combat mode.
- **GPIO Buttons and LEDs**: For controlling gameplay events and health indication.
- **Python Modules**:
  - Main game loop for handling exploration and combat transitions.
  - Animation module for character actions (idle, walk, attack).
  - Combat system for engaging enemies with interactive mechanics.

---

## Hardware Setup

### Components:
1. **Raspberry Pi**: Core of the system.
2. **MPU6050 Accelerometer**: Captures motion data.
3. **LEDs**: Indicate player health.
4. **Button**: Used to transition into combat mode.
5. **Buzzer**: Provides audio feedback.
![comOrg_setup](https://github.com/user-attachments/assets/b1f2e855-8c2d-4d8a-b524-a2d5ac9d3333)


---

## Challenges Faced

- **Precision in Accelerometer Input**: Addressed with calibration and filtering for smoother gameplay.
- **Hardware Integration**: Efficiently handled GPIO for real-time responses.
- **Enemy Mechanics**: Differentiated boss encounters from regular enemies with unique animations and health values.

---

## Future Improvements

1. Enhanced AI for dynamic enemy behavior.
2. Multiplayer mode for competitive or cooperative play.
3. Additional power-ups and items for strategic depth.
4. Improved graphics and animations for a more polished experience.
5. Advanced boss mechanics with unique attack patterns.

---


