import pyautogui
import time
import numpy as np
from math_utils import ease_out_bezier, clamp

screen_width, screen_height = pyautogui.size()

# Adding a margin on each side of the screen to make edges of the screen more accessible
screen_margin = 0.2
target_width = screen_width * (1 + screen_margin * 2)
target_height = screen_height * (1 + screen_margin * 2)

# Constants for smoothing
jitter_threshold = 22 # px
single_move_duration = 300 # ms
first_step_duration = 50 # ms


cursor_target_x = screen_width / 2
cursor_target_y = screen_height / 2
time_till_target = single_move_duration


def os_actions_handler():
    target_fps = 60
    time_per_frame = 1 / target_fps

    while True:
        move_to_target()
        time.sleep(time_per_frame)


def update_cursor_target(normalized_landmarks):
    global cursor_target_x, cursor_target_y, time_till_target
    
    # Landmark indexes can be found here: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html#hand-landmark-model
    thumb_tip = normalized_landmarks[4]
    # index_finger_tip = normalized_landmarks[8] Note: not using index finger tip for simplicity because it is used to detect click
    middle_finger_tip = normalized_landmarks[12]
    
    # Average over target fingers
    average_tip = np.mean([thumb_tip, middle_finger_tip], axis=0)
    
    # Map index finger tip position to target dimensions
    cursor_x = int(average_tip[0] * target_width - screen_margin * screen_width)
    cursor_y = int(average_tip[1] * target_height - screen_margin * screen_height)
    
    # Clamp cursor position to screen boundaries
    cursor_x = max(0, min(cursor_x, screen_width - 1))
    cursor_y = max(0, min(cursor_y, screen_height - 1))
    
    # Check if new position is close enough to the current and skip moving to reduce jitter
    if abs(cursor_x - pyautogui.position().x) <= jitter_threshold and abs(cursor_y - pyautogui.position().y) <= jitter_threshold: return
    
    cursor_target_x = cursor_x
    cursor_target_y = cursor_y
    time_till_target = single_move_duration - first_step_duration


movement_clock = time.time() * 1000

def move_to_target():
    global cursor_target_x, cursor_target_y, time_till_target, movement_clock
    
    # Current cursor position
    current_x, current_y = pyautogui.position()
    
    # Progress fraction of the way to the target
    progress = 1 - (time_till_target / single_move_duration)
    progress = clamp(progress, 0, 1)
    
    # Skip unnecessary movement
    if progress == 1: return
    
    # Apply easing function
    progress = ease_out_bezier(progress)
    
    # Interpolate between current cursor position and target position with a ease out bezier curve
    interpolated_x = current_x + (cursor_target_x - current_x) * progress
    interpolated_y = current_y + (cursor_target_y - current_y) * progress
    
    # _pause=False to avoid freezes caused by pyautogui (https://stackoverflow.com/questions/60006483/python-pyautogui-mouse-movement-in-thread-is-slow-and-unreliable)
    pyautogui.moveTo(interpolated_x, interpolated_y, _pause=False)
    
    # Update time till target
    time_delta = time.time() * 1000 - movement_clock
    time_till_target -= time_delta
    movement_clock = time.time() * 1000


click_cooldown = 300 # ms
last_click_time = 0

def perform_click():
    global last_click_time
    
    if time.time() * 1000 - last_click_time < click_cooldown: return
    
    pyautogui.click(button='left')
    last_click_time = time.time() * 1000