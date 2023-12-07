
import logging
import argparse
from pyftg import Gateway
from game_interface import DemoAI_2
from action_mapping import *
from combo_logic import combo_finder, sample_action

from typing import List
import uvicorn
from fastapi import FastAPI 
from pydantic import BaseModel
from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager
import random
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

LOG_TYPE = "DEBUG"
GAME_PORT = 50051
P1_TWITCH_KEYS = []
P2_TWITCH_KEYS = []

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger 

command_logger = setup_logger('command_logger', './game_log/command_log.txt', level=logging.INFO)
game_logger = setup_logger('game_logger', './game_log/game_log.txt', level=logging.INFO)
# logging.basicConfig(filename='./game_log/log.txt', level=LOG_TYPE)

def AICommand(twitch_keys: List[str]):
    # At the moment use simple heuristic to decide the action
    #command_logger.info("triggered AI command")
    print("triggered AI command")
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
    

def run_game(port:int, gateway, character):
    # Thread to run the game
    game_num = 1
    # while True:
    #     try:
    gateway.run_game([character, character], ["KickAI", "DisplayInfo"], game_num)
    gateway.close()
        # except Exception as ex:
        #     gateway.close()



def command_handler(agent_1, agent_2, p1_twich_keys, p2_twitch_keys):
    # Thread to check the command buffer and send to game
    # input: list of commands
    # output: move + attack
    #command_logger.info(f"Buffer key: {p1_twich_keys} {p2_twitch_keys}")
    print("current buffer key:", p1_twich_keys, p2_twitch_keys)
    if len(p1_twich_keys) == 0 or len(p2_twitch_keys) == 0:
        return
    else:
        try:
            p1_move, p1_attack = AICommand(p1_twich_keys)
            p2_move, p2_attack = AICommand(p2_twitch_keys)
            command_logger.info(f"Commands to game:  {p1_move} {p1_attack} {p2_move} {p2_attack}")
            #print("sending command to game:", p1_move, p1_attack, p2_move, p2_attack)
            agent_1.set_action(p1_move, p1_attack)
            agent_2.set_action(p2_move, p2_attack)
        except:
            print("Error in command handler")
    

def get_game_status(agent_1):
    round_finished, p1_data, p2_data = agent_1.get_status()
    return round_finished, p1_data, p2_data
        
        
class Commands(BaseModel):
    p1_actions: List[str]
    p2_actions: List[str]


app = FastAPI()

@app.post("/set-command")
def perform_command(body:Commands):
    P1_TWITCH_KEYS, P2_TWITCH_KEYS = body.p1_actions, body.p2_actions
    print("received keys", P1_TWITCH_KEYS, P2_TWITCH_KEYS)
    game_state = get_game_status(agent_1)
    command_handler(agent_1, agent_2, P1_TWITCH_KEYS, P2_TWITCH_KEYS)
    if game_state == None:
        return {"game_state": "error"}
    if game_state[1] == None or game_state[2] == None:
        return {"game_state": "character data unavailable"}
    state = {"p1_stats": {
            "hp": game_state[1]["hp"],
            "energy": game_state[1]["energy"],
            "player_number": game_state[1]["player_number"]},
        "p2_stats": {
            "hp": game_state[2]["hp"],
            "energy": game_state[2]["energy"],
            "player_number": game_state[2]["player_number"]
        }
    }
    if game_state[0] == True:
        state["game_state"] = "finished"
        agent_1.set_round_status(False)
        agent_2.set_round_status(False)
    else:
        state["game_state"] = "running"
    return state


@app.get("/ping", status_code=200)
def ping():
    return {"message": "Hello world!"}



if __name__ == "__main__":
    BaseManager.register('DemoAI_2', DemoAI_2)
    gateway = Gateway(port=GAME_PORT)
    manager = BaseManager()
    manager.start()
    agent_1 = manager.DemoAI_2()
    agent_2 = manager.DemoAI_2()
    character = 'ZEN'
    gateway.register_ai("KickAI", agent_1)
    gateway.register_ai("DisplayInfo", agent_2)

    game_proc = Process(target=run_game, args=(GAME_PORT, gateway, character))
    #command_proc = Process(target=command_handler, args=(agent_1, agent_2, P1_TWITCH_KEYS, P2_TWITCH_KEYS))
    server_proc = Process(target=uvicorn.run, args=(app,), kwargs={"port": 8888})
    procs = [game_proc, server_proc]
    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()
    #uvicorn.run(app, port=8888)