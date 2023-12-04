
import logging
import argparse
from pyftg import Gateway
from samples.DemoAI_2 import DemoAI_2

from typing import List
import uvicorn
from fastapi import FastAPI 
from pydantic import BaseModel
from multiprocessing import Process


LOG_TYPE = "INFO"
GAME_PORT = 50051
P1_TWITCH_KEYS = []
P2_TWITCH_KEYS = []
gateway, agent_1, agent_2 = None, None, None

logging.basicConfig(level=LOG_TYPE)

def AICommand(twitch_keys: List[str]):
    # At the moment use the default random actions
    pass

def run_game(port:int):
    global gateway, agent_1, agent_2 
    character = 'ZEN'
    gateway= Gateway(port = port)
    agent_1 = DemoAI_2()
    agent_2 = DemoAI_2()
    gateway.register_ai("KickAI", agent_1)
    gateway.register_ai("DisplayInfo", agent_2)
    game_num = 1
    gateway.run_game([character, character], ["KickAI", "DisplayInfo"], game_num)
    gateway.close()


def command_handler():
    # input: list of commands
    # output: move + attack
    while True:
        if len(P1_TWITCH_KEYS) == 0 or len(P2_TWITCH_KEYS) == 0:
            continue
        else:
            try:
                p1_move, p1_attack = AICommand(P1_TWITCH_KEYS)
                p2_move, p2_attack = AICommand(P2_TWITCH_KEYS)
                agent_1.set_action(p1_move, p1_attack)
                agent_2.set_action(p2_move, p2_attack)
            except:
                print("Error in command handler")
    

def get_game_status():
    if gateway == None or agent_1 == None or agent_2 == None:
        return None
    agent_1.get_information()
    characters = agent_1.frame_data.character_data
    p1_data, p2_data = {}, {}
    for i, character in enumerate(characters):
        if i == 0:
            p1_data["hp"] = character.hp
            p1_data["energy"] = character.energy
            p1_data["player_numer"] = character.player_number
        elif i == 1:
            p2_data["hp"] = character.hp
            p2_data["energy"] = character.energy
            p2_data["player_numer"] = character.player_number
    return p1_data, p2_data
        
        
class Commands(BaseModel):
    p1_actions: List[str]
    p2_actions: List[str]


app = FastAPI()

@app.post("/set-command")
def perform_command(body:Commands):
    P1_TWITCH_KEYS, P2_TWITCH_KEYS = body.p1_actions, body.p2_actions
    game_state = get_game_status()
    state = {"p1_stats": {
            "hp": game_state[0]["hp"],
            "energy": game_state[0]["energy"],
            "player_number": game_state[0]["player_number"]},
        "p2_stats": {
            "hp": game_state[1]["hp"],
            "energy": game_state[1]["energy"],
            "player_number": game_state[1]["player_number"]
        }
    }
    state["game_state": "running"]
    return state


@app.get("/ping", status_code=200)
def ping():
    return {"message": "Hello world!"}



if __name__ == "__main__":
    game_proc = Process(target=run_game, args=(GAME_PORT,))
    command_proc = Process(target=command_handler)
    server_proc = Process(target=uvicorn.run, args=(app,), kwargs={"port": 8888})
    procs = [game_proc, command_proc, server_proc]
    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()
    #uvicorn.run(app, port=8888)