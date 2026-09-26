import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

# Constants
GHOST = "assets/ghost.webp"
MODEL_PATH = "selfie_segmenter.tflite"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite"


def ensure_model_exists():
    """Auto-downloads the MediaPipe model file if not present locally."""
    if not os.path.exists(MODEL_PATH):
        print("Model file missing. Downloading selfie segmenter model...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded successfully!")


# Overlay logic
def overlay(background, overlay):
    """Blends a 4-channel transparent PNG/WebP image onto a 3-channel BGR frame."""
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
    

def process_frame(frame, asset, segmentor):
    """Composites human video frame over monster background using segmentation mask."""
    h, w, _ = frame.shape

    asset_resized = cv2.resize(asset, (w,h), interpolation=cv2.INTER_AREA)
    altered_frame = overlay(frame, asset_resized)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    segmentation_result = segmentor.segment(mp_image)
    category_mask = np.squeeze(segmentation_result.category_mask.numpy_view())

    human_condition = category_mask == 0
    human_condition_3d = np.stack((human_condition,)*3, axis=-1)

    return np.where(human_condition_3d, frame, altered_frame)

    
def main():

    if not os.path.exists(GHOST):
        print(f"Error: '{GHOST}' not found")
        exit()
        return
    
    ensure_model_exists()

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.ImageSegmenterOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        output_category_mask=True
    )

    with vision.ImageSegmenter.create_from_options(options) as segmentor:
        # Initialize the default webcam
        cam = cv2.VideoCapture(0)

        # Check if the camera opened correctly
        if not cam.isOpened():
            print("Error: Could not access the webcam.")
            exit()
            return 

        asset = cv2.imread(GHOST, cv2.IMREAD_UNCHANGED)
        print("Camera feed running. Press 'q' on the video window to quit.")

        while True:
            ret, frame = cam.read()

            if not ret:
                print("Error: Failed to grab frame.")
                break

            output = process_frame(frame, asset, segmentor)

            # Display
            cv2.imshow('Horror Photobooth', output)

            # if 'q' is pressed, exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Clean up
        cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
