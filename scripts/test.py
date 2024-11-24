import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not accessible.")
else:
    print("Webcam is accessible.")
cap.release()
