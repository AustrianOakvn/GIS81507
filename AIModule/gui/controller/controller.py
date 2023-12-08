import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from model import Leaderboard, Player, CurrentMatch
import uvicorn 
from fastapi import FastAPI 
from multiprocessing import Process 



app = FastAPI()
@app.post("/leaderboard")
def get_leaderboard_info(body:Leaderboard):
    pass


@app.post("/current_match")
def get_current_match_info(body:CurrentMatch):
    pass


@app.post("/player")
def get_player_info(body:Player):
    pass


if __name__ == "__main__":
    uvicorn.run(app, port= 8889)