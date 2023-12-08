import tkinter as tk
from tkinter import ttk

# Main application window
root = tk.Tk()
root.title("Game Betting Interface")

root.resizable(False, False)

# Frame for the game display (assuming a label for simplicity)
game_frame = tk.LabelFrame(root, text="Game", width=640, height=480)
game_frame.grid(row=0, column=0, rowspan=4, columnspan=2, padx=10, pady=10)


# Contact and advertisement frame
contact_frame = tk.LabelFrame(root, text="Contact Us")
contact_frame.grid(row=5, column=2, padx=10, pady=10)
tk.Label(contact_frame, text="Group3").pack()

ad_frame = tk.LabelFrame(root, text="Advertisement")
ad_frame.grid(row=5, column=3, padx=10, pady=10)
tk.Label(ad_frame, text="Ad").pack()

# Character 1 and 2 information frames
character1_frame = tk.LabelFrame(root, text="Character 1")
character1_frame.grid(row=5, column=0, padx=10, pady=10)

character2_frame = tk.LabelFrame(root, text="Character 2")

character2_frame.grid(row=5, column=1, padx=10, pady=10)

# Placeholder for player names in character frames (using labels for simplicity)
tk.Label(character1_frame, text="player1, player2, etc.").pack()
tk.Label(character2_frame, text="player1, player2, etc.").pack()

# Frame for balance leaderboard

balance_leaderboard_frame = tk.LabelFrame(root, text="Balance Leaderboard")
balance_leaderboard_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

# Example of how to add items to the balance leaderboard
for i in range(5):

   ttk.Label(balance_leaderboard_frame, text=f"Player {i+1} (score)").pack() 

# Frame for game stats
game_stats_frame = tk.LabelFrame(root, text="Game Stats")
game_stats_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

# Placeholder for actual game stats (using a label for simplicity)
tk.Label(game_stats_frame, text="Current Match: \nNext Match:").pack()

if __name__ == "__main__":
    # Run the application
    root.mainloop()

