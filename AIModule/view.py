import argparse
import json
import tkinter as tk
from tkinter import PhotoImage, ttk


USER_NAME_LENTH_LIMIT = 12

class GameView:
    def __init__(self, arg, update_interval=1000):

        self.arg = arg

        # Main application window
        self.root = tk.Tk()
        self.root.title("Game Betting Interface")
        self.root.resizable(False, False)
        self.root.geometry("1280x720")

        self.update_interval = update_interval

        # Frame for the game display (assuming a label for simplicity)
        self.game_frame = tk.LabelFrame(self.root, text="Game", width=960, height=640)
        # self.game_frame.grid(row=0, column=0, rowspan=4, columnspan=2)
        self.game_frame.place(x=0, y=0)

        # Contact and advertisement frame
        self.contact_frame = tk.LabelFrame(self.root, text="Contact Us", width=160, height=80)
        self.contact_frame.place(x=960, y=640)
        # self.contact_frame.grid(row=5, column=2, padx=10, pady=10)
        tk.Label(self.contact_frame, text="Group3", justify=tk.LEFT, wraplength=160).pack(expand=1, fill=tk.BOTH)

        self.ad_frame = tk.LabelFrame(self.root, text="Buy more balance")
        # self.ad_frame.grid(row=5, column=3, padx=10, pady=10)
        self.ad_frame.place(x=1120, y=640)
        tk.Label(self.ad_frame, text="1000 credits for 1000 JPY", justify=tk.LEFT, wraplength=160).pack()

        # Character 1 and 2 information frames
        self.character1_frame = tk.LabelFrame(self.root, text="Character 1")
        self.character1_frame.place(x=0, y=640)

        self.character2_frame = tk.LabelFrame(self.root, text="Character 2")
        self.character2_frame.place(x=480, y=640)

        # Placeholder for player names in character frames (using labels for simplicity)
        self.player1_label = tk.Label(
            self.character1_frame, text="player1, player2, etc.",
            justify=tk.LEFT, wraplength=480
        )
        self.player1_label.pack()

        self.player2_label = tk.Label(
            self.character2_frame, text="player1, player2, etc.",
            justify=tk.LEFT, wraplength=480
        )
        self.player2_label.pack()

        # Frame for balance leaderboard
        self.balance_leaderboard_frame = tk.LabelFrame(
            self.root, text="Balance Leaderboard",
        )
        self.balance_leaderboard_frame.place(x=960, y=0)

        # Example of how to add items to the balance leaderboard
        # for i in range(5):
        #     ttk.Label(self.balance_leaderboard_frame, text=f"Player {i+1} (score)").pack()

        self.player_leaderboard_records = []

        # Frame for instructions
        self.instruction_frame = tk.LabelFrame(self.root, text="Instructions")
        # self.instruction_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10)
        self.instruction_frame.place(x=960, y=320)

        # Read instructions file
        with open("command_instruction.txt") as f:
            instr = f.readlines()
            instr = [x.strip() for x in instr]
            instr = "\n".join(instr)
            # print(instr)
            self.instruction_label = tk.Label(self.instruction_frame, text=instr, justify=tk.LEFT, wraplength=320)
            self.instruction_label.pack()

        # Placeholder for actual game stats (using a label for simplicity)
        # self.game_stats_label = tk.Label(
        #     self.game_stats_frame, text="Current Match: \nNext Match:"
        # )
        # self.game_stats_label.pack()

        # frameCnt = 12
        # self.frames = [PhotoImage(file='mygif.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
        # self.gif_label = tk.Label(self.ad_frame)
        # self.gif_label.pack()
        # self.root.after(0, self.update_gif, 0)

        # Update the content of the LabelFrame every 1 second
        self.root.after(self.update_interval, self.update_content)

    def update_content(self):
        try:

            status = self._read_status_json()
            # print(status)

            child_ld_board = self.balance_leaderboard_frame.winfo_children()

            # destroy previous leaderboard
            cnt_for_destroy = abs(len(status["top_5_balance"]) - len(child_ld_board))
            # print(cnt_for_destroy)
            if cnt_for_destroy > 0:
                for i, child in enumerate(self.balance_leaderboard_frame.winfo_children(), start=1):
                    child.destroy()
                    if i == cnt_for_destroy:
                        break

            self.player_leaderboard_records = []
            child_ld_board = self.balance_leaderboard_frame.winfo_children()

            # update leaderboard
            for i in range(len(status["top_5_balance"])):

                user_id, user_name, balance = status["top_5_balance"][i]

                if i < len(child_ld_board):
                    child_ld_board[i].config(text=f"{user_name}: {balance}")
                    continue

                label = ttk.Label(
                    self.balance_leaderboard_frame, text=f"{user_name}: {balance}"
                ).pack(anchor='w')
                self.player_leaderboard_records.append(label)

            player_1_list = []
            player_2_list = []

            for current_player in status["player_list"]:
                if current_player["player_team"] == "player_1":
                    player_1_list.append(current_player["username"][:USER_NAME_LENTH_LIMIT])
                elif current_player["player_team"] == "player_2":
                    player_2_list.append(current_player["username"][:USER_NAME_LENTH_LIMIT])

            next_game_list_p1 = []
            next_game_list_p2 = []

            for next_player in status["next_game_queue"]:
                if next_player["player_team"] == "player_1":
                    next_game_list_p1.append(next_player["username"][:USER_NAME_LENTH_LIMIT])
                elif next_player["player_team"] == "player_2":
                    next_game_list_p2.append(next_player["username"][:USER_NAME_LENTH_LIMIT])

            player_1_info = "Current players: " + ", ".join(player_1_list) + "\nNext game players: " + ", ".join(next_game_list_p1)
            player_2_info = "Current players: " + ", ".join(player_2_list) + "\nNext game players: " + ", ".join(next_game_list_p2)

            self.player1_label.config(text=player_1_info)
            self.player2_label.config(text=player_2_info)

            # self.game_stats_label.config(text=f"Next Match: {', '.join(next_game_list)}")

            # Schedule the next update after 1 second
            self.root.after(self.update_interval, self.update_content)

        except Exception as e:
            print(e)
            self.root.after(self.update_interval, self.update_content)

    # @staticmethod
    def _read_status_json(self):
        path = self.arg.json_path
        with open(path, "r") as f:
            return json.load(f)

    # def update_gif(self):
    #     frame = self.frames[ind]
    #     ind += 1
    #     if ind == self.frameCnt:
    #         ind = 0
    #     self.gif_label.configure(image=frame)
    #     self.root.after(100, self.update_gif, ind)

def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument("--json_path", type=str, default="status.json")

    return arg.parse_args()

if __name__ == "__main__":

    arg = parse_args()

    # Create an instance of the GameView class
    game_view = GameView(arg)

    # Run the application
    game_view.root.mainloop()
