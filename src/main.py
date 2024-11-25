import sys
import os
import pyautogui
import cv2
import mediapipe as mp
from collections import deque
import time

# Initialize MediaPipe drawing and hand detection modules
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Add project root to the system path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from hand_tracking import HandTracker
from gesture_recognition import detect_pinch
from os_actions import move_mouse, perform_click

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Use AVFoundation for macOS and DSHOW for Windows
    hand_tracker = HandTracker()
    
    t = time.time()

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
                    move_mouse(normalized_landmarks)

                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # print fps
        fps = 1 / (time.time() - t)
        print(f"FPS: {fps:.2f}")
        t = time.time()
        
        cv2.imshow("Hand Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
