import math
import numpy as np
import time

def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def detect_pinch(normalized_landmarks):
    """
    Detect if all fingers are pinched (connected to the thumb).
    Args:
        landmarks (list): List of normalized hand landmarks detected by MediaPipe.

    Returns:
        bool: True if all fingers are pinched together, False otherwise.
    """
    # Target fingers
    thumb_tip = normalized_landmarks[4]
    
    index_tip = normalized_landmarks[8]
    middle_tip = normalized_landmarks[12]
    finger_tips = [index_tip, middle_tip]

    # Threshold distance for "pinch"
    threshold = 0.15  # Adjust based on testing (5% of normalized space)

    # Check if all fingertips are close to the thumb
    for fingertip in finger_tips:
        if calculate_distance(thumb_tip, fingertip) > threshold:
            return False  # If any finger is not close, return False

    return True


ready_for_click_time_limit = 20 # events
latest_ready_for_click_times = []

def detect_finger_ready_for_click(normalized_landmarks):
    global latest_ready_for_click_times
    
    # Target fingers
    index_tip = normalized_landmarks[8]
    
    thumb_tip = normalized_landmarks[4]
    middle_tip = normalized_landmarks[12]
    base_fingers = [thumb_tip, middle_tip]
    
    # Calculate the distance between the base fingers
    # If the fingers are not together, skip
    base_fingers_distance = np.linalg.norm(np.array(base_fingers[0]) - np.array(base_fingers[1]))
    if base_fingers_distance > 0.15:
        return False

    # Calculate the average of base fingers
    base_fingers_average = np.mean(base_fingers, axis=0)

    # Calculate the distance between the index tip and the base fingers average
    click_distance = np.linalg.norm(np.array(index_tip) - np.array(base_fingers_average))

    detected = 0.10 < click_distance < 0.25
    
    # Threshold for "click" (adjust based on camera setup)
    if detected:
        if len(latest_ready_for_click_times) > ready_for_click_time_limit:
            latest_ready_for_click_times.pop(0)
            
        latest_ready_for_click_times.append(time.time())
        
        print("Ready")
        
    return detected


ready_for_click_lookback = 500 # ms
ready_for_click_threshold = 5 # events during lookback

def detect_finger_click(normalized_landmarks):
    global latest_ready_for_click_times
    
    # Target fingers
    index_tip = normalized_landmarks[8]
    
    thumb_tip = normalized_landmarks[4]
    middle_tip = normalized_landmarks[12]
    base_fingers = [thumb_tip, middle_tip]
    
    # If the fingers are not together, skip
    base_fingers_distance = np.linalg.norm(np.array(base_fingers[0]) - np.array(base_fingers[1]))
    if base_fingers_distance > 0.15:
        return False

    # Calculate the average of base fingers
    base_fingers_average = np.mean(base_fingers, axis=0)

    # Calculate the distance between the index tip and the base fingers average
    click_distance = np.linalg.norm(np.array(index_tip) - np.array(base_fingers_average))

    # Threshold for "click" (adjust based on camera setup)
    detected = click_distance < 0.10
    
    if detected:
        match_lookback = [t for t in latest_ready_for_click_times if (time.time() - t) * 1000 < ready_for_click_lookback]
        
        if len(match_lookback) >= ready_for_click_threshold:
            # Clear the list to avoid multiple clicks
            latest_ready_for_click_times = []
            
            print("Click fired")
            return True
            
    return False