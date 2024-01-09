import tkinter as tk
import tkinter.font as tkf
import random
import threading
import time


class AIPlayer:
    """
    A class used to represent the AI player for the single player mode.

    ...

    Attributes
    ----------
    backgammon_board : BackgammonBoard
        the current game environment
    result_label : tkinter.Label
        holds the results of a dice roll
    ai_thread : threading.Thread
        in which the main loop should run

    Methods
    -------
    ai_turn()
        Continuously runs the AI, waiting for its turn to take action.
    roll_dice()
        Simulates dice roll, with delay to be readable to the human player.
    make_move()
        Simulates piece selection and movement, with delay to be readable to the human player.
    start_ai_thread()
        Creates ai_thread and runs ai_turn on it.
    """

    def __init__(self, backgammon_board, result_label):
        """
        Provides all the necessary attributes to simulate actions.

        Parameters
        ----------
        backgammon_board : BackgammonBoard
            the current game environment, to access properties and simulate actions
        result_label : tkinter.Label
            holds the results of a dice roll, to simulate roll
        """

        self.backgammon_board = backgammon_board
        self.result_label = result_label
        self.ai_thread = None

    def ai_turn(self):
        """
        Continuously runs the AI, waiting for its turn to take action.

        Returns
        -------
        None
        """

        while True:
            if self.backgammon_board.light_count == 15 or self.backgammon_board.dark_count == 15:
                break
            if self.backgammon_board.turn == 2:
                if len(self.backgammon_board.dice) == 0:
                    self.roll_dice()
                self.make_move()
            time.sleep(0.1)

    def roll_dice(self):
        """
        Simulates dice roll, with delay to be readable to the human player.

        Returns
        -------
        None
        """

        time.sleep(1)
        roll_dice(self.result_label, self.backgammon_board)

    def make_move(self):
        """
        Simulates piece selection and movement, with delay to be readable to the human player.

        Returns
        -------
        None
        """

        move = self.backgammon_board.valid_move_exists()
        time.sleep(1)
        self.backgammon_board.decide_action(move[2])
        time.sleep(1)
        self.backgammon_board.decide_action(move[1])

    def start_ai_thread(self):
        """
        Creates ai_thread and runs ai_turn() on it.

        Preferred to running ai_turn() directly, as that may lag or freeze the game.

        Returns
        -------
        None
        """

        if self.ai_thread is None or not self.ai_thread.is_alive():
            self.ai_thread = threading.Thread(target=self.ai_turn)
            self.ai_thread.start()


class BackgammonBoard:
    """
    A class used to represent the Backgammon Board with all its logic.

    ...

    Attributes
    ----------
    canvas : tkinter.Canvas
        the visuals of the board, including pieces
    turn_label : tkinter.Label
        displays whose turn it is, with additional messages to the player(s)
    turn : int
        index of the player who / must make a move, 1 or 2
    light_count_label : tkinter.Label
        displays how many pieces player 1 bore off
    dark_count_label : tkinter.Label
        displays how many pieces player 2 bore off
    game_window : tkinter.Frame
        contains all the information of the game screen, to be deleted on win screen transition
    light_count : int
        number of pieces borne off by player 1
    dark_count : int
        number of pieces borne off by player 2
    piece_radius : int
        radius of a checkers piece
    columns : list[list[int]]
        holds the coordinates and number of pieces of each color on each space on the board
    selected_piece : int
        the index of the column from which a piece was selected
    base_x : int
        base x coordinate, relative to starting point of the element in the frame, where the canvas will be drawn
    base_y : int
        base x coordinate, relative to starting point of the element in the frame, where the canvas will be drawn
    dice : list[int]
        list of remaining move distances, based on rolled dice and moves already made
    Methods
    -------
    draw_piece(x, y, color):
        Draws one circular checker piece at the specified x and y coordinates, in the specified color.
    place_pieces():
        (re)Places all pieces on the board, according to their last saved position.
    handle_click():
        Handles left mouse button click event from player(s).
    decide_action():
        Decides what action to take on click event.
    valid_move(clicked_column, selected_piece):
        Decides whether moving selected_piece to clicked_column is a valid move.
    valid_move_exists():
        Decides if there are any possible valid moves left in the current game state.
    redraw_board():
        Redraws all elements of the board, including pieces.
    draw_board():
        Draws the board itself: border, background, triangles.
    get_clicked_column(x_coord, y_coord):
        Decides which column / space corresponds to the given coordinates, if any.
    """

    def __init__(self, canvas, turn_label, turn, light_count_label, dark_count_label, game_window):
        """
        Provides all the necessary attributes to simulate a backgammon game board.

        Sets the initial piece positions and the column coordinates.

        Parameters
        ----------
        canvas : tkinter.Canvas
            the visuals of the board, including pieces
        turn_label : tkinter.Label
            displays whose turn it is, with additional messages to the player(s)
        turn : int
            index of the player who / must make a move, 1 or 2
        light_count_label : tkinter.Label
            displays how many pieces player 1 bore off
        dark_count_label : tkinter.Label
            displays how many pieces player 2 bore off
        game_window : tkinter.Frame
            contains all the information of the game screen, to be deleted on win screen transition
        """

        self.game_window = game_window
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
        self.columns[24] = [self.base_x+700, self.base_y + 400, 0, 0]

    def draw_piece(self, x, y, color):
        """
        Draws one circular checker piece at the specified x and y coordinates, in the specified color.

        Parameters
        ----------
        x : int
            x coordinate of the center of the piece
        y : int
            y coordinate of the center of the piece
        color : string
            color code to fill the circle

        Returns
        -------
        None
        """

        self.canvas.create_oval(x - self.piece_radius, y - self.piece_radius,
                                x + self.piece_radius, y + self.piece_radius, fill=color)

    def place_pieces(self):
        """
        (re)Places all pieces on the board, according to their last saved position.

        Returns
        -------
        None
        """

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
        """
        Handles left mouse button click event from player(s).

        Parameters
        ----------
        event : Event
            left mouse button click event on the canvas

        Returns
        -------
        None
        """

        clicked_x, clicked_y = event.x, event.y
        clicked_column = self.get_clicked_column(clicked_x, clicked_y)
        self.decide_action(clicked_column)

    def decide_action(self, clicked_column):
        """
        Decides what action to take on click event.

        If no selected piece, set clicked column as selected. If piece already selected check if move is valid.
        If move is not valid, let the player know. If player has no more valid moves, let the player know.
        Change turns and declare winner when viable.

        Parameters
        ----------
        clicked_column : int
            index of the clicked column, 0 to 24

        Returns
        -------
        None
        """

        if len(self.dice) > 0:
            if self.valid_move_exists()[0]:
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
        """
        Decides whether moving selected_piece to clicked_column is a valid move.

        It respects all the original rules of the game. It also returns which dice move was used, so that it can be
        removed from the list.

        Parameters
        ----------
        clicked_column : int, optional
            index of the clicked column, 0 to 24, or None if outside the board
        selected_piece : int
            the index of the column from which a piece was selected

        Returns
        -------
        (bool, int)
        """

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
        """
        Decides if there are any possible valid moves left in the current game state.

        It respects all the original rules of the game. All moves are checked from lowest to highest index.
        Returns bool, clicked_column and selected_piece, in that order.

        Returns
        -------
        (bool, int, int)
        """
        valid_moves = []
        if self.columns[24][self.turn+1] != 0:
            for i in range(24):
                if self.valid_move(i, 24)[0]:
                    valid_moves.append((i, 24))
        else:
            for i in range(24):
                if self.columns[i][self.turn+1] != 0:
                    for j in range(24):
                        if self.valid_move(j, i)[0]:
                            valid_moves.append((j, i))
                    if self.valid_move(None, i)[0]:
                        valid_moves.append((None, i))
        if len(valid_moves) == 0:
            return False, None, None
        move = random.choice(valid_moves)
        return True, move[0], move[1]

    def redraw_board(self):
        """
        Redraws all elements of the board, including pieces.

        Returns
        -------
        None
        """

        self.canvas.delete("all")
        self.draw_board()
        self.place_pieces()

    def draw_board(self):
        """
        Draws the board itself: border, background, triangles.

        Returns
        -------
        None
        """

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
            self.canvas.create_polygon(x_left + 710, y_top_base, x_right + 710, y_top_base, (x_left + x_right) / 2 +
                                       710, y_top_tip, outline="#654426", fill=fill_color_top)
            self.canvas.create_polygon(x_left, y_bottom_base, x_right, y_bottom_base, (x_left + x_right) / 2,
                                       y_bottom_tip, outline="#654426", fill=fill_color_bottom)
            self.canvas.create_polygon(x_left + 710, y_bottom_base, x_right + 710, y_bottom_base,
                                       (x_left + x_right) / 2 + 710, y_bottom_tip, outline="#654426",
                                       fill=fill_color_bottom)

    def get_clicked_column(self, x_coord, y_coord):
        """
        Decides which column / space corresponds to the given coordinates, if any.

        Returns
        -------
        int
        """
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
    """
    Rolls two dice during a game, displaying the resulting integers and updating the values for environment logic.

    Parameters
    ----------
    result_label : tkinter.Label
        holds the results of a dice roll
    backgammon_board : BackgammonBoard
        the current game environment

    Returns
    -------
    None
    """

    if len(backgammon_board.dice) == 0:
        dice_value_1 = random.randint(1, 6)
        dice_value_2 = random.randint(1, 6)
        result_label.config(text=f"{dice_value_1}, {dice_value_2}", font=("Eras Medium ITC", 50))
        if dice_value_1 == dice_value_2:
            backgammon_board.dice = [dice_value_1] * 4
        else:
            backgammon_board.dice = [dice_value_1, dice_value_2]


def roll_turn(result_label, player_nr):
    """
    Rolls two dice for preliminary rolls, displaying the resulting integers.

    Parameters
    ----------
    result_label : tkinter.Label
        holds the results of a dice roll
    player_nr : int
        the index of the rolling player

    Returns
    -------
    None
    """

    if len(result_label.cget("text")) <= 10:
        dice_value_1 = random.randint(1, 6)
        dice_value_2 = random.randint(1, 6)
        result_label.config(text=f"Player {player_nr}: {dice_value_1}, {dice_value_2}", font=("Eras Medium ITC", 50))


def check_who_starts(result_label_1, result_label_2, winner_label, dice_frame, game_mode):
    """
    Rolls two dice for preliminary rolls, displaying the resulting integers.

    Parameters
    ----------
    result_label_1 : tkinter.Label
        holds the results of player 1's dice roll
    result_label_2 : tkinter.Label
        holds the results of player 2's dice roll
    winner_label : tkinter.Label
        holds the results of the preliminary rolls
    dice_frame : tkinter.Frame
        holds all preliminary screen information, for deletion on screen transition
    game_mode : int
        number of human players, 1 or 2, for propagation on screen transition


    Returns
    -------
    None
    """

    if len(result_label_1.cget("text")) > 10 and len(result_label_2.cget("text")) > 10:
        rolls_1 = []
        for i in result_label_1.cget("text"):
            if i.isdigit():
                rolls_1.append(int(i))
        rolls_2 = []
        for i in result_label_2.cget("text"):
            if i.isdigit():
                rolls_2.append(int(i))

        if sum(rolls_1)-1 == sum(rolls_2)-2:
            winner_label.config(text="Roll again!")
            result_label_1.config(text="Player 1: ")
            if game_mode == 2:
                result_label_2.config(text="Player 2: ")
            else:
                roll_turn(result_label_2, 2)
        else:
            winner = 1 if sum(rolls_1) > sum(rolls_2) else 2
            winner_label.config(text=f"Player {winner} wins!")
            root.after(3000, lambda: start_game(game_mode, dice_frame, winner))


def deselect_piece(backgammon_board):
    """
    Deselects piece during a turn, to avoid getting stuck.

    Parameters
    ----------
    backgammon_board : BackgammonBoard
        the current game environment

    Returns
    -------
    None
    """

    backgammon_board.selected_piece = None
    backgammon_board.turn_label.config(text=f"Player {backgammon_board.turn}'s Turn")


def win_screen(game_window, winner):
    """
    Generates UI of win screen when a player finishes the game.

    Displays who won and a back to main menu button.

    Parameters
    ----------
    game_window : tkinter.Frame
        holds all the content of the previous screen, for deletion
    winner : int
        the index of the winning player, 1 or 2

    Returns
    -------
    None
    """

    game_window.destroy()
    win_frame = tk.Frame(root, bg="#654426")
    win_frame.pack(fill=tk.BOTH, expand=True)
    title_label = tk.Label(win_frame, text=f"Player {winner} won !! :D", bg="#654426", fg="#f5eee8",
                           font=("Eras Bold ITC", 70))
    title_label.pack(pady=(300, 50))
    back_button = tk.Button(win_frame, text="Back to main menu", bg="#90663f", fg="#f5eee8",
                            command=lambda: create_start_menu(win_frame), font=("Eras Medium ITC", 35))
    back_button.pack()


def start_game(game_mode, preliminary_frame, starting_player):
    """
    Generates UI of game screen after turns are decided.

    Displays whose turn it is, the game board, rolled dice values and number of borne off pieces per player.
    Offers dice roll and piece deselect buttons.

    Parameters
    ----------
    game_mode : int
        number of human players, 1 or 2
    preliminary_frame : tkinter.Frame
        holds all the content of the previous screen, for deletion
    starting_player : int
        index of player who goes first, 1 or 2

    Returns
    -------
    None
    """

    preliminary_frame.destroy()
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
    if game_mode == 1:
        ai_player = AIPlayer(backgammon_board, result_label)
        ai_player.start_ai_thread()


def preliminary_rolls(game_mode, start_menu):
    """
    Generates UI of game screen where turns are decided.

    Displays each player's rolls, buttons to roll and whp the winner is. Transitions to next screen after 3 seconds.
    If players roll the same sum of dice, values are reset.

    Parameters
    ----------
    game_mode : int
        number of human players, 1 or 2
    start_menu : tkinter.Frame
        holds all the content of the previous screen, for deletion

    Returns
    -------
    None
    """

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
                                               check_who_starts(result_label_1, result_label_2, winner_label,
                                                                dice_frame, game_mode)),
                              font=("Eras Medium ITC", 20))
    roll_button_1.pack(pady=10)
    result_label_2 = tk.Label(dice_frame, text="Player2: ", bg="#654426", fg="#f5eee8", font=("Eras Medium ITC", 50))
    result_label_2.pack(pady=10)
    if game_mode == 2:
        roll_button_2 = tk.Button(dice_frame, text="Roll Dice", bg="#90663f", fg="#f5eee8",
                                  command=lambda: (roll_turn(result_label_2, 2),
                                                   check_who_starts(result_label_1, result_label_2, winner_label,
                                                                    dice_frame, game_mode)),
                                  font=("Eras Medium ITC", 20))
        roll_button_2.pack(pady=10)
    else:
        roll_turn(result_label_2, 2)


def create_start_menu(win_frame=None):
    """
    Generates UI of main menu screen, where players can decide between the 2 game modes

    Parameters
    ----------
    win_frame: tkinter.Frame, optional
        holds all the content of the previous screen, if any, for deletion

    Returns
    -------
    None
    """

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
    create_start_menu()
    root.mainloop()
