import random
ACTIONS = {
    "AIR_A": "A", 
    "AIR_B": "B", 
    "AIR_D_DB_BA":"2 1 4_A", 
    "AIR_D_DB_BB":"2 1 4_B", 
    "AIR_D_DF_FA":"2 3 6_A", 
    "AIR_D_DF_FB":"2 3 6_B", 
    "AIR_DA":"2_A", 
    "AIR_DB":"2_B", 
    "AIR_F_D_DFA":"6 2 3_A", 
    "AIR_F_D_DFB":"6 2 3_B", 
    "AIR_FA":"6_A", 
    "AIR_FB":"6_B", 
    "AIR_UA":"8_A", 
    "AIR_UB":"8_B", 
    "BACK_JUMP":"7", 
    "BACK_STEP":"4 4", 
    "CROUCH": "2",
    "CROUCH_A":"2_A", 
    "CROUCH_B":"2_B", 
    "CROUCH_FA":"3_A", 
    "CROUCH_FB":"3_B", 
    "CROUCH_GUARD":"1", 
    "DASH":"6 6", 
    "FOR_JUMP": "9", 
    "FORWARD_WALK":"6",
    "JUMP":"8", 
    "STAND_A": "A", 
    "STAND_B": "B", 
    "STAND_D_DB_BA":"2 1 4_A", 
    "STAND_D_DB_BB":"2 1 4_B", 
    "STAND_D_DF_FA":"2 3 6_A", 
    "STAND_D_DF_FB":"2 3 6_B", 
    "STAND_D_DF_FC":"2 3 6_C", 
    "STAND_F_D_DFA":"6 2 3_A", 
    "STAND_F_D_DFB":"6 2 3_B", 
    "STAND_FA":"6_A", 
    "STAND_FB":"6_B", 
    "STAND_GUARD":"4", 
    "THROW_A":"4_A", 
    "THROW_B":"4_B"
}

ACTIONS_INVERSE = {v:k for k, v in ACTIONS.items()}

KEY_MAP_INVERSE = {
    "T": "A", 
    "Y": "B",
    "U": "C",
    "K+J": "1", # down + left
    "K": "2",   # down
    "K+L": "3", # down + right
    "J": "4",   # left
    "L": "6",   # right
    "I+J": "7", # up + left
    "I": "8",   # up
    "I+L": "9"  # up + right
}
# K -> down, J-> left, L -> right, I->up
MOVEMENT_KEYS = ["K", "J", "L", "I"]
ATTACK_KEYS = ["T", "Y", "U"]


KEY_MAP = {v:k for k,v in KEY_MAP_INVERSE.items()}

def generate_random_keys(key_length:int):
    # available_keys= list(KEY_MAP_INVERSE.keys())
    available_keys = MOVEMENT_KEYS + ATTACK_KEYS
    # print(type(available_keys))
    return random.sample(available_keys, key_length)


def keys2action(keys:list):
    # input: list of keys
    movements = []
    attacks = []
    for k in keys:
        if k in MOVEMENT_KEYS:
            movements.append(k)
        if k in ATTACK_KEYS:
            attacks.append(k)
    if len(movements) != 0:
        movement = random.sample(movements, 1)[0]
        movement = KEY_MAP_INVERSE[movement]
        movement = ACTIONS_INVERSE[movement]
    else:
        movement = None
    if len(attacks) != 0:
        attack = random.sample(movements, 1)[0]
        attack = KEY_MAP_INVERSE[attack]
        attack = ACTIONS_INVERSE[attack]
    else:
        attack = None
    return {"move":movement, "attack":attack}

if __name__ == "__main__":
    rand = generate_random_keys(key_length=5)
    action = keys2action(rand)
    print(rand)
    print(action)
