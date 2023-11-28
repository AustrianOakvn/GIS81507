import uvicorn
from fastapi import FastAPI 
from pydantic import BaseModel
from typing import List
from multiprocessing import Process
from queue import Queue
import time


ACTION_QUEUE_1 = Queue(maxsize=100)
ACTION_QUEUE_2 = Queue(maxsize=100)
GAME_STATUS = None

class CommandRequest(BaseModel):
    p1_actions: List[str]
    p2_actions: List[str]

def pop_command(window_size:int=5):
    # check if queue is empty
    if ACTION_QUEUE_1.empty() or ACTION_QUEUE_2.empty():
        return None
    if ACTION_QUEUE_1.qsize() < window_size() or ACTION_QUEUE_2.qsize() < window_size:
        return None
    else:
        sub_actions_1 = []
        sub_actions_2 = []
        for i in range(window_size):
            sub_actions_1.append(ACTION_QUEUE_1.get())
            sub_actions_2.append(ACTION_QUEUE_2.get())
        return {
            "p1_actions": sub_actions_1,
            "p2_actions": sub_actions_2
        }
    
    
def send_command2game(commands):
    pass

def game_handler():
    while True:
        commands = pop_command(window_size=5)
        if commands == None:
            continue
        else:
            GAME_STATUS = send_command2game()

        
app = FastAPI()

@app.post("/commands")
def perform_command(body:CommandRequest):
    p1_commands, p2_commands = body.p1_actions, body.p2_actions
    print(p1_commands, p2_commands)
    for c1, c2 in zip(p1_commands, p2_commands):
        ACTION_QUEUE_1.put(c1)
        ACTION_QUEUE_2.put(c2)

    return {"game_status": GAME_STATUS}

    
@app.get("/ping", status_code=200)
def ping():
    return {"message": "Hello world!"}



if __name__ == "__main__":
    uvicorn.run(app, port=8080)