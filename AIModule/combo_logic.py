from action_mapping import *
import itertools
import random


def combo_finder(keys:list):
    combo_2, combo_4 = None, None
    inversed_keys = [KEY_MAP_INVERSE[k] for k in keys]
    double_combinations = list(itertools.combinations(inversed_keys, 2))
    quad_combinations = list(itertools.combinations(inversed_keys, 4))
    double_combinations = list(map(lambda x: " ".join(x), double_combinations))
    quad_combinations = list(map(lambda x: " ".join(x), quad_combinations))
    for c in double_combinations:
        if c in ACTIONS_INVERSE.keys():
            combo_2 = ACTIONS_INVERSE[c]
            break
    for c in quad_combinations:
        if c in ACTIONS_INVERSE.keys():
            combo_4 = ACTIONS_INVERSE[c]
            break
    return combo_2, combo_4

def sample_action(keys):
    key = random.sample(keys, 1)[0]
    action = KEY_MAP_INVERSE[key]
    return ACTIONS_INVERSE[action]


def AICommand(twitch_keys):
    # At the moment use simple heuristic to decide the action
    twitch_move_keys = []
    twitch_attk_keys = []
    for k in twitch_keys:
        if k in MOVEMENT_KEYS:
            twitch_move_keys.append(k)
        if k in ATTACK_KEYS:
            twitch_attk_keys.append(k)
    combo_2, combo_4 = combo_finder(twitch_keys)
    if combo_4 != None:
        return combo_4, sample_action(twitch_move_keys)
    if combo_2 != None:
        return combo_2, sample_action(twitch_attk_keys)
    else:
        return sample_action(twitch_attk_keys), sample_action(twitch_move_keys)

if __name__ == "__main__":
    keys = ["K", "J", "L", "I", "Y"]
    # combo_finder(keys)
    print(AICommand(keys))