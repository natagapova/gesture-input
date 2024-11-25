import math
import numpy as np

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
    
    index_finger_tip = normalized_landmarks[8]
    middle_finger_tip = normalized_landmarks[12]
    finger_tips = [index_finger_tip, middle_finger_tip]

    # Threshold distance for "pinch"
    threshold = 0.15  # Adjust based on testing (5% of normalized space)

    # Check if all fingertips are close to the thumb
    for fingertip in finger_tips:
        if calculate_distance(thumb_tip, fingertip) > threshold:
            return False  # If any finger is not close, return False

    return True

def detect_finger_click(landmarks):
    """
    Detect if a 'click' gesture is made with one of the fingers.
    Specifically checks if the index and middle fingers are close together.
    """
    index_tip = landmarks[8]  # Index finger tip
    middle_tip = landmarks[12]  # Middle finger tip

    # Calculate distance between index and middle finger tips
    click_distance = np.linalg.norm(np.array(index_tip) - np.array(middle_tip))

    # Threshold for "click" (adjust based on camera setup)
    return click_distance < 0.10  # 3% of normalized distance