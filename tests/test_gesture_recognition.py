import unittest
from scripts.gesture_recognition import detect_pinch

class MockLandmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockHandLandmarks:
    landmark = [
        MockLandmark(0, 0),  # Dummy values
        MockLandmark(0, 0),
        MockLandmark(0, 0),
        MockLandmark(0, 0),
        MockLandmark(0.1, 0.1),  # Thumb tip
        MockLandmark(0, 0),
        MockLandmark(0, 0),
        MockLandmark(0, 0),
        MockLandmark(0.15, 0.15),  # Index tip
    ]

class TestGestureRecognition(unittest.TestCase):
    def test_detect_pinch(self):
        hand_landmarks = MockHandLandmarks()
        self.assertTrue(detect_pinch(hand_landmarks))

if __name__ == "__main__":
    unittest.main()
