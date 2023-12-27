import tkinter as tk
import tkinter.font as tkf
import random


class BackgammonBoard:
    def __init__(self, canvas, turn_label, turn, light_count_label, dark_count_label, game_window):
        self.game_window=game_window
        self.light_count_label = light_count_label
        self.dark_count_label = dark_count_label
        self.light_count = 0
        self.dark_count = 0
        self.turn_label = turn_label
        self.canvas = canvas
        self.piece_radius = 35
        self.columns = [[0, 0, 0, 0]] * 25
        self.selected_piece = None
        self.base_x = 50
        self.base_y = 50
        self.turn = turn
        self.dice = []
        for i in range(6):
            x_left = self.base_x + 35 + i * 105
            x_right = x_left + 95
            y_top_base = self.base_y + 30
            y_bottom_base = self.base_y + 770
            self.columns[11 - i] = [(x_left + x_right) / 2, y_top_base, 0, 0]
            self.columns[5 - i] = [(x_left + x_right) / 2 + 710, y_top_base, 0, 0]
            self.columns[12 + i] = [(x_left + x_right) / 2, y_bottom_base, 0, 0]
            self.columns[18 + i] = [(x_left + x_right) / 2 + 710, y_bottom_base, 0, 0]
            self.columns[0][2] = 2
            self.columns[5][3] = 5
            self.columns[7][3] = 3
            self.columns[11][2] = 5
            self.columns[12][3] = 5
            self.columns[16][2] = 3
            self.columns[18][2] = 5
            self.columns[23][3] = 2
        self.columns[24] = [self.base_x+700, self.base_y +400, 0 , 0]

    def draw_piece(self, x, y, color):
        self.canvas.create_oval(x - self.piece_radius, y - self.piece_radius,
                                x + self.piece_radius, y + self.piece_radius, fill=color)

    def place_pieces(self):
        for i, column in enumerate(self.columns):
            for j in range(column[2]):
                if i < 12:
                    self.draw_piece(column[0]+self.piece_radius*(j//5)/2, column[1] + 2 * (j % 5) * self.piece_radius +
                                    self.piece_radius, "#ebddd1")
                elif i < 24:
                    self.draw_piece(column[0]+self.piece_radius*(j//5)/2, column[1] - 2 * (j % 5) * self.piece_radius -
                                    self.piece_radius, "#ebddd1")
                else:
                    self.draw_piece(column[0] + self.piece_radius * (j // 5) / 2,
                                    column[1] - 2 * (j % 5) * self.piece_radius - self.piece_radius, "#ebddd1")
            for j in range(column[3]):
                if i < 12:
                    self.draw_piece(column[0]+self.piece_radius*(j//5)/2, column[1] + 2 * (j % 5) * self.piece_radius +
                                    self.piece_radius, "#25190e")
                elif i < 24:
                    self.draw_piece(column[0]+self.piece_radius*(j//5)/2, column[1] - 2 * (j % 5) * self.piece_radius -
                                    self.piece_radius, "#25190e")
                else:
                    self.draw_piece(column[0] + self.piece_radius * (j // 5) / 2,
                                    column[1] + 2 * (j % 5) * self.piece_radius + self.piece_radius, "#25190e")

    def handle_click(self, event):
        clicked_x, clicked_y = event.x, event.y
        clicked_column = self.get_clicked_column(clicked_x, clicked_y)
        if len(self.dice) > 0:
            if self.valid_move_exists():
                if self.selected_piece is None:
                    if (clicked_column is not None and self.columns[clicked_column][self.turn + 1] > 0 and
                            (self.columns[24][self.turn+1] == 0 or clicked_column == 24)):
                            self.selected_piece = clicked_column
                            self.turn_label.config(text=f"Player {self.turn}'s Turn. Selected col {clicked_column}")
                else:
                    valid = self.valid_move(clicked_column, self.selected_piece)
                    if valid[0]:
                        self.dice.remove(valid[1])
                        if clicked_column is None:
                            if self.turn == 1:
                                self.light_count += 1
                                self.light_count_label.config(text=f"W x {self.light_count}")
                                if self.light_count == 15:
                                    root.after(1000, lambda: win_screen(self.game_window, 1))
                            else:
                                self.dark_count += 1
                                self.dark_count_label.config(text=f"B x {self.dark_count}")
                                if self.dark_count == 15:
                                    root.after(1000, lambda: win_screen(self.game_window, 2))
                        else:
                            if self.turn == 1 and self.columns[clicked_column][3] == 1:
                                self.columns[clicked_column][3] = 0
                                self.columns[24][3] += 1
                            elif self.turn == 2 and self.columns[clicked_column][2] == 1:
                                self.columns[clicked_column][2] = 0
                                self.columns[24][2] += 1
                            self.columns[clicked_column][self.turn+1] += 1
                        self.columns[self.selected_piece][self.turn + 1] -= 1
                        self.selected_piece = None
                        if len(self.dice) == 0:
                            self.turn = self.turn % 2 + 1
                        self.turn_label.config(text=f"Player {self.turn}'s Turn")
                self.redraw_board()
            else:
                self.selected_piece = None
                self.dice = []
                self.turn = self.turn % 2 + 1
                self.turn_label.config(text=f"No more valid moves! Player {self.turn}'s Turn")

    def valid_move(self, clicked_column, selected_piece):
        if clicked_column is None:
            if self.turn == 1:
                for i in range(18):
                    if self.columns[i][2] != 0:
                        return False, None
            else:
                for i in range(18):
                    if self.columns[i+6][3] != 0:
                        return False, None
        if clicked_column == 24:
            return False, None
        if self.turn == 1:
            if clicked_column is not None and self.columns[clicked_column][3] > 1:
                return False, None
            if clicked_column is None:
                if 24 - selected_piece in self.dice:
                    return True, 24 - selected_piece
                for i in range(24 - selected_piece, 6):
                    if self.columns[23-i][2] != 0:
                        return False, None
                max_dice = max(self.dice)
                if max_dice > 24 - selected_piece:
                    return True, max_dice
                return False, None
            move = clicked_column - selected_piece % 24 + selected_piece // 24
            if move in self.dice:
                return True, move
            return False, None
        else:
            if clicked_column is not None and self.columns[clicked_column][2] > 1:
                return False, None
            if clicked_column is None:
                if selected_piece+1 in self.dice:
                    return True, selected_piece+1
                for i in range(selected_piece+1, 6):
                    if self.columns[i][3] != 0:
                        return False, None
                max_dice = max(self.dice)
                if max_dice > selected_piece+1:
                    return True, max_dice
                return False, None
            else:
                move = selected_piece - clicked_column
                if move in self.dice:
                    return True, move
            return False, None

    def valid_move_exists(self):
        if self.columns[24][self.turn+1] != 0:
            for i in range(24):
                if self.valid_move(i, 24)[1]:
                    return True
        else:
            for i in range(24):
                if self.columns[i][self.turn+1] != 0:
                    for j in range(24):
                        if self.valid_move(j, i):
                            return True
                    if self.valid_move(None, i)[1]:
                        return True
        return False



    def redraw_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.place_pieces()

    def draw_board(self):
        self.canvas.create_rectangle(self.base_x, self.base_y, self.base_x + 1400, self.base_y + 800,
                                     outline="#654426", fill="#90663f")
        self.canvas.create_rectangle(self.base_x + 30, self.base_y + 30, self.base_x + 660, self.base_y + 770,
                                     outline="#654426", fill="#c9a583")
        self.canvas.create_rectangle(self.base_x + 740, self.base_y + 30, self.base_x + 1370, self.base_y + 770,
                                     outline="#654426", fill="#c9a583")
        for i in range(6):
            x_left = self.base_x + 35 + i * 105
            x_right = x_left + 95
            y_top_base = self.base_y + 30
            y_top_tip = self.base_y + 350
            y_bottom_tip = self.base_y + 450
            y_bottom_base = self.base_y + 770

            if i % 2 == 1:
                fill_color_top = "#654426"
                fill_color_bottom = "#f5eee8"
            else:
                fill_color_top = "#f5eee8"
                fill_color_bottom = "#654426"
            self.canvas.create_polygon(x_left, y_top_base, x_right, y_top_base, (x_left + x_right) / 2, y_top_tip,
                                       outline="#654426", fill=fill_color_top)
            self.canvas.create_polygon(x_left + 710, y_top_base, x_right + 710, y_top_base, (x_left + x_right) / 2 + 710,
                                       y_top_tip, outline="#654426", fill=fill_color_top)
            self.canvas.create_polygon(x_left, y_bottom_base, x_right, y_bottom_base, (x_left + x_right) / 2, y_bottom_tip,
                                       outline="#654426", fill=fill_color_bottom)
            self.canvas.create_polygon(x_left + 710, y_bottom_base, x_right + 710, y_bottom_base,
                                       (x_left + x_right) / 2 + 710, y_bottom_tip, outline="#654426", fill=fill_color_bottom)

    def get_clicked_column(self, x_coord, y_coord):
        if self.base_y+30 <= y_coord <= self.base_y + 400:
            for i in range(12):
                if abs(self.columns[i][0]-x_coord) <= 47:
                    return i
            if abs(self.columns[24][0] - x_coord) <= 47:
                return 24
        elif self.base_y + 400 < y_coord <= self.base_y + 770:
            for i in range(12):
                if abs(self.columns[i+12][0] - x_coord) <= 47:
                    return i+12
            if abs(self.columns[24][0] - x_coord) <= 47:
                return 24
        return None


def roll_dice(result_label, backgammon_board):
    if len(backgammon_board.dice) == 0:
        dice_value_1 = random.randint(1, 6)
        dice_value_2 = random.randint(1, 6)
        result_label.config(text=f"{dice_value_1}, {dice_value_2}", font=("Eras Medium ITC", 50))
        if dice_value_1 == dice_value_2:
            backgammon_board.dice = [dice_value_1] * 4
        else:
            backgammon_board.dice = [dice_value_1, dice_value_2]

def roll_turn(result_label, player_nr):
    if len(result_label.cget("text")) <= 10:
        dice_value_1 = random.randint(1, 6)
        dice_value_2 = random.randint(1, 6)
        result_label.config(text=f"Player {player_nr}: {dice_value_1}, {dice_value_2}", font=("Eras Medium ITC", 50))

def check_who_starts(result_label_1, result_label_2, winner_label, root, dice_frame, game_mode):
    if len(result_label_1.cget("text")) > 10 and len(result_label_2.cget("text")) > 10:
        rolls_1 = []
        for i in result_label_1.cget("text"):
            if i.isdigit():
                rolls_1.append(int(i))
        rolls_2 = []
        for i in result_label_2.cget("text"):
            if i.isdigit():
                rolls_2.append(int(i))

        if sum(rolls_1) == sum(rolls_2):
            winner_label.config(text="Roll again!")
            result_label_1.config(text="Player 1: ")
            result_label_2.config(text="Player 2: ")
        else:
            winner = 1 if sum(rolls_1) > sum(rolls_2) else 2
            winner_label.config(text=f"Player {winner} wins!")
            root.after(3000, lambda: start_game(game_mode, dice_frame, winner))

def deselect_piece(backgammon_board):
    backgammon_board.selected_piece = None
    backgammon_board.turn_label.config(text=f"Player {backgammon_board.turn}'s Turn")

def win_screen(game_window, winner):
    game_window.destroy()
    win_frame = tk.Frame(root, bg="#654426")
    win_frame.pack(fill=tk.BOTH, expand=True)
    title_label = tk.Label(win_frame, text=f"Player {winner} won !! :D", bg="#654426", fg="#f5eee8",
                           font=("Eras Bold ITC", 70))
    title_label.pack(pady=(300, 50))
    back_button = tk.Button(win_frame, text="Back to main menu", bg="#90663f", fg="#f5eee8",
                            command=lambda: create_start_menu(win_frame), font=("Eras Medium ITC", 35))
    back_button.pack()

def start_game(game_mode, preliminary_rolls, starting_player):
    preliminary_rolls.destroy()
    game_window = tk.Frame(root, bg="#f5eee8")
    game_window.pack(fill=tk.BOTH, expand=True)

    turn_label = tk.Label(game_window, text=f"Player {starting_player}'s Turn", bg="#654426", fg="#f5eee8",
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
                            command=lambda: roll_dice(result_label, backgammon_board), font=("Eras Medium ITC", 20))
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
    deselect_button = tk.Button(borne_off_frame, text="Deselect piece", bg="#f5eee8", fg="#654426",
                            command=lambda: deselect_piece(backgammon_board), font=("Eras Medium ITC", 20))
    deselect_button.pack(pady=10)

    canvas = tk.Canvas(game_window, bg="#f5eee8", highlightthickness=0)
    canvas.pack(expand=True, fill=tk.BOTH)
    backgammon_board = BackgammonBoard(canvas, turn_label, starting_player, light_count_label, dark_count_label,
                                       game_window)
    canvas.bind("<Button-1>", backgammon_board.handle_click)
    backgammon_board.draw_board()
    backgammon_board.place_pieces()

def preliminary_rolls(game_mode, start_menu):
    start_menu.destroy()
    dice_frame = tk.Frame(root, bg="#654426")
    dice_frame.pack(fill=tk.BOTH, expand=True)
    title_label = tk.Label(dice_frame, text="Roll to see who starts:", bg="#654426", fg="#f5eee8",
                           font=("Eras Medium ITC", 35))
    title_label.pack(pady=100)
    winner_label = tk.Label(dice_frame, text="", bg="#654426", fg="#f5eee8",
                           font=("Eras Medium ITC", 25))
    winner_label.pack(pady=20)
    result_label_1 = tk.Label(dice_frame, text="Player1: ", bg="#654426", fg="#f5eee8", font=("Eras Medium ITC", 50))
    result_label_1.pack(pady=10)
    roll_button_1 = tk.Button(dice_frame, text="Roll Dice", bg="#90663f", fg="#f5eee8",
                            command=lambda: (roll_turn(result_label_1, 1),
                                             check_who_starts(result_label_1, result_label_2, winner_label, root,
                                                              dice_frame, game_mode)),
                                             font=("Eras Medium ITC", 20))
    roll_button_1.pack(pady=10)
    result_label_2 = tk.Label(dice_frame, text="Player2: ", bg="#654426", fg="#f5eee8", font=("Eras Medium ITC", 50))
    result_label_2.pack(pady=10)
    roll_button_2 = tk.Button(dice_frame, text="Roll Dice", bg="#90663f", fg="#f5eee8",
                              command=lambda: (roll_turn(result_label_2, 2),
                                               check_who_starts(result_label_1, result_label_2, winner_label, root,
                                                                dice_frame, game_mode)),
                                               font=("Eras Medium ITC", 20))
    roll_button_2.pack(pady=10)




def create_start_menu(win_frame):
    if win_frame is not None:
        win_frame.destroy()
    start_menu = tk.Frame(root, bg="#654426")
    start_menu.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(start_menu, text="Backgammon", bg="#654426", fg="#f5eee8",
                           font=tkf.Font(family="Eras Bold ITC", size=80, weight="bold"))
    title_label.pack(pady=(150, 50))

    game_mode_label = tk.Label(start_menu, text="Select game mode:", bg="#654426", fg="#f5eee8",
                               font=("Eras Medium ITC", 40))
    game_mode_label.pack(pady=40)

    button_2_players = tk.Button(start_menu, text="2 Players (local coop)", width=20, bg="#90663f", fg="#f5eee8",
                                 command=lambda: preliminary_rolls(2, start_menu), font=("Eras Medium ITC", 30))
    button_2_players.pack(pady=10)

    button_1_player = tk.Button(start_menu, text="1 Player (vs AI)", width=20, bg="#90663f", fg="#f5eee8",
                                command=lambda: preliminary_rolls(1, start_menu), font=("Eras Medium ITC", 30))
    button_1_player.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Backgammon")
    root.geometry("1920x1080")
    create_start_menu(None)
    root.mainloop()
