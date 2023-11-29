from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import time

app = Flask(__name__)
CORS(app, resources={r"/receive_json": {"origins": "http://localhost:3000"}})

# @app.route('/')
# def home():
#     return 'Hello, World! This is the home page.'

from datetime import datetime
import time

def get_current_time_and_ping(start_time):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_time = time.time()
    ping = round((end_time - start_time) * 1000)  # 毫秒
    return {'current_time': current_time, 'ping': ping}


@app.route('/receive_json', methods=['POST'])
def receive_json():
    print('This is recieve_json method')
    print(request)
    try:
        json_data = request.json
        print("Received JSON data:", json_data)

        # handle

        response = {'status': 'success', 'message': 'json recieved!'}
        return jsonify(response)
    except Exception as e:
        print("Error:", str(e))
        response = {'status': 'error', 'message': str(e)}
        return jsonify(response)

received_data = {}

@app.route('/receive_game_state', methods=['POST'])
def receive_game_state():
    start_time = time.time()
    global received_data
    try:
        game_state_data = request.json
        print("Received game state from ", game_state_data, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        received_data = game_state_data

        time_ping = get_current_time_and_ping(start_time)
        response = {'status': 'success', 'message': 'Your sent message has been recieved.', **time_ping}
        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        time_ping = get_current_time_and_ping(start_time)
        response = {'status': 'error', 'message': str(e),**time_ping}
        return jsonify(response)

@app.route('/get_game_state_for', methods=['GET'])
def get_game_state():
    global received_data
    try:
        # 返回存储的数据给地址B
        return jsonify(received_data)
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
