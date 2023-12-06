"""
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
"""

ACTIONS = {
    "A",
    "B",
    "214A",
    "214B",
    "236A",
    "236B",
    "2A",
    "2B",
    "623A",
    "623B",
    "6A",
    "6B",
    "8A",
    "8B",
    "7",
    "44",
    "2",
    "2A",
    "2B",
    "3A",
    "3B",
    "1",
    "66",
    "9",
    "6",
    "8",
    "A",
    "B",
    "236C",
    "6A",
    "6B",
    "4",
    "4A",
    "4B"
}

def combo_find(input_string: str, word_dict: set):
    """
    Finds all words in the word_dict that can be formed with the characters in the input string.

    :param input_string: A string of characters.
    :param word_dict: A set of words to check against.
    :return: A list of words from the word_dict that can be formed with the characters.
    """
    def can_form_word(word, chars):
        for char in word:
            if char not in chars:
                return False
            chars[char] -= 1
            if chars[char] < 0:
                return False
        return True

    from collections import Counter
    input_chars = Counter(input_string)
    valid_words = [word for word in word_dict if can_form_word(word, input_chars.copy())]

    return valid_words



priority_map = {
    '214A': 1, '214B': 2, '236A': 3, '236B': 4, '236C': 5, '623A': 6, '623B': 7,
    '2A': 8, '2B': 9, '3A': 10, '3B': 11, '44': 12, '4A': 13, '4B': 14, '66': 15,
    '6A': 16, '6B': 17, '8A': 18, '8B': 19, '1': 20, '2': 21, '4': 22, '6': 23,
    '7': 24, '8': 25, '9': 26, 'A': 27, 'B': 28
}
def sort_by_custom_priority(strings, priority_map):
    return sorted(strings, key=lambda x: priority_map.get(x, float('inf')))



# Example usage
input_string = '621233AB'

print(sort_by_custom_priority(combo_find(input_string, ACTIONS), priority_map))
# The output result represents the possible combinations of 'combo' that can be formed from the obtained strings,
# and they are arranged according to the order of priority 'priority_map'.


