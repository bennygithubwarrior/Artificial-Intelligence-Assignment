Question 3: Tic-Tac-Toe AI (Minimax with α-β Pruning)
-

Description
-
Implements a Tic-Tac-Toe game with three AI difficulty levels:
Easy: random moves
Medium: 50% random, 50% optimal
Hard: full Minimax with α-β pruning (unbeatable)


Files
-
tictactoe.py – Core game logic, state handling, Minimax+α-β pruning, ai_move wrapper

runner.py – GUI interface for human vs AI or AI vs AI, with board display and replay feature

Dependencies
-
• Python 3.x (no additional libraries required)


Usage
-
Script mode:

python runner.py

Follow on-screen prompts:

Choose game mode (1=You vs AI, 2=AI vs AI)

Select symbol and difficulty

Play the game in the GUI

Optionally replay the move sequence

Project Overview
-
Game logic: initial_state(), player(), actions(), result(), winner(), terminal(), utility()

Minimax with α-β pruning (minimax_ab): max_value and min_value functions implement recursive search with cutoffs

ai_move(): selects actions based on difficulty level


Outputs
-
GUI display of the board

End-of-game messages with emojis (win/lose/draw)

Replay of move sequence for analysis


