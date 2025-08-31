import math

X = "X"
O = "O"
EMPTY = None
SIZE = 3


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibilities = set()
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] is EMPTY:
                possibilities.add((i, j))
    return possibilities


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    
    board_copy = [row[:] for row in board]

    i, j = action
    if board_copy[i][j] is not EMPTY:
        raise Exception("Cell already occupied")
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def isWinner(player):
        for row in board:
            if all(cell == player for cell in row):
                return True
        for col in range(SIZE):
            if all(board[row][col] == player for row in range(SIZE)):
                return True
        if all(board[i][i] == player for i in range(SIZE)):
            return True
        if all(board[i][SIZE - 1 - i] == player for i in range(SIZE)):
            return True

        return False
    
    if isWinner(X):
        return X    
    elif isWinner(O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def maxVal(board):
    """
    returns the maximum utility X can guarantee from this board.
    """
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, minVal(result(board, action)))
    return v


def minVal(board):
    """
    returns the minimum utility O can guarantee from this board.
    """
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, maxVal(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    best_action = None
    best_value = -math.inf if player(board) == X else math.inf
    
    if player(board) == X:
        for action in actions(board):
            value = minVal(result(board, action))
            if value > best_value:
                best_value, best_action = value, action
        return best_action
    else:
        for action in actions(board):
            value = maxVal(result(board, action))
            if value < best_value:
                best_value, best_action = value, action
        return best_action