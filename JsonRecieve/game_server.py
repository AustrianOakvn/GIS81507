import uvicorn
from fastapi import FastAPI 
from pydantic import BaseModel
from typing import List
from multiprocessing import Process, Queue




class CommandRequest(BaseModel):
    p1_actions: List[str]
    p2_actions: List[str]

def extract_command(command_content):
    pass

def get_game_status():
    pass

app = FastAPI()


@app.post("/commands")
def perform_command(body:CommandRequest):
    p1_commands, p2_commands = body.p1_actions, body.p2_actions
    print(p1_commands)




@app.get("/ping", status_code=200)
def ping():
    return {"message": "Hello world!"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080)