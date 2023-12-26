import tkinter as tk
import tkinter.font as tkf
def start_game(game_mode, start_menu, root):
    start_menu.destroy()
    game_window = tk.Frame(root)


def create_start_menu(root):
    start_menu = tk.Frame(root, bg="#654426")
    start_menu.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(start_menu, text="Backgammon", bg="#654426", fg="#f5eee8",
                           font=tkf.Font(family="Eras Bold ITC", size=80, weight="bold"))
    title_label.pack(pady=(150, 50))

    game_mode_label = tk.Label(start_menu, text="Select game mode:", bg="#654426", fg="#f5eee8",
                               font=("Eras Medium ITC", 40))
    game_mode_label.pack(pady=40)

    button_2_players = tk.Button(start_menu, text="2 Players (local coop)", width=20, bg="#90663f", fg="#f5eee8",
                                 command=lambda: start_game(2, start_menu, root), font=("Eras Medium ITC", 30))
    button_2_players.pack(pady=10)

    button_1_player = tk.Button(start_menu, text="1 Player (vs AI)", width=20, bg="#90663f", fg="#f5eee8",
                                command=lambda: start_game(1, start_menu, root), font=("Eras Medium ITC", 30))
    button_1_player.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Backgammon")
    root.geometry("1920x1080")
    create_start_menu(root)
    root.mainloop()
