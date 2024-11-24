import cv2

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Use AVFoundation for macOS
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened successfully. Press 'q' to exit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Frame not captured.")
            continue

        # Mirror the captured frame
        frame = cv2.flip(frame, 1)

        # Display the captured frame directly without converting to RGB
        cv2.imshow("Webcam Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
