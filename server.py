from flask import Flask, request, jsonify
import logging
import json
#from detection import jprint

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def jprint(obj):
    # Create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

chessboard = {
    'a1': {'x': 12.5, 'y': 437.5, 'piece': 'R_W'},
    'b1': {'x': 62.5, 'y': 437.5, 'piece': 'N_W'},
    'c1': {'x': 112.5, 'y': 437.5, 'piece': 'B_W'},
    'd1': {'x': 162.5, 'y': 437.5, 'piece': 'Q_W'},
    'e1': {'x': 212.5, 'y': 437.5, 'piece': 'K_W'},
    'f1': {'x': 262.5, 'y': 437.5, 'piece': 'B_W'},
    'g1': {'x': 312.5, 'y': 437.5, 'piece': 'N_W'},
    'h1': {'x': 362.5, 'y': 437.5, 'piece': 'R_W'},
    
    'a2': {'x': 12.5, 'y': 387.5, 'piece': 'P_W'},
    'b2': {'x': 62.5, 'y': 387.5, 'piece': 'P_W'},
    'c2': {'x': 112.5, 'y': 387.5, 'piece': 'P_W'},
    'd2': {'x': 162.5, 'y': 387.5, 'piece': 'P_W'},
    'e2': {'x': 212.5, 'y': 387.5, 'piece': 'P_W'},
    'f2': {'x': 262.5, 'y': 387.5, 'piece': 'P_W'},
    'g2': {'x': 312.5, 'y': 387.5, 'piece': 'P_W'},
    'h2': {'x': 362.5, 'y': 387.5, 'piece': 'P_W'},
    
    'a3': {'x': 12.5, 'y': 337.5, 'piece': None},
    'b3': {'x': 62.5, 'y': 337.5, 'piece': None},
    'c3': {'x': 112.5, 'y': 337.5, 'piece': None},
    'd3': {'x': 162.5, 'y': 337.5, 'piece': None},
    'e3': {'x': 212.5, 'y': 337.5, 'piece': None},
    'f3': {'x': 262.5, 'y': 337.5, 'piece': None},
    'g3': {'x': 312.5, 'y': 337.5, 'piece': None},
    'h3': {'x': 362.5, 'y': 337.5, 'piece': None},
    
    'a4': {'x': 12.5, 'y': 287.5, 'piece': None},
    'b4': {'x': 62.5, 'y': 287.5, 'piece': None},
    'c4': {'x': 112.5, 'y': 287.5, 'piece': None},
    'd4': {'x': 162.5, 'y': 287.5, 'piece': None},
    'e4': {'x': 212.5, 'y': 287.5, 'piece': None},
    'f4': {'x': 262.5, 'y': 287.5, 'piece': None},
    'g4': {'x': 312.5, 'y': 287.5, 'piece': None},
    'h4': {'x': 362.5, 'y': 287.5, 'piece': None},
    
    'a5': {'x': 12.5, 'y': 237.5, 'piece': None},
    'b5': {'x': 62.5, 'y': 237.5, 'piece': None},
    'c5': {'x': 112.5, 'y': 237.5, 'piece': None},
    'd5': {'x': 162.5, 'y': 237.5, 'piece': None},
    'e5': {'x': 212.5, 'y': 237.5, 'piece': None},
    'f5': {'x': 262.5, 'y': 237.5, 'piece': None},
    'g5': {'x': 312.5, 'y': 237.5, 'piece': None},
    'h5': {'x': 362.5, 'y': 237.5, 'piece': None},
    
    'a6': {'x': 12.5, 'y': 187.5, 'piece': None},
    'b6': {'x': 62.5, 'y': 187.5, 'piece': None},
    'c6': {'x': 112.5, 'y': 187.5, 'piece': None},
    'd6': {'x': 162.5, 'y': 187.5, 'piece': None},
    'e6': {'x': 212.5, 'y': 187.5, 'piece': None},
    'f6': {'x': 262.5, 'y': 187.5, 'piece': None},
    'g6': {'x': 312.5, 'y': 187.5, 'piece': None},
    'h6': {'x': 362.5, 'y': 187.5, 'piece': None},
    
    'a7': {'x': 12.5, 'y': 137.5, 'piece': 'P_B'},
    'b7': {'x': 62.5, 'y': 137.5, 'piece': 'P_B'},
    'c7': {'x': 112.5, 'y': 137.5, 'piece': 'P_B'},
    'd7': {'x': 162.5, 'y': 137.5, 'piece': 'P_B'},
    'e7': {'x': 212.5, 'y': 137.5, 'piece': 'P_B'},
    'f7': {'x': 262.5, 'y': 137.5, 'piece': 'P_B'},
    'g7': {'x': 312.5, 'y': 137.5, 'piece': 'P_B'},
    'h7': {'x': 362.5, 'y': 137.5, 'piece': 'P_B'},
    
    'a8': {'x': 12.5, 'y': 87.5, 'piece': 'R_B'},
    'b8': {'x': 62.5, 'y': 87.5, 'piece': 'N_B'},
    'c8': {'x': 112.5, 'y': 87.5, 'piece': 'B_B'},
    'd8': {'x': 162.5, 'y': 87.5, 'piece': 'Q_B'},
    'e8': {'x': 212.5, 'y': 87.5, 'piece': 'K_B'},
    'f8': {'x': 262.5, 'y': 87.5, 'piece': 'B_B'},
    'g8': {'x': 312.5, 'y': 87.5, 'piece': 'N_B'},
    'h8': {'x': 362.5, 'y': 87.5, 'piece': 'R_B'}
}


@app.route('/update_chessboard', methods=['POST', 'GET'])
def update_chessboard():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if data is None or len(data.keys()) != 64:
                return jsonify({"error": "Invalid chessboard data"}), 400
            chessboard.update(data)
            #jprint(chessboard)
            #print(chessboard)
            return jsonify({"message": "Chessboard updated successfully"}), 200

        elif request.method == 'GET':
            return jsonify(chessboard), 200

    except Exception as e:
        app.logger.error("An error occurred with update_chessboard: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500
    
current_move = ""
    
@app.route('/move', methods=['POST', 'GET'])
def move():
    global current_move
    try:
        if request.method == 'POST':
            data = request.get_json()
            if data is None:
                app.logger.error("Invalid move data provided.")
                return jsonify({"error": "Invalid move data"}), 400
            # Assign the move directly from the JSON data
            current_move = data['move']
            app.logger.info("Move updated to: %s", current_move)
            return jsonify({"message": "Move updated successfully"}), 200

        elif request.method == 'GET':
            if current_move:
                # Return the move as a part of a JSON object
                return jsonify({"move": current_move}), 200
            else:
                app.logger.warning("No move data available.")
                return jsonify({"error": "No move data available"}), 404

    except Exception as e:
        app.logger.error("An error occurred with move: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Correct the host IP address for public access
    app.run(host='0.0.0.0', port=5000)