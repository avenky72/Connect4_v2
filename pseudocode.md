function minimax(board, depth, alpha, beta, is_maximizing_player):
    if check_win(board, -1):  // Computer wins
        return 1
    else if check_win(board, 1):  // User wins
        return -1
    else if is_board_full(board):  // Draw
        return 0
    
    if is_maximizing_player:
        best_score = -infinity
        for each empty_cell in board:
            board[empty_cell] = -1  // Make move for computer
            score = minimax(board, depth + 1, alpha, beta, False)
            board[empty_cell] = 0  // Undo move
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  // Beta cut-off
        return best_score
    else:
        best_score = +infinity
        for each empty_cell in board:
            board[empty_cell] = 1  // Make move for user
            score = minimax(board, depth + 1, alpha, beta, True)
            board[empty_cell] = 0  // Undo move
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  // Alpha cut-off
        return best_score


Initialize the game board and UI.
Implement player move handling and piece placement.
Develop the minimax algorithm with alpha-beta pruning for the computer's moves.
Add game mechanics for bomb and freeze pieces.
Check for win and draw conditions after each move.