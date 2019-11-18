'''
Code by: Amir Kedem
Date: 22/ 12/ 2018

This code is a Tic Tac Toe game in which you play against
the computer, At first you start and then the computer starts and so on.
The computer on each turn gets the board and its current turn and by using
the min-max algorithm it decides where to place the 'X' or 'O'.

More over on the min-max algorithm and its use:
Min-Max algorithm Wikipedia: https://en.wikipedia.org/wiki/Minimax

The main goal of this algorithm is to get each turn (function call)
the best move for both sides - if it's my turn then maximize and if it's the
human turn then minimize. By going on this route you achieve the best next move
because you always check the best route for both sides.
'''


import random


def get_input():
    flag = True
    while flag:
        try:
            s = raw_input('Please enter your desired square: ').strip()

            if s == 'exit':
                quit()

            s = int(s) - 1
            if not (8 >= s >= 0):
                print('Input must be between 1 - 9 try once more')
                continue
        # in case of a bad cast
        except ValueError:
            print('Input must be a number between 1 - 9 try again')
            continue
        flag = False
    return s / 3, s % 3


def usr_place_xo():
    row, col = get_input()
    while board[row][col] != '-':
        print('Oops already taken try once more')
        row, col = get_input()

    board[row][col] = curr_turn


def bot_place_xo():
    # With a global board the computer using the min max algorithm
    empty_indexes = [[i, j] for i in range(3) for j in range(3) if board[i][j] == '-']

    # The first turn
    if len(empty_indexes) == 9:
        # This will make the odds of winning a lot bigger
        # yet we don't want to let our user understand the best strategy
        corners = [0, 2, 6, 8]
        s = random.choice(corners)
        # Therefore we go full random
        # all_indexes = [[i, j] for i in range(3) for j in range(3)]
        # s = random.choice(all_indexes)
        board[s / 3][s % 3] = curr_turn
    else:
        best_move_index = get_best_move(empty_indexes, curr_turn)
        board[best_move_index[0]][best_move_index[1]] = curr_turn


def get_best_move(empty_indexes, _c_t):
    choices = []

    for index in empty_indexes:
        temp_b = [x[:] for x in board]
        temp_b[index[0]][index[1]] = curr_turn
        choices.append(min_max_rec(temp_b, 'O' if curr_turn == 'X' else 'X', curr_turn))

    choices = [i for i in range(len(choices)) if choices[i] == max(choices)]
    best_move_index = empty_indexes[random.choice(choices)]

    return best_move_index


def min_max_rec(_board, past_turn, original_turn):
    # Keep on with the recursive calls as long as the game hasn't gotten into a
    # terminal state (win, lose, tie).

    empty_indexes = [[i, j] for i in range(3) for j in range(3) if _board[i][j] == '-']
    is_winner = check_winner(_board)

    # if there is no empty squares then it's length will be 0
    if not is_winner and len(empty_indexes) > 0:
        # As long as there is no victory and there is still free squares.
        # Flip the turn if its x's turn make it o's turn and vice versa.
        curr_turn = 'O' if past_turn == 'X' else 'X'

        # Give each empty spot a score
        score_board = []
        for index in empty_indexes:
            # Call the min max rec function on the new board.
            new_temp_board = [x[:] for x in _board]
            new_temp_board[index[0]][index[1]] = past_turn
            score_board.append(min_max_rec(new_temp_board, curr_turn, original_turn))

        # Max or Min is determined by if this current score
        # If the last turn was the same as the original computer's turn
        # Then it wants to win so it'll take the max score
        # If the last turn was not the same as the original computer's turn
        # Then the human will want us to lose so it'll take the min score

        # by doing so we achieve the route that is the best for both sides
        # because we make the best move on every recursive call.
        if past_turn == original_turn:
            return max(score_board)
        else:
            return min(score_board)
    else:
        # The game ended and we should return a score
        if is_winner:
            if original_turn == past_turn:
                # means that the last turn was mine and i lose
                score = -1
            else:
                # means that this turn was mine and i win
                score = 1
        else:
            # Tie
            score = 0
    return score


def print_board(_b):
    # With a given 2d list _b
    # Print it with formatting
    print('-------------')
    for i in range(len(_b)):
        print('|' + str(_b[i])[1:-1].replace('\'', ' ').replace(', ', '|').replace('-', ' ') + '|')
        print('-------------')
    

def check_winner(_b):
    # with a given board _b return true or false if there is a win
    # if there is the last one who played
    for win_combination in check_list:
        # tuple of indexes
        x, y, z = win_combination
        if (_b[x/3][x % 3] == _b[y/3][y % 3] and
            _b[z/3][z % 3] == _b[y/3][y % 3] and
            _b[y/3][y % 3] != '-'):
            return True
    return False


# Variables
# Who will start
last_player_2_start = True
turn_counter = 9
curr_turn = 'X'
is_winner = False
# A Tuple that holds all the winning combinations.
check_list = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
# 'x', 'o' and '-' for empty
board = []

# The Game Logic
while True:
    print("X Mix Drix")
    # Rules:
    print('in any time to exit the game type exit')
    print('The squares are: ')

    print_board([[str(i), str(i+1), str(i+2)] for i in range(1, 9, 3)])
    # Since The board has changed in the last game.
    board = [['-', '-', '-'] for _ in range(3)]

    # The Game Loop
    while not is_winner:
        print
        print_board(board)

        # Alternating Turns the first time the human starts and then the computer
        # and so on and so forth.
        # last_player_2_start has to True in the start in order to the human to start first
        if last_player_2_start:
            if curr_turn == 'X':
                # Gets Input, if input is Space then quit
                # Places a square, if square is already taken then it'll try again
                print('Your turn, ' + curr_turn + '\'s move')
                usr_place_xo()
            else:
                print('The Computer\'s turn, ' + curr_turn + '\'s move')
                bot_place_xo()
                # usr_place_xo()
        else:
            if curr_turn == 'O':
                # Gets Input, if input is Space then quit
                # Places a square, if square is already taken then it'll try again
                print('Your turn, ' + curr_turn + '\'s move')
                usr_place_xo()
            else:
                print('The Computer\'s turn, ' + curr_turn + '\'s move')
                bot_place_xo()
                # usr_place_xo()

        is_winner = check_winner(board)
        if not is_winner and turn_counter > 1:
            # Flip the turn if its x's turn make it o's turn and vice versa.
            curr_turn = 'O' if curr_turn == 'X' else 'X'
            turn_counter -= 1
        else:
            if is_winner:
                print('\nThe Winner Is ' + curr_turn + '\n')
            else:
                is_winner = True
                print('\nTie\n')
            print_board(board)

    else:
        # Reset
        print('\nnew game maybe this time you won\'t lose nah you can only tie\n\
who am I kidding you\'ll lose again\n\
good luck and please have fun and don\'t get mad\n')
        last_player_2_start = not last_player_2_start
        curr_turn = 'X'
        turn_counter = 9
        is_winner = False

