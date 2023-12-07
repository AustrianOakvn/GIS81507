import tkinter as tk
from tkinter import ttk

# Main application window
root = tk.Tk()
root.title("Game Betting Interface")
root.geometry("1280x720")
root.resizable(False, False)

# Style for frame label
style = ttk.Style()
style.configure("Bold.TLabel", font=("TkDefaultFont", 16, "bold"))

# Frame for the game display (assuming a label for simplicity)
game_frame_label = ttk.Label(text="Game", style="Bold.TLabel")
game_frame = tk.LabelFrame(root, width=960, height=640, labelwidget=game_frame_label)
game_frame.grid(row=0, column=0, rowspan=4, columnspan=2, padx=10, pady=10)

# Contact and advertisement frame
# contact_frame = tk.LabelFrame(root, text="Contact Us")
# contact_frame.grid(row=5, column=2, padx=10, pady=10)
# tk.Label(contact_frame, text="Group3").pack()

ad_frame_label = ttk.Label(text="Advertisement", style="Bold.TLabel")
ad_frame = tk.LabelFrame(root, labelwidget=ad_frame_label)
ad_frame.grid(row=4, rowspan=2, column=3, padx=10, pady=10)
tk.Label(ad_frame, text="Ad").pack()

# Character 1 and 2 information frames
c1_frame_label = ttk.Label(text="Character 1", style="Bold.TLabel")
character1_frame = tk.LabelFrame(root, labelwidget=c1_frame_label)
character1_frame.grid(row=5, column=0, padx=10, pady=10)

c2_frame_label = ttk.Label(text="Character 2", style="Bold.TLabel")
character2_frame = tk.LabelFrame(root, labelwidget=c2_frame_label)
character2_frame.grid(row=5, column=1, padx=10, pady=10)

# Placeholder for player names in character frames (using labels for simplicity)
tk.Label(character1_frame, text="player1, player2, etc.").pack()
tk.Label(character2_frame, text="player1, player2, etc.").pack()

# Frame for balance leaderboard
balance_leaderboard_frame_label = ttk.Label(text="Balance Leaderboard", style="Bold.TLabel")
balance_leaderboard_frame = tk.LabelFrame(root, labelwidget=balance_leaderboard_frame_label)
balance_leaderboard_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

# Example of how to add items to the balance leaderboard
for i in range(5):
   ttk.Label(balance_leaderboard_frame, text=f"Player {i+1} (score)").pack()

# # Frame for game stats
# game_stats_frame = tk.LabelFrame(root, text="Game Stats")
# game_stats_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

# # Placeholder for actual game stats (using a label for simplicity)
# tk.Label(game_stats_frame, text="Current Match: \nNext Match:").pack()

if __name__ == "__main__":
    # Run the application
    root.mainloop()

