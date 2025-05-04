Question 1: Informed Search Maze Solver
---------------------------------------


-----------
Description
-----------

This project implements Greedy Best-First Search and A* search on maze puzzles defined in text files. It provides both terminal and PNG visualizations of the search. Files
-


 question1.py – Contains Node and Maze classes, search implementations, drawing and terminal output
 Easy/, Medium/, Hard/ – Each folder contains one .txt maze input and will contain the generated .png images



Dependencies
-
 Python 3.x
 Pillow library (install via pip install pillow)

Instructions
-
1.	Place your maze text file in Easy/, Medium/, Hard/ as easy.txt, medium.txt, hard.txt

2.	Run the solver: python maze.py

What to Expect from the Script
- 

Parse each maze, strip any full border
– Run “original” draw, Greedy best-first search, and A* search
– Print expansion counts, run times, and path lengths to the terminal
– Save images named easy_original.png, easy_greedy.png, easy_astar.png (and similarly for Medium and Hard)


Project Overview
-
• Maze class: loads grid, identifies walls, start and goal, provides neighbour generation and heuristic (Manhattan distance)
• Node class: stores state, parent, action, cost (g) and priority (h or g+h)
• solve(algorithm): uses heapq frontier, explored set, returns path and explored states
• draw(): creates an RGB image with colored walls, explored cells, path, and overlaid cost/heuristic values
• print_terminal(): ANSI-colored ASCII display in the console

Outputs
-
• Terminal logs showing “GREEDY” and “ASTAR” statistics
• PNG images in each folder showing the search progression and final path


