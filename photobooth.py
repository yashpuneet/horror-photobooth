import cv2

# Initialize the default webcam
cap = cv2.VideoCapture(0)

# Check if the camera opened correctly
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Camera feed running. Press 'q' on the video window to quit.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Display
    cv2.imshow('Horror Photobooth', frame)

    # if 'q' is pressed, exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
