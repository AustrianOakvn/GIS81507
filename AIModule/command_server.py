import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

#from multiprocessing import Process, Queue, Value, Array
#from multiprocessing.managers import BaseManager
from queue import Queue
import time
import requests
import threading



GAME_ENDPOINT = "http://127.0.0.1:8888/set-command"
GAME_ENDPOINT_STAT = "http://127.0.0.1:8888/get-game-status"
GAME_STATUS = {}

class CommandRequest(BaseModel):
    player_1: List[str]
    player_2: List[str]

def pop_command(queue_1, queue_2, window_size:int=5):
    # check if queue is empty
    # if queue_1.empty() or queue_2.empty():
    #     return None
    # if queue_1.qsize() < window_size or queue_2.qsize() < window_size:
    #     return None
    # else:
    #     sub_actions_1 = []
    #     sub_actions_2 = []
    #     for i in range(window_size):
    #         sub_actions_1.append(queue_1.get())
    #         sub_actions_2.append(queue_2.get())

    #     return {
    #         "p1_actions": sub_actions_1,
    #         "p2_actions": sub_actions_2
    #     }
    sub_actions_1 = []
    sub_actions_2 = []
    if queue_1.qsize() > 0:
        while not queue_1.empty():
            sub_actions_1.append(queue_1.get())
    if queue_2.qsize() > 0:
        while not queue_2.empty():
            sub_actions_2.append(queue_2.get())

    return {
        "p1_actions": sub_actions_1,
        "p2_actions": sub_actions_2
    }



def send_command2game(commands):
    payload = {
        "p1_actions": commands["p1_actions"],
        "p2_actions": commands["p2_actions"]
    }
    response = requests.post(GAME_ENDPOINT, json=payload)

    game_stat = response.json()
    return game_stat


def get_game_stat():
    response = requests.post(GAME_ENDPOINT_STAT)
    game_stat = response.json()
    return game_stat


def game_handler(queue_1, queue_2):
    global GAME_STATUS
    while True:
        time.sleep(0.5)
        commands = pop_command(queue_1, queue_2,
                               window_size=5)
        print("commands", commands)
        if commands == None:
            GAME_STATUS = get_game_stat()
        else:
            print("sending commands to game server", commands)
            GAME_STATUS = send_command2game(commands)

def clear_queue(queue):
    while not queue.empty():
        queue.get()


app = FastAPI()

@app.post("/commands")
def perform_command(body:CommandRequest):

    print("received command", body)
    p1_commands, p2_commands = body.player_1, body.player_2
    print(p1_commands, p2_commands)
    print("game stat when command invoked", GAME_STATUS)

    for c1 in p1_commands:
        QUEUE_1.put(c1)
    for c2 in p2_commands:
        QUEUE_2.put(c2)


    return GAME_STATUS


@app.post("/ping", status_code=200)

def ping():
    return {"message": "Hello world!"}



if __name__ == "__main__":

    QUEUE_1 = Queue(maxsize=100)
    QUEUE_2 = Queue(maxsize=100)
    #GAME_STATUS = Value('d', {"state": ""})
    #GAME_STATUS = Array('i', {"state": "sth"})
    #GAME_STATUS = Array('i', {'state': 'initial_value'})
    #server_proc = Process(target=uvicorn.run, args=(app,), kwargs={"host": '0.0.0.0', "port": 8080})
    #command_proc = Process(target=game_handler, args=(QUEUE_1, QUEUE_2, GAME_STATUS,))
    server_proc = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": '0.0.0.0', "port": 8080})
    command_proc = threading.Thread(target=game_handler, args=(QUEUE_1, QUEUE_2,))
    procs = [server_proc, command_proc]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()

