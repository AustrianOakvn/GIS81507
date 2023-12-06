import uvicorn
from fastapi import FastAPI 
from pydantic import BaseModel
from typing import List
from multiprocessing import Process, Queue, Value
from multiprocessing.managers import BaseManager
# from queue import Queue
import time
import requests



GAME_ENDPOINT = "http://127.0.0.1:8888/set-command"

    
class CommandRequest(BaseModel):
    p1_actions: List[str]
    p2_actions: List[str]

def pop_command(queue_1, queue_2, window_size:int=5):
    # check if queue is empty
    if queue_1.empty() or queue_2.empty():
        return None
    if queue_1.qsize() < window_size or queue_2.qsize() < window_size:
        return None
    else:
        sub_actions_1 = []
        sub_actions_2 = []
        for i in range(window_size):
            sub_actions_1.append(queue_1.get())
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


def game_handler(queue_1, queue_2, game_stat):
    while True:
        time.sleep(0.5)
        commands = pop_command(queue_1, queue_2, 
                               window_size=5)
        print("commands", commands)
        if commands == None:
            continue
        else:
            print("sending commands to game server", commands)
            game_stat = send_command2game(commands)

        
app = FastAPI()

@app.post("/commands")
def perform_command(body:CommandRequest):
    p1_commands, p2_commands = body.p1_actions, body.p2_actions
    print(p1_commands, p2_commands)
    for c1, c2 in zip(p1_commands, p2_commands):
        # tmp_storage.append_queue(c1, c2)
        QUEUE_1.put(c1)
        QUEUE_2.put(c2)

    return {"game_status": GAME_STATUS.value}

    
@app.get("/ping", status_code=200)
def ping():
    return {"message": "Hello world!"}



if __name__ == "__main__":
    QUEUE_1 = Queue(maxsize=100)
    QUEUE_2 = Queue(maxsize=100)
    GAME_STATUS = Value('i', 0)

    server_proc = Process(target=uvicorn.run, args=(app,), kwargs={"port": 8080})
    command_proc = Process(target=game_handler, args=(QUEUE_1, QUEUE_2, GAME_STATUS,))
    procs = [server_proc, command_proc]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()