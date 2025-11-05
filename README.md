#  Gesture-Controlled Snake Game

A modern take on the classic Nokia Snake game, controlled entirely with hand gestures using computer vision! Built during my free time to explore computer vision capabilities and create something fun.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

##  Why I Built This

I was bored during my free time and wanted to explore computer vision capabilities in a fun way.

It's a perfect blend of nostalgia (classic Snake game) and modern technology (gesture control)!

##  Demo

Control the snake by simply pointing your finger in the direction you want to move - no keyboard, no mouse, just your hand!

##  Features

- **Gesture Control**: Move the snake using hand gestures detected through your webcam
- **Modern UI**: Clean, premium interface with smooth animations
- **Visual Effects**: Glowing snake head, pulsing food, gradient colors
- **Game Modes**: Start screen, gameplay, and game over screens
- **Score Tracking**: Live score and high score tracking
- **Smooth Gameplay**: Optimized speed for enjoyable control

##  Technologies Used

- **Python 3.8+**
- **OpenCV**: Webcam capture and image processing
- **MediaPipe**: Real-time hand tracking and gesture detection
- **Pygame**: Game rendering and UI
- **NumPy**: Mathematical operations

##  Prerequisites

- Python 3.8 or higher
- Webcam
- Good lighting for hand detection

##  Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samuel-isr/gesture-snake-game.git
   cd gesture-snake-game
   ```

2. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe pygame numpy
   ```

3. **Run the game**
   ```bash
   python gesture_snake_premium.py
   ```

##  How to Play

1. **Launch the game** and allow camera access when prompted
2. **Show your hand** to the camera to start
3. **Point your index finger** in the direction you want the snake to move:
   - Point **UP** → Snake moves up
   - Point **DOWN** → Snake moves down
   - Point **LEFT** → Snake moves left
   - Point **RIGHT** → Snake moves right
4. **Eat the food** (red pulsing circle) to grow and score points
5. **Avoid** running into yourself!

### Keyboard Controls
- **R**: Restart game
- **Q**: Quit game

##  Features Breakdown

### Computer Vision
- Real-time hand landmark detection using MediaPipe
- Gesture recognition based on finger pointing direction
- Smooth gesture buffering to reduce jittery movements
- Mirror-mode camera for intuitive control

### Game Mechanics
- Classic snake gameplay with wraparound edges
- Collision detection with self
- Score system with high score tracking
- Smooth movement with optimized speed

### Visual Design
- Premium dark theme color palette
- Gradient snake body (emerald to deep green)
- Glowing effects on snake head and food
- Pulsing food animation
- Clean stat boxes with rounded corners
- Professional typography and shadows

##  Acknowledgments

- Classic Nokia Snake game for inspiration
- The open-source community

