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

runner.py – CLI interface for human vs AI or AI vs AI, with board display and replay feature

notebook.ipynb – Jupyter notebook version with in-depth explanations and demo


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

Play the game in the terminal

Optionally replay the move sequence

Notebook mode:
-
1.	Open notebook.ipynb in Jupyter
   
2.	Run cells to explore code, play a quick demo, and review detailed explanation of Minimax and α-β pruning


Project Overview
-
Game logic: initial_state(), player(), actions(), result(), winner(), terminal(), utility()

Minimax with α-β pruning (minimax_ab): max_value and min_value functions implement recursive search with cutoffs

ai_move(): selects actions based on difficulty level

runner CLI: input validation, board printing, turn loop, replay for move analysis

Outputs
-
Terminal display of the board

AI thinking messages and chosen moves

End-of-game messages with emojis (win/lose/draw)

Replay of move sequence for analysis


