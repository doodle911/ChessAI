
import cv2
VIRTUAL_CAMERA_INDEX = 2 # Adjust this index as needed

# Attempt to open the virtual camera
cap = cv2.VideoCapture(VIRTUAL_CAMERA_INDEX)

if not cap.isOpened():
    print("Error: Could not open virtual camera.")
    exit()

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display the resulting frame
        cv2.imshow('Virtual Camera Output', frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()