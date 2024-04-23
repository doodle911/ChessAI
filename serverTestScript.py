import requests

# Constructing a dummy chessboard dictionary
chessboard = {
    'a1': {'x': 12.5, 'y': 437.5, 'piece': 'R_W'},
    'b1': {'x': 62.5, 'y': 437.5, 'piece': 'N_W'},
    'c1': {'x': 112.5, 'y': 437.5, 'piece': 'B_W'},
    'd1': {'x': 162.5, 'y': 437.5, 'piece': 'Q_W'},
    'e1': {'x': 212.5, 'y': 437.5, 'piece': 'K_W'},
    'f1': {'x': 262.5, 'y': 437.5, 'piece': 'B_W'},
    'g1': {'x': 312.5, 'y': 437.5, 'piece': 'N_W'},
    'h1': {'x': 362.5, 'y': 437.5, 'piece': 'R_W'},
    # Add entries for all squares, this example only includes the first row for brevity
}

# Specify the URL of your Flask server
url = 'http://localhost:5000/update_chessboard'

# Send the chessboard dictionary as a JSON payload in a POST request to the Flask server
response = requests.post(url, json=chessboard)

# Print the response from the server
print(f"Status Code: {response.status_code}, Response Text: {response.text}")