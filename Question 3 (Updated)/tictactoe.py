import math      # for infinity constants
import copy      # for deep-copying board states
import random    # for random move selection

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """Return a new 3×3 empty board."""
    return [[EMPTY] * 3 for _ in range(3)]

def player(board):
    """Return the player who has the next turn on the board."""
    x_count = sum(r.count(X) for r in board)
    o_count = sum(r.count(O) for r in board)
    return X if x_count == o_count else O

def actions(board):
    """Return set of all empty cell coordinates (i, j)."""
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}

def result(board, action):
    """Return the board that results from making move at action."""
    if action not in actions(board):
        raise ValueError("Invalid move")
    b = copy.deepcopy(board)
    b[action[0]][action[1]] = player(board)
    return b

def winner(board):
    """Return X or O if there is a winner, else None."""
    lines = [
        # rows
        [(i, 0) for i in range(3)], [(i, 1) for i in range(3)], [(i, 2) for i in range(3)],
        # columns
        [(0, i) for i in range(3)], [(1, i) for i in range(3)], [(2, i) for i in range(3)],
        # diagonals
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)],
    ]
    for line in lines:
        vals = [board[i][j] for i, j in line]
        if vals == [X] * 3:
            return X
        if vals == [O] * 3:
            return O
    return None

def terminal(board):
    """Return True if game is over (win or no empty cells)."""
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    """Return 1 if X wins, -1 if O wins, 0 otherwise."""
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0

def minimax_ab(board):
    """Return optimal move using Minimax with α-β pruning."""
    def max_value(b, α, β):
        if terminal(b):
            return utility(b), None
        v, move = -math.inf, None
        for a in actions(b):
            min_v, _ = min_value(result(b, a), α, β)
            if min_v > v:
                v, move = min_v, a
                α = max(α, v)
            if v >= β:
                break  # β-cutoff
        return v, move

    def min_value(b, α, β):
        if terminal(b):
            return utility(b), None
        v, move = math.inf, None
        for a in actions(b):
            max_v, _ = max_value(result(b, a), α, β)
            if max_v < v:
                v, move = max_v, a
                β = min(β, v)
            if v <= α:
                break  # α-cutoff
        return v, move

    cur = player(board)
    if cur == X:
        return max_value(board, -math.inf, math.inf)[1]
    else:
        return min_value(board, -math.inf, math.inf)[1]

def minimax(board):
    """Alias to α-β minimax for a move choice."""
    return minimax_ab(board)

def ai_move(board, difficulty="hard"):
    """Return AI move based on difficulty setting."""
    avail = list(actions(board))
    if difficulty.lower() == "easy":
        return random.choice(avail)
    if difficulty.lower() == "medium" and random.random() < 0.5:
        return random.choice(avail)
    # hard mode or fallback
    return minimax(board)
