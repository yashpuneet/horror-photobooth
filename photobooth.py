import cv2
import numpy as np
import os

# Constants
GHOST = "assets/ghost.webp"

# Overlay logic
def overlay(background, overlay):
    bg = background.copy()

    # Normalize Alpha
    if overlay.shape[2] == 4:
        b, g, r, alpha = cv2.split(overlay)
        alpha_mask = alpha/255.0
        inv_mask = 1.0 - alpha_mask

        # Blend
        for c in range(0, 3):
            bg[:,:,c] = (alpha_mask * overlay[:,:,c] + inv_mask * bg[:,:,c])
        
        return bg

    else:
        return background
    
def main():

    if not os.path.exists(GHOST):
        print(f"Error: '{GHOST}' not found")
        exit()


    # Initialize the default webcam
    cam = cv2.VideoCapture(0)

    # Check if the camera opened correctly
    if not cam.isOpened():
        print("Error: Could not access the webcam.")
        exit()

    print("Camera feed running. Press 'q' on the video window to quit.")

    while True:

        ret, frame = cam.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        h, w, _ = frame.shape

        ghost = cv2.imread(GHOST, cv2.IMREAD_UNCHANGED)
        ghost_resized = cv2.resize(ghost, (w,h), interpolation=cv2.INTER_AREA)

        altered_frame = overlay(frame, ghost_resized)

        # Display
        cv2.imshow('Horror Photobooth', altered_frame)

        # if 'q' is pressed, exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
