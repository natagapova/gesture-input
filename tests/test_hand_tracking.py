import unittest
from src.hand_tracking import HandTracker

class TestHandTracking(unittest.TestCase):
    def test_init(self):
        tracker = HandTracker()
        self.assertIsNotNone(tracker.hands)

if __name__ == "__main__":
    unittest.main()
