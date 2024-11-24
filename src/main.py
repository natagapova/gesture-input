import sys
import os
import pyautogui
import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# Initialize MediaPipe drawing and hand detection modules
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize position history for smoothing
position_history = deque(maxlen=5)  # Stores the last 5 cursor positions

# Add project root to the system path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from hand_tracking import HandTracker
from scripts.gesture_recognition import detect_pinch
from gesture_to_action import move_mouse, perform_click

def main():
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Mirror the frame to ensure left and right movements are correct
        frame = cv2.flip(frame, 1)

        results = hand_tracker.process_frame(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract landmarks as a list of (x, y) coordinates
                normalized_landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

                # Check if all fingers are pinched together
                if detect_pinch(normalized_landmarks):
                    # Map index finger tip position to screen dimensions
                    index_finger_tip = normalized_landmarks[8]
                    cursor_x = int(index_finger_tip[0] * screen_width)
                    cursor_y = int(index_finger_tip[1] * screen_height)

                    # Add the position to history
                    position_history.append((cursor_x, cursor_y))

                    # Calculate smoothed position using the moving average
                    smoothed_position = np.mean(position_history, axis=0).astype(int)

                    # Move the cursor to the smoothed position
                    pyautogui.moveTo(smoothed_position[0], smoothed_position[1])

                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
