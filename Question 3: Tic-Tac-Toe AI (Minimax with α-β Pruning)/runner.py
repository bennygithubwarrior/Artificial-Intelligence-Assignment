import tkinter as tk
from tkinter import messagebox, ttk
from tictactoe import (
    initial_state, player, actions, result,
    winner, terminal, ai_move, X, O, EMPTY
)

BG_COLOR = "#f7f7f7"
BUTTON_BG = "#ffffff"
# X and O are shown in black instead of colored
X_COLOR = "black"
O_COLOR = "black"

# use a color emoji capable font when available
import sys

if sys.platform == "win32":
    EMOJI_FONT = "Segoe UI Emoji"
else:
    EMOJI_FONT = "Noto Color Emoji"

# default fonts
FONT_LARGE = (EMOJI_FONT, 20, "bold")
FONT_MED = (EMOJI_FONT, 16)
FONT_SMALL = (EMOJI_FONT, 14)

class TicTacToeGUI:
    """Main window for playing Tic-Tac-Toe."""

    def __init__(self, master):
        """Set up styles and show the initial configuration screen."""
        self.master = master
        master.title("Tic-Tac-Toe")
        master.configure(bg=BG_COLOR)
        self.style = ttk.Style(master)
        self.style.configure(
            "Big.TRadiobutton",
            indicatorsize=20,
            background=BG_COLOR,
            font=FONT_MED,
            foreground="black",
            focusthickness=0,
            focuscolor=BG_COLOR,
        )
        self.style.map(
            "Big.TRadiobutton",
            indicatorcolor=[("selected", "black")],
            foreground=[("selected", "black")],
            focuscolor=[("pressed", BG_COLOR), ("!pressed", BG_COLOR)],
        )
        self.setup_screen()

    def clear_widgets(self):
        """Remove all widgets from the window."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def setup_screen(self):
        """Display the mode and difficulty selection screen."""
        self.clear_widgets()
        self.mode_var = tk.StringVar(value="1")
        self.user_sym_var = tk.StringVar(value=X)
        self.diff_var = tk.StringVar(value="hard")
        self.diff_x_var = tk.StringVar(value="hard")
        self.diff_o_var = tk.StringVar(value="hard")

        self.setup_frame = tk.Frame(self.master, padx=20, pady=20, bg=BG_COLOR)
        self.setup_frame.pack()

        tk.Label(
            self.setup_frame,
            text="Select Game Mode",
            font=FONT_LARGE,
            bg=BG_COLOR,
        ).pack(pady=5)
        mode_frame = tk.Frame(self.setup_frame, bg=BG_COLOR)
        mode_frame.pack(pady=5)
        ttk.Radiobutton(
            mode_frame,
            text="You vs Computer",
            variable=self.mode_var,
            value="1",
            command=self.update_setup,
            style="Big.TRadiobutton",
            takefocus=False,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            mode_frame,
            text="Computer vs Computer",
            variable=self.mode_var,
            value="2",
            command=self.update_setup,
            style="Big.TRadiobutton",
            takefocus=False,
        ).pack(side=tk.LEFT, padx=5)

        self.user_frame = tk.Frame(self.setup_frame, bg=BG_COLOR)
        tk.Label(self.user_frame, text="Your symbol", bg=BG_COLOR, font=FONT_MED).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            self.user_frame,
            text="X",
            variable=self.user_sym_var,
            value=X,
            style="Big.TRadiobutton",
            takefocus=False,
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            self.user_frame,
            text="O",
            variable=self.user_sym_var,
            value=O,
            style="Big.TRadiobutton",
            takefocus=False,
        ).pack(side=tk.LEFT)

        self.diff_frame = tk.Frame(self.setup_frame, bg=BG_COLOR)
        tk.Label(self.diff_frame, text="Computer difficulty", bg=BG_COLOR, font=FONT_MED).pack(side=tk.LEFT, padx=5)
        for diff in ("easy", "medium", "hard"):
            ttk.Radiobutton(
                self.diff_frame,
                text=diff.title(),
                variable=self.diff_var,
                value=diff,
                style="Big.TRadiobutton",
                takefocus=False,
            ).pack(side=tk.LEFT)

        self.comp_frame = tk.Frame(self.setup_frame, bg=BG_COLOR)
        tk.Label(self.comp_frame, text="Computer X difficulty", bg=BG_COLOR, font=FONT_MED).grid(row=0, column=0, padx=5, pady=2, sticky="e")
        for i, diff in enumerate(("easy", "medium", "hard")):
            ttk.Radiobutton(
                self.comp_frame,
                text=diff.title(),
                variable=self.diff_x_var,
                value=diff,
                style="Big.TRadiobutton",
                takefocus=False,
            ).grid(row=0, column=i + 1, padx=2, pady=2)
        tk.Label(self.comp_frame, text="Computer O difficulty", bg=BG_COLOR, font=FONT_MED).grid(row=1, column=0, padx=5, pady=2, sticky="e")
        for i, diff in enumerate(("easy", "medium", "hard")):
            ttk.Radiobutton(
                self.comp_frame,
                text=diff.title(),
                variable=self.diff_o_var,
                value=diff,
                style="Big.TRadiobutton",
                takefocus=False,
            ).grid(row=1, column=i + 1, padx=2, pady=2)

        tk.Button(
            self.setup_frame,
            text="Start Game",
            command=self.start_game,
            bg="#4CAF50",
            fg="white",
            font=FONT_LARGE,
            padx=10,
            pady=5,
        ).pack(pady=10)
        self.update_setup()

    def update_setup(self):
        """Toggle option panels based on selected mode."""
        if self.mode_var.get() == "1":
            self.user_frame.pack(pady=5)
            self.diff_frame.pack(pady=5)
            self.comp_frame.pack_forget()
        else:
            self.user_frame.pack_forget()
            self.diff_frame.pack_forget()
            self.comp_frame.pack(pady=5)

    def start_game(self):
        """Initialize a new game and let the AI start if needed."""
        self.mode = self.mode_var.get()
        if self.mode == "1":
            self.user_sym = self.user_sym_var.get()
            self.ai_diff = self.diff_var.get()
        else:
            self.user_sym = None
            self.ai_diff = {X: self.diff_x_var.get(), O: self.diff_o_var.get()}
        self.state = initial_state()
        self.moves = []
        self.draw_board()
        if self.mode == "2":
            self.master.after(500, self.ai_turn)
        elif self.mode == "1" and self.user_sym != player(self.state):
            self.master.after(500, self.ai_turn)

    def draw_board(self):
        """Create the board grid and status label."""
        self.clear_widgets()
        self.frame = tk.Frame(self.master, padx=10, pady=10, bg=BG_COLOR)
        self.frame.pack()
        self.buttons = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.frame,
                    text=" ",
                    width=6,
                    height=3,
                    font=(EMOJI_FONT, 32, "bold"),
                    command=lambda i=i, j=j: self.cell_clicked(i, j),
                    bg=BUTTON_BG,
                    fg="black",
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        self.status = tk.Label(
            self.master,
            text=f"Player {player(self.state)} to move",
            font=FONT_MED,
            bg=BG_COLOR,
        )
        self.status.pack(pady=10)

    def update_board(self):
        """Refresh the buttons to show the current board."""
        sym = {X: "X", O: "O", EMPTY: " "}
        colors = {X: X_COLOR, O: O_COLOR, EMPTY: "black"}
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(
                    text=sym[self.state[i][j]], fg=colors[self.state[i][j]]
                )
        # ensure updates are drawn immediately
        self.master.update_idletasks()

    def cell_clicked(self, i, j):
        """Handle a click on the board by the human player."""
        if terminal(self.state):
            return
        if self.mode == "1" and player(self.state) == self.user_sym:
            if (i, j) in actions(self.state):
                self.state = result(self.state, (i, j))
                self.moves.append((i, j))
                self.update_board()
                self.after_move()
            else:
                messagebox.showwarning("Invalid Move", "Cell already taken.")

    def after_move(self):
        """Check game status and queue the next turn."""
        if terminal(self.state):
            self.game_over()
        else:
            self.status.configure(text=f"Player {player(self.state)} to move")
            if self.mode == "1" and player(self.state) != self.user_sym:
                self.master.after(300, self.ai_turn)
            elif self.mode == "2":
                self.master.after(300, self.ai_turn)

    def ai_turn(self):
        """Make the AI move and update the board."""
        if terminal(self.state):
            return
        cur = player(self.state)
        diff = self.ai_diff if self.mode == "1" else self.ai_diff[cur]
        mv = ai_move(self.state, diff)
        self.state = result(self.state, mv)
        self.moves.append(mv)
        self.update_board()
        self.after_move()

    def game_over(self):
        """Show the final result and ask about replay."""
        w = winner(self.state)
        if w:
            if self.mode == "1":
                msg = "You win! 🎉🎉" if w == self.user_sym else "Computer wins! 😢😢"
            else:
                msg = f"Computer {w} wins! 🎉🎉"
        else:
            msg = "It's a tie! 😐😐"
        self.status.configure(text=msg)
        if messagebox.askyesno("Game Over", f"{msg}\nWatch replay?"):
            self.replay_game()
        else:
            self.post_game_prompt()

    def post_game_prompt(self):
        """Prompt to play again or exit."""
        if messagebox.askyesno("Game Over", "Play again?"):
            self.setup_screen()
        else:
            self.master.destroy()

    def replay_game(self):
        """Animate the recorded moves one by one."""
        original_moves = self.moves[:]
        self.state = initial_state()
        self.update_board()

        def step(i=0):
            if i < len(original_moves):
                self.state = result(self.state, original_moves[i])
                self.update_board()
                self.master.after(600, lambda: step(i + 1))
            else:
                self.master.after(500, self.post_game_prompt)

        step()


def main():
    """Entry point to launch the GUI application."""
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
