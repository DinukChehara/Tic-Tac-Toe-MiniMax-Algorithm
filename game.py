current_player = "X"

def display_board(board):
    print("--+---+--+--")
    print(f"| {board[0]} | {board[1]} | {board[2]} |")
    print("--+---+--+--")
    print(f"| {board[3]} | {board[4]} | {board[5]} |")
    print("--+---+--+--")
    print(f"| {board[6]} | {board[7]} | {board[8]} |")
    print("--+---+--+--")
    print("\n"*2)

def player():
    return "X" if current_player == "O" else "O"


def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in winning_combinations:
        if (board[combo[0]] == board[combo[1]] == board[combo[2]] 
            and board[combo[0]] in ['X', 'O']):
            return board[combo[0]]
    
    return None

def is_terminal_state(board):
    return check_winner(board) != None or is_board_full(board)

def is_board_full(board):
    for cell in board:
        if str(cell).isdigit():
            return False
    return True

def draw(board):
    return check_winner(board) == None and is_board_full(board)

def utility(board):
    if check_winner(board) == "X":
        return 1
    elif check_winner(board) == "O":
        return -1
    elif draw(board):
        return 0

def actions(board):
    l = []
    for cell in board:
        if cell != "X" and cell != "O":
            l.append(int(cell))
    return l

def result(board, slot, player=current_player):
    b = board.copy()
    b[slot] = player
    return b

def maxValue(board):
    if is_terminal_state(board):
        return utility(board)
    v = float('-inf')

    for action in actions(board):
        v = max(v, minValue(result(board, action-1, player="X")))
    return v


def minValue(board):
    if is_terminal_state(board):
        return utility(board)
    v = float('inf')

    for action in actions(board):
        v = min(v, maxValue(result(board, action-1, player="O")))
    return v

def getBotMove(board):
    if is_terminal_state(board):
        return None
    
    best_value = float('-inf')
    best_move = None

    for action in actions(board):
        move_value = minValue(result(board, action-1, "X"))

        if move_value > best_value:
            best_value = move_value
            best_move = action
    return best_move

def main():
    global current_player
    game_board = [_ for _ in range(1,10)]
    while not is_terminal_state(game_board):
        display_board(game_board)
        if current_player == "O":
            move = 0
            while True:
                move = input("Your turn, select a slot: ")
                if (not move.isdigit()) or (move.isdigit() and int(move) not in actions(game_board)):
                    print("Invalid move")
                    print("Valid moves: ", actions(game_board))
                    continue
                else:
                    game_board = result(game_board, int(move)-1, "O")
                    current_player = player()
                    display_board(game_board)
                    break
        else:
            print("The bot is choosing")
            game_board = result(game_board, getBotMove(game_board)-1, "X")
            current_player = player()
        pass

    print("\nGame Over!\n")
    if check_winner()!=None:
        print(f"Winner: {check_winner(game_board)} - {"player" if check_winner(game_board) == "O" else "bot"}")
    else:
        print("Draw")
        

main()