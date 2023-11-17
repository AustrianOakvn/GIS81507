import requests
import json

# define the json structure
json_data = {
    'player_3': {
        'actions': ['action_1', 'action_2', 'action_3']
    },
    'player_2': {
        'actions': ['action_4', 'action_5', 'action_6']
    }
}

# server address
server_url = 'http://localhost:3000/receive_json'  # server address

headers = {'Content-Type': 'application/json'}  # head info

try:
    # POST request
    response = requests.post(server_url, json=json_data, headers=headers)

    # print server response
    print("Server response code:", response.status_code)

    try:
        # Check data
        response_data = response.json()
        print("Parsed response:", response_data)
    except json.JSONDecodeError:

        print("Raw response:", response.text)

except requests.exceptions.RequestException as e:
    # print error
    print("Error sending request:", str(e))
