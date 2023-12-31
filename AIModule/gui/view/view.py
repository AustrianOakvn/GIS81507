import json
import tkinter as tk
from tkinter import PhotoImage, ttk


class GameView:
    def __init__(self, update_interval=1000):
        # Main application window
        self.root = tk.Tk()
        self.root.title("Game Betting Interface")
        self.root.resizable(False, False)

        self.update_interval = update_interval

        # Frame for the game display (assuming a label for simplicity)
        self.game_frame = tk.LabelFrame(self.root, text="Game", width=640, height=480)
        self.game_frame.grid(row=0, column=0, rowspan=4, columnspan=2, padx=10, pady=10)

        # Contact and advertisement frame
        self.contact_frame = tk.LabelFrame(self.root, text="Contact Us")
        self.contact_frame.grid(row=5, column=2, padx=10, pady=10)
        tk.Label(self.contact_frame, text="Group3").pack()

        self.ad_frame = tk.LabelFrame(self.root, text="Advertisement")
        self.ad_frame.grid(row=5, column=3, padx=10, pady=10)
        tk.Label(self.ad_frame, text="Ad").pack()

        # Character 1 and 2 information frames
        self.character1_frame = tk.LabelFrame(self.root, text="Character 1")
        self.character1_frame.grid(row=5, column=0, padx=10, pady=10)

        self.character2_frame = tk.LabelFrame(self.root, text="Character 2")
        self.character2_frame.grid(row=5, column=1, padx=10, pady=10)

        # Placeholder for player names in character frames (using labels for simplicity)
        self.player1_label = tk.Label(
            self.character1_frame, text="player1, player2, etc."
        )
        self.player1_label.pack()

        self.player2_label = tk.Label(
            self.character2_frame, text="player1, player2, etc."
        )
        self.player2_label.pack()

        # Frame for balance leaderboard
        self.balance_leaderboard_frame = tk.LabelFrame(
            self.root, text="Balance Leaderboard"
        )
        self.balance_leaderboard_frame.grid(
            row=1, column=2, columnspan=2, padx=10, pady=10
        )

        # Example of how to add items to the balance leaderboard
        # for i in range(5):
        #     ttk.Label(self.balance_leaderboard_frame, text=f"Player {i+1} (score)").pack()

        self.player_leaderboard_records = []

        # Frame for game stats
        self.game_stats_frame = tk.LabelFrame(self.root, text="Game Stats")
        self.game_stats_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        # Placeholder for actual game stats (using a label for simplicity)
        self.game_stats_label = tk.Label(
            self.game_stats_frame, text="Current Match: \nNext Match:"
        )
        self.game_stats_label.pack()

        # frameCnt = 12
        # self.frames = [PhotoImage(file='mygif.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
        # self.gif_label = tk.Label(self.ad_frame)
        # self.gif_label.pack()
        # self.root.after(0, self.update_gif, 0)

        # Update the content of the LabelFrame every 1 second
        self.root.after(self.update_interval, self.update_content)

    def update_content(self):
        status = self._read_status_json()
        # print(status)
        
        child_ld_board = self.balance_leaderboard_frame.winfo_children()

        # destroy previous leaderboard
        cnt_for_destroy = abs(len(status["top_5_balance"]) - len(child_ld_board))
        print(cnt_for_destroy)
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
                child_ld_board[i].config(text=f"Player {user_name}: {balance}")
                continue
            
            label = ttk.Label(
                self.balance_leaderboard_frame, text=f"Player {user_name}: {balance}"
            ).pack()
            self.player_leaderboard_records.append(label)

        player_1_list = []
        player_2_list = []

        for current_player in status["player_list"]:
            if current_player["player_team"] == "player_1":
                player_1_list.append(current_player["username"])
            elif current_player["player_team"] == "player_2":
                player_2_list.append(current_player["username"])

        self.player1_label.config(text=", ".join(player_1_list))
        self.player2_label.config(text=", ".join(player_2_list))

        next_game_list = []

        for next_player in status["next_game_queue"]:
            next_game_list.append(next_player["username"])

        self.game_stats_label.config(text=f"Next Match: {', '.join(next_game_list)}")

        # Schedule the next update after 1 second
        self.root.after(self.update_interval, self.update_content)

    @staticmethod
    def _read_status_json():
        with open("status.json", "r") as f:
            return json.load(f)

    # def update_gif(self):
    #     frame = self.frames[ind]
    #     ind += 1
    #     if ind == self.frameCnt:
    #         ind = 0
    #     self.gif_label.configure(image=frame)
    #     self.root.after(100, self.update_gif, ind)


if __name__ == "__main__":
    # Create an instance of the GameView class
    game_view = GameView()

    # Run the application
    game_view.root.mainloop()
