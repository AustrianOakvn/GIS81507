from flask import Flask, request, jsonify
from flask_cors import CORS  #

app = Flask(__name__)
CORS(app, resources={r"/receive_json": {"origins": "http://localhost:3000"}})

# @app.route('/')
# def home():
#     return 'Hello, World! This is the home page.'

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

if __name__ == '__main__':
    app.run(debug=True, port=3000)
