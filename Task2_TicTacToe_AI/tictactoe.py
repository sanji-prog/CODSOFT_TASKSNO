import math
 
HUMAN = "X"
AI = "O"
EMPTY = " "
 
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]
 
 
def print_board(board):
    print()
    for r in range(3):
        row = board[r * 3:(r + 1) * 3]
        print(" " + " | ".join(row))
        if r < 2:
            print("---+---+---")
    print()
 
 
def winner(board):
    """Return 'X' or 'O' if someone has won, otherwise None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None
 
 
def is_full(board):
    return EMPTY not in board
 
 
def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]
 
 
def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Minimax with Alpha-Beta Pruning.
    AI (O) is the maximizing player, HUMAN (X) is the minimizing player.
    Score: +10 - depth if AI wins, depth - 10 if human wins, 0 for a draw.
    Using depth makes the AI prefer faster wins and slower losses.
    """
    result = winner(board)
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if is_full(board):
        return 0
 
    if is_maximizing:
        best = -math.inf
        for move in available_moves(board):
            board[move] = AI
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move] = EMPTY
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:  # prune
                break
        return best
    else:
        best = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move] = EMPTY
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:  # prune
                break
        return best
 
 
def best_ai_move(board):
    """Pick the move with the highest minimax score for the AI."""
    best_score = -math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
 
 
def get_human_move(board):
    while True:
        choice = input("Your move (1-9): ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Please enter a number from 1 to 9.")
            continue
        move = int(choice) - 1
        if board[move] != EMPTY:
            print("That spot is already taken. Try another.")
            continue
        return move
 
 
def play_game():
    board = [EMPTY] * 9
 
    print("=" * 40)
    print("  Tic-Tac-Toe AI (CodSoft Task 2)")
    print("  You are X, the AI is O. Can you beat it?")
    print("=" * 40)
 
    first = input("Do you want to go first? (y/n): ").strip().lower()
    human_turn = first != "n"
 
    print_board(board)
 
    while True:
        if human_turn:
            board[get_human_move(board)] = HUMAN
        else:
            print("AI is thinking...")
            board[best_ai_move(board)] = AI
 
        print_board(board)
 
        result = winner(board)
        if result == HUMAN:
            print("You win! (This should be impossible...)")
            break
        if result == AI:
            print("AI wins! Better luck next time.")
            break
        if is_full(board):
            print("It's a draw!")
            break
 
        human_turn = not human_turn
 
 
def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
 
 
if __name__ == "__main__":
    main()
