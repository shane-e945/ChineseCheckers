from ChineseCheckers import ChineseCheckers

def move_arm(start_pos, end_pos) -> None:
    """Makes the arm move the marble from start_pos to end_pos"""

    pass

def get_opponent_move(old_board) -> tuple:
    """Takes in the old board state, compares to the new one and looks for change"""

    pass

if __name__ == '__main__':
    """This script drives the bot by getting the AI move, moving the arm, and updating the board state"""

    board = ChineseCheckers()

    winner = 0
    while winner == 0:
        # Gets AI move
        move = board.get_move(2)

        if move is not None:
            start, end = move
        else:
            print('AI forefeits')

            winner = 1
            break
        
        board[start], board[end] = board[end], board[start]

        print(board)

        # Moves the marble from start to end
        # move_arm(start, end)

        # start, end = get_opponent_move(board._marbles)
        # board[start], board[end] = board[end], board[start]

        winner = board.is_over()

    if winner == 1:
        print('Human wins!')
    else:
        print('I win!')
        

    
