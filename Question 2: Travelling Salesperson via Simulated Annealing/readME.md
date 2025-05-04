Question 2: Travelling Salesperson via Simulated Annealing
-

Description
-
Solves the TSP for 10 Namibian towns using a Simulated Annealing heuristic, with brute-force comparison on a 5-town subset and analysis of parameters and scalability.


Files
-
question2.py – Defines TSP and SimulatedAnnealingSolver classes and runs the algorithm

notebook.ipynb – Jupyter notebook version with multi-cell layout, plots, brute-force code snippets, and discussion


Dependencies
-
Python 3.x

NumPy (install via pip install numpy)

Matplotlib (install via pip install matplotlib)


Usage
Script mode:
python question2.py

This prints
-
– Initial random route and its total distance
– Best route found and its total distance
– Displays two plots: convergence of best cost over iterations, and circular layout of the best route

Notebook mode:
-
1.	Open notebook.ipynb in Jupyter
2.	Run cells in order to see code, printed results, brute-force comparison for 5 towns, parameter sensitivity discussion, and scalability reflection

Project Overview
-
TSP class: stores list of town names and a distance matrix; method total_distance(route) computes the sum of distances

SimulatedAnnealingSolver class:

_initial_route(): generates random permutation fixing Windhoek as start and end

_neighbor(): produces candidate by swapping two intermediate towns

solve(): applies Metropolis acceptance criterion at temperature T, cools by factor alpha, records best route and cost history

Brute-force snippet: verifies optimal route on a 5-town subset for comparison

Analysis: discusses the effect of temperature (T0), cooling rate (alpha), iteration count (max_iters), and scalability for larger problems


Outputs
-

Console printout of routes and costs

Convergence plot (best cost vs. iterations)

Circular route visualization plot


