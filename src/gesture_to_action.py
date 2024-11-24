import pyautogui

def move_mouse(hand_landmarks):
    screen_width, screen_height = pyautogui.size()
    x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
    pyautogui.moveTo(x * screen_width, y * screen_height)

def perform_click():
    pyautogui.click()
