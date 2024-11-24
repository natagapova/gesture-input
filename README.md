# Hand Gesture Mouse Control

## Overview
This project allows users to control their computer mouse using hand gestures captured by a webcam. The system uses Mediapipe for hand tracking and recognizes gestures like "pinch" for clicking or swiping.

## Directory Structure
- `scripts/`: Contains utility scripts for testing webcam and prototyping.
- `src/`: Core logic, including hand tracking, gesture recognition, and mouse control.
- `tests/`: Unit tests for verifying functionality.
- `data/`: Datasets for gesture recognition.
- `notebooks/`: Jupyter notebooks for dataset exploration.

## How to Run
1. Install dependencies:
   ```bash
   pip install mediapipe opencv-python pyautogui
