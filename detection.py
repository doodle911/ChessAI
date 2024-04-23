from inference import InferencePipeline
from inference.models.utils import get_model
from inference.core.interfaces.stream.sinks import render_boxes
from inference.core.interfaces.camera.entities import VideoFrame
import cv2
import numpy as np
import json
import keyboard
import requests
import threading
import time

PIECE_TYPES = ["P_W", "N_W", "B_W", "R_W", "Q_W", "K_W", "P_B", "N_B", "B_B", "R_B", "Q_B", "K_B"]

send_flag = False

def jprint(dictionary):
    print(json.dumps(dictionary, indent=4))

# Function to calculate center coordinates of each square on a chessboard
def calculate_square_centers(image_width, image_height):
    square_width = image_width / 8
    square_height = image_height / 8

    square_centers = {}
    # Iterate through rows and columns to calculate centers
    for row in range(8):  # 8 rows (1-8)
        for col in range(8):  # 8 columns (a-h)
            # Calculate center coordinates of this square
            center_x = (col + 0.5) * square_width
            center_y = (row + 0.5) * square_height

            # Convert row and col to algebraic notation a1, b1 etc.
            square_name = chr(col + ord('a')) + str(8 - row)
            square_centers[square_name] = {'x': center_x, 'y': center_y}

    return square_centers

# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

# Function to find the closest square to a given object center
def find_closest_square(object_center_x, object_center_y, square_centers):
    closest_square = None
    min_distance = float('inf')
    
    # Iterate through square centers to find the closest one
    for square, coords in square_centers.items():
        distance = calculate_distance(coords['x'], coords['y'], object_center_x, object_center_y)
        if distance < min_distance:
            closest_square = square
            min_distance = distance
            
    return closest_square

# Define image dimensions
image_width = 640  
image_height = 480

# Calculate square centers for the chessboard
square_centers = calculate_square_centers(image_width, image_height)

# Generate the chessboard dictionary using for loops
chessboard = {}
for row in range(8, 0, -1):  # Iterate through rows (1-8)
    for col in range(ord('a'), ord('i')):  # Iterate through columns (a-h)
        square_name = chr(col) + str(row)  # Convert row and col to algebraic notation
        chessboard[square_name] = {"x": None, "y": None, "piece": None}

# Update chessboard dictionary with square centers
for square, center in square_centers.items():
    chessboard[square] = center
    chessboard[square]['piece'] = None

# Send chessboard to Flask Server at specified rate
def send_chessboard(chessboard):
    url = 'http://localhost:5000/update_chessboard'  # Ensure the port number is correct here.
    response = requests.post(url, json=chessboard)


def clear_chessboard():
    for key in chessboard:
        chessboard[key]['piece'] = None

# Custom sink function to handle predictions
def my_custom_sink(predictions: dict, video_frame: VideoFrame):
    #global square_centers
    global chessboard, send_flag
    clear_chessboard() 
    # Iterate through each prediction in the predictions list
    for p in predictions['predictions']:
        center_x = p['x']
        center_y = p['y']
        piece = p['class']
        
        # Find the closest square to the object center
        closest_square = find_closest_square(center_x, center_y, square_centers)
        
        # Update the chessboard with detected piece in the closest square
        chessboard[closest_square]['piece'] = piece
    
    # Print the updated chessboard 
    jprint(chessboard) 
    send_flag = True
    
# Initialize the inference pipeline
pipeline = InferencePipeline.init(
    model_id="crap-object-detection/1",
    api_key="VCkdCb9yChgHCrexOwvX",
    video_reference=2,
    on_prediction=my_custom_sink,
)

def monitor_and_send_chessboard():
    global send_flag
    while True:
        if send_flag:
            send_chessboard(chessboard)
            send_flag = False
        time.sleep(1)

# Start the monitor thread
thread = threading.Thread(target=monitor_and_send_chessboard)
thread.daemon = True
thread.start()


# Start the pipeline
pipeline.start()
# Wait for the pipeline to finish
pipeline.join()


