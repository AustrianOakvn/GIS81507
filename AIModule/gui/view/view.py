import tkinter as tk
from tkinter import ttk
import uvicorn 
from fastapi import FastAPI, APIRouter
import threading
from pydantic import BaseModel
from typing import List

# example format {player1_name: balance, player2_name: balance, ...} (sorted by balance)
LEADERBOARD = {'Noah': 100, 'Jenny': 50, 'John': 25, 'Bob': 10, 'Alice': 5}
CURRENT_TEAM1 = ['Noah', 'Jenny', 'John']
CURRENT_TEAM2 = ['Bob', 'Alice', 'Michael']

class MainWIndow():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Game Betting Interface")

        self.game_frame = tk.LabelFrame(self.root, text="Game", width=960, height=680)
        self.game_frame.grid(row=0, column=0, rowspan=4, columnspan=2, padx=10, pady=10)

        self.contact_frame = tk.LabelFrame(self.root, text="Contact Us")
        self.contact_frame.grid(row=5, column=2, padx=10, pady=10)
        tk.Label(self.contact_frame, text="Group3").pack()

        self.ad_frame = tk.LabelFrame(self.root, text="Advertisement")
        self.ad_frame.grid(row=5, column=3, padx=10, pady=10)
        tk.Label(self.ad_frame, text = "Advertisement").pack()

        self.character1_frame = tk.LabelFrame(self.root, text="Character 1")
        self.character1_frame.grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self.character1_frame, text="Character 1").pack()

        self.character2_frame = tk.LabelFrame(self.root, text="Character 2")
        self.character2_frame.grid(row=5, column=1, padx=10, pady=10)
        tk.Label(self.character2_frame, text="Character 2").pack()

        self.balance_leaderboard_frame = tk.LabelFrame(self.root, text="Balance Leaderboard")
        self.balance_leaderboard_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        self.root.after(5000, self.update_leaderboard)
        self.root.after(5000, self.update_player1)
        self.root.after(5000, self.update_player2)
        self.root.mainloop()
    
    def update_leaderboard(self):
        for widget in self.balance_leaderboard_frame.winfo_children():
            widget.destroy()
        for ch in LEADERBOARD:
            ttk.Label(self.balance_leaderboard_frame, text=f"Player {ch} score {LEADERBOARD[ch]}").pack()
        self.root.after(5000, self.update_leaderboard)

    def update_player1(self):
        for widget in self.character1_frame.winfo_children():
            widget.destroy()
        for ch in CURRENT_TEAM1:
            tk.Label(self.character1_frame, text=ch).pack()
        self.root.after(5000, self.update_player1)

    def update_player2(self):
        for widget in self.character2_frame.winfo_children():
            widget.destroy()
        for ch in CURRENT_TEAM2:
            tk.Label(self.character2_frame, text=ch).pack()
        self.root.after(5000, self.update_player2)


class Player(BaseModel):
    name: str
    balance: int


class LeaderBoard(BaseModel):
    players: List[Player]

class CurrentPlayers(BaseModel):
    players: List[Player]


class GUIAPI():
    def __init__(self) -> None:
        self.app = FastAPI()
        self.router = APIRouter()
        self.router.add_api_route("/leaderboard", self.update_leaderboard_info, methods=["POST"])
        self.router.add_api_route("/update_p1", self.update_player1_info, methods=["POST"])
        self.router.add_api_route("/update_p2", self.update_player2_info, methods=["POST"])
        uvicorn.run(self.app, port=8889, host="127.0.0.1")

    def update_leaderboard_info(body:LeaderBoard):
        for player in body.players:
            LEADERBOARD[player.name] = player.balance

    def update_player1_info(body:CurrentPlayers):
        CURRENT_TEAM1.append(body.name)

    def update_player2_info(body:CurrentPlayers):
        CURRENT_TEAM2.append(body.name)
        



def main():
    window = MainWIndow()
    gui_api = GUIAPI()

if __name__ == "__main__":
    main()