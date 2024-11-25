import pyautogui

screen_width, screen_height = pyautogui.size()

# Adding a margin on each side of the screen to make edges of the screen more accessible
screen_margins = 0.12
target_width = screen_width * (1 + screen_margins)
target_height = screen_height * (1 + screen_margins)

def move_mouse(normalized_landmarks):
    # Landmark indexes can be found here: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html#hand-landmark-model
    index_finger_tip = normalized_landmarks[8] 
    
    # Map index finger tip position to target dimensions
    cursor_x = int(index_finger_tip[0] * target_width)
    cursor_y = int(index_finger_tip[1] * target_height)
    
    # Clamp cursor position to screen boundaries
    cursor_x = max(0, min(cursor_x, screen_width - 1))
    cursor_y = max(0, min(cursor_y, screen_height - 1))
    
    # _pause=False to avoid freezes caused by pyautogui (https://stackoverflow.com/questions/60006483/python-pyautogui-mouse-movement-in-thread-is-slow-and-unreliable)
    pyautogui.moveTo(cursor_x, cursor_y, duration=0.05, _pause=False)

def perform_click():
    pyautogui.click()
