Question 4: Gridworld Q-Learning
-

Description
-
Applies Q-learning to a 5×5 Gridworld with two special teleport states (A and B). Trains an agent using ε-greedy policy and displays the optimal value function and policy.


File
-
question4.py – Implements environment (step function), ε-greedy Q-learning, extract_policy, print_value, print_policy functions
notebook.ipynb – Jupyter notebook version with training cell, and detailed explanations

Dependencies
-
• Python 3.x (no extra libraries required)

Usage
-

Script mode:
python question4.py

This will:
– Print initialization info and training progress every 1000 episodes
– After training, display:
• Optimal value function grid (numerical)
• Optimal policy as words (north/south/east/west)
• Optimal policy as arrows (↑/↓/→/←)

Notebook mode:
-
1.	Open notebook.ipynb in Jupyter
2.	Run the training cell to compute and display V and policies

Project Overview
-
Environment: teleport logic for A and B, boundary penalties for off-grid moves

Q-learning:
choose_action(): ε-greedy action selection
train(): Bellman update over episodes

Policy extraction: derive V(s) = max_a Q(s,a), and greedy policy in both word and arrow formats


Outputs
-
Console logs of training progress

Printed optimal value function and policy grids matching theoretical quantities in Figure 2


