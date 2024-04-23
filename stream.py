import cv2
import os
import time
import numpy as np
import pyvirtualcam
from pyvirtualcam import PixelFormat

# Assuming Cropping.py and LocateGrid.py are in the same directory
from cropBoard import ExtractAndStraightenFromImage
# from LocateGrid import DetectGrid

# Set default camera ID and FPS
CAMERA_ID = 0
FPS_OUT = 20

def main():
    # Start the video capture
    vid = cv2.VideoCapture(CAMERA_ID)

    if not vid.isOpened():
        raise RuntimeError('Could not open video source')

    # Query final capture device values (may be different from preferred settings).
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f'Webcam capture started ({width}x{height} @ {vid.get(cv2.CAP_PROP_FPS)}fps)')

    with pyvirtualcam.Camera(width, height, FPS_OUT, fmt=PixelFormat.BGR) as cam:
        print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')

        try:
            while True:
                ret, frame = vid.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                # Apply the image processing function
                boardImg = ExtractAndStraightenFromImage(frame)

                # Display the processed frame
                cv2.imshow("Processed Frame", boardImg)

                # Send to virtual cam
                cam.send(boardImg)
                cam.sleep_until_next_frame()

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit if 'q' is pressed
                    break
        finally:
            vid.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

