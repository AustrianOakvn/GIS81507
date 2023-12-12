
# K -> down, J-> left, L -> right, I->up
MOVEMENT_KEYS = ["K", "J", "L", "I"]
USER_MM_KEYS = ["A", "W", "S", "D"]
# ATTACK_KEYS = ["T", "Y", "U"]
ATTACK_KEYS = ["T", "Y"]
# USER_ATTACK_KEYS = ["Z", "X", "C"]
USER_ATTACK_KEYS = ["Z", "X"]

CONTROL_KEYS = set(USER_MM_KEYS + USER_ATTACK_KEYS)

MAPPING = {k:v for k,v in zip(USER_MM_KEYS, MOVEMENT_KEYS)}

for i, k in enumerate(USER_ATTACK_KEYS):
    MAPPING[k] = ATTACK_KEYS[i]

# START_GAME_ROUTE = "http://192.168.1.22:8080/start_game"
COMMAND_HANDLER_ROUTE = "http://localhost:8080/commands"
PING_ROUTE = "http://localhost:8080/ping"
NUM_PLAYERS = 6
PING_MS = 500
