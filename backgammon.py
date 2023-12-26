import tkinter as tk
import tkinter.font as tkf
import random


def roll_dice(result_label):
    dice_value_1 = random.randint(1, 6)
    dice_value_2 = random.randint(1, 6)
    result_label.config(text=f"{dice_value_1}, {dice_value_2}", font=("Eras Medium ITC", 50))

def start_game(game_mode, start_menu, root):
    start_menu.destroy()
    game_window = tk.Frame(root, bg="#f5eee8")
    game_window.pack(fill=tk.BOTH, expand=True)

    turn_label = tk.Label(game_window, text="Player 1's Turn", bg="#654426", fg="#f5eee8",
                          font=("Eras Medium ITC", 30), height=2)
    turn_label.pack(side=tk.TOP, fill=tk.BOTH)

    dice_frame = tk.Frame(game_window, bg="#654426")
    dice_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
    dice_result = tk.Label(dice_frame, text="Dice:", bg="#654426", fg="#f5eee8",
                           font=("Eras Medium ITC", 25))
    dice_result.pack(pady=(300, 10), padx=50)
    result_label = tk.Label(dice_frame, text="", bg="#654426", fg="#f5eee8", font=("Eras Medium ITC", 50))
    result_label.pack(pady=10)
    roll_button = tk.Button(dice_frame, text="Roll Dice", bg="#90663f", fg="#f5eee8",
                            command=lambda: roll_dice(result_label), font=("Eras Medium ITC", 20))
    roll_button.pack(pady=10)

    borne_off_frame = tk.Frame(game_window, bg="#f5eee8")
    borne_off_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    borne_label = tk.Label(borne_off_frame, text="Borne:", bg="#f5eee8", fg="#654426",
                           font=("Eras Medium ITC", 25))
    borne_label.pack(pady=(300, 10), padx=50)

    light_count_label = tk.Label(borne_off_frame, text="W x 0", bg="#f5eee8", fg="#654426",
                                 font=("Eras Medium ITC", 20))
    light_count_label.pack(pady=5)
    dark_count_label = tk.Label(borne_off_frame, text="B x 0", bg="#f5eee8", fg="#654426",
                                font=("Eras Medium ITC", 20))
    dark_count_label.pack(pady=5)

    canvas = tk.Canvas(game_window, bg="#f5eee8", highlightthickness=0)
    canvas.pack(expand=True, fill=tk.BOTH)
    draw_board(canvas)


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

def draw_board(canvas):
    base_x = 50 #was 50
    base_y = 50 #was 150
    canvas.create_rectangle(base_x, base_y, base_x+1400, base_y+800, outline="#654426", fill="#90663f")
    canvas.create_rectangle(base_x+30, base_y+30, base_x+660, base_y+770, outline="#654426", fill="#c9a583")
    canvas.create_rectangle(base_x+740, base_y+30, base_x+1370, base_y+770, outline="#654426", fill="#c9a583")

    for i in range(6):
        x_left = base_x + 35 + i * 105
        x_right = x_left + 95
        y_top_base = base_y+30
        y_top_tip = base_y+350
        y_bottom_tip = base_y+450
        y_bottom_base = base_y+770

        if i % 2 == 1:
            fill_color_top = "#654426"
            fill_color_bottom = "#f5eee8"
        else:
            fill_color_top = "#f5eee8"
            fill_color_bottom = "#654426"
        canvas.create_polygon(x_left, y_top_base, x_right, y_top_base, (x_left+x_right)/2, y_top_tip,
                              outline="#654426", fill=fill_color_top)
        canvas.create_polygon(x_left+710, y_top_base, x_right+710, y_top_base, (x_left + x_right) / 2 + 710, y_top_tip,
                              outline="#654426", fill=fill_color_top)
        canvas.create_polygon(x_left, y_bottom_base, x_right, y_bottom_base, (x_left + x_right) / 2, y_bottom_tip,
                              outline="#654426", fill=fill_color_bottom)
        canvas.create_polygon(x_left + 710, y_bottom_base, x_right + 710, y_bottom_base,
                              (x_left + x_right) / 2 + 710, y_bottom_tip, outline="#654426", fill=fill_color_bottom)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Backgammon")
    root.geometry("1920x1080")
    create_start_menu(root)
    root.mainloop()
