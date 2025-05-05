import random   # for random action selection

# Gridworld settings
GRID_SIZE = 5
A_POS = (0, 1)                # special state A
B_POS = (0, 3)                # special state B
A_PRIME = (4, 1)              # teleport target for A
B_PRIME = (2, 3)              # teleport target for B
SPECIAL_REWARDS = {A_POS: 10, B_POS: 5}
TELEPORTS = {A_POS: A_PRIME, B_POS: B_PRIME}

# Q-learning parameters
GAMMA = 0.9                   # discount factor
ALPHA = 0.2                   # learning rate
EPSILON = 0.1                 # exploration rate
EPISODES = 5000               # number of training episodes
MAX_STEPS = 5000              # max steps per episode

# Possible actions
ACTIONS = ['north', 'south', 'east', 'west']
# Initialize Q-values: Q[(i,j,action)] = 0.0
Q = {
    (i, j, a): 0.0
    for i in range(GRID_SIZE)
    for j in range(GRID_SIZE)
    for a in ACTIONS
}

def step(state, action):
    """Return next state and reward after taking action from state."""
    # Handle teleport states
    if state in TELEPORTS:
        return TELEPORTS[state], SPECIAL_REWARDS[state]

    i, j = state
    # Compute tentative next position
    if action == 'north':
        ni, nj = max(i - 1, 0), j
    elif action == 'south':
        ni, nj = min(i + 1, GRID_SIZE - 1), j
    elif action == 'east':
        ni, nj = i, min(j + 1, GRID_SIZE - 1)
    else:  # 'west'
        ni, nj = i, max(j - 1, 0)

    # Check if move hit the boundary
    off_edge = (
        ni == i and nj == j and
        ((i == 0 and action == 'north') or
         (i == GRID_SIZE - 1 and action == 'south') or
         (j == 0 and action == 'west') or
         (j == GRID_SIZE - 1 and action == 'east'))
    )
    if off_edge:
        return state, -1  # penalty for invalid move

    return (ni, nj), 0  # normal move, zero reward

def choose_action(state):
    """Select an action via ε-greedy policy."""
    if random.random() < EPSILON:
        return random.choice(ACTIONS)
    # pick best action(s) based on current Q-values
    vals = [Q[(state[0], state[1], a)] for a in ACTIONS]
    max_val = max(vals)
    best = [a for a, v in zip(ACTIONS, vals) if v == max_val]
    return random.choice(best)

def train():
    """Run Q-learning over multiple episodes."""
    print("\n--- Training in progress ---")
    for ep in range(1, EPISODES + 1):
        # start from a random cell
        state = (random.randrange(GRID_SIZE), random.randrange(GRID_SIZE))
        for _ in range(MAX_STEPS):
            action = choose_action(state)
            next_state, reward = step(state, action)
            # Bellman update
            future_vals = [Q[(next_state[0], next_state[1], a)] for a in ACTIONS]
            target = reward + GAMMA * max(future_vals)
            Q[(state[0], state[1], action)] = (
                (1 - ALPHA) * Q[(state[0], state[1], action)] +
                ALPHA * target
            )
            state = next_state
        if ep % 1000 == 0:
            print(f"  Completed {ep}/{EPISODES} episodes")
    print("\nTraining complete.")

def extract_policy():
    """Derive optimal value function and policy from learned Q."""
    V = [[0.0] * GRID_SIZE for _ in range(GRID_SIZE)]
    policy_words = [[''] * GRID_SIZE for _ in range(GRID_SIZE)]
    policy_arrows = [[''] * GRID_SIZE for _ in range(GRID_SIZE)]
    arrows = {'north': '↑', 'south': '↓', 'east': '→', 'west': '←'}

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            vals = [Q[(i, j, a)] for a in ACTIONS]
            best_idx = vals.index(max(vals))
            best_action = ACTIONS[best_idx]
            V[i][j] = round(vals[best_idx], 2)
            policy_words[i][j] = best_action
            policy_arrows[i][j] = arrows[best_action]

    return V, policy_words, policy_arrows

def print_value(V):
    """Print the value function grid."""
    print("\nOptimal Value Function:")
    for row in V:
        print(" ".join(f"{v:5.2f}" for v in row))

def print_policy_words(policy):
    """Print the policy as action words."""
    print("\nOptimal Policy:")
    for row in policy:
        print(" ".join(f"{w:<5}" for w in row))

def print_policy_arrows(arrows):
    """Print the policy as directional arrows."""
    print("\nOptimal Policy (arrows):")
    for row in arrows:
        print(" ".join(f"{a:^3}" for a in row))

if __name__ == "__main__":
    # Display setup information
    print("Initializing Gridworld...")
    print(f"Grid size:            {GRID_SIZE}×{GRID_SIZE}")
    print(f"Special_states:       A at {A_POS}, B at {B_POS}")
    print(f"Teleport targets:     A′ at {A_PRIME}, B′ at {B_PRIME}")
    print(f"Teleport rewards:     A→{SPECIAL_REWARDS[A_POS]}, B→{SPECIAL_REWARDS[B_POS]}")
    print("\nStarting Q-learning with parameters:")
    print(f" γ = {GAMMA}")
    print(f" ε = {EPSILON}")
    print(f" α = {ALPHA}")
    print(f" Episodes = {EPISODES}")
    print(f" Steps = {MAX_STEPS}")

    train()  # run the training loop

    print("\nEvaluating optimal value function and policy…")
    V_opt, w_opt, a_opt = extract_policy()
    print_value(V_opt)
    print_policy_words(w_opt)
    print_policy_arrows(a_opt)
