import random
import tkinter as tk
from enum import Enum
from colorama import Fore


class State(Enum):
    UNCOVERED = 1
    COVERED = 2
    QUESTION_MARK = 3
    BOMB_SIGN = 4


def index_validate(x, y, rows, cols):
    if x < 0 or y < 0 or x >= rows or y >= cols:
        return False
    return True


def count_adjacent_bombs(rows, cols, board):
    for row_index in range(rows):
        for col_index in range(cols):
            if board[row_index][col_index] == 'X':
                continue
            number_of_bombs = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if index_validate(row_index + i, col_index + j, rows, cols) and board[row_index + i][col_index + j] == 'X':
                        number_of_bombs = number_of_bombs + 1

            board[row_index][col_index] = str(number_of_bombs)


def generate_board(rows, cols, num_mines):
    board = []
    for one_row in range(rows):
        one_row = [' '] * cols
        board.append(one_row)

    mines_placed = 0
    while mines_placed < num_mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        if board[row][col] != 'X':
            board[row][col] = 'X'
            mines_placed += 1

    count_adjacent_bombs(rows, cols, board)
    return board


def generate_state_board(rows, cols):
    board = []
    for one_row in range(rows):
        one_row = [State.COVERED] * cols
        board.append(one_row)
    return board


def print_board(rows, cols, board):
    for row_index in range(rows):
        for col_index in range(cols):
            if board[row_index][col_index] == 'X':
                print(f"{Fore.RED}{board[row_index][col_index]}{Fore.RESET}", end='  ')
            else:
                print(f"{Fore.GREEN}{board[row_index][col_index]}{Fore.RESET}", end='  ')
        print()
    print()


def check_if_ending(rows, cols, g_board, s_board, b_board):
    safe_buttons = 0
    for i in range(rows):
        for j in range(cols):
            if s_board[i][j] == State.UNCOVERED and g_board[i][j] != 'X':
                safe_buttons = safe_buttons + 1

    if safe_buttons == 54:
        print('You win!')
        reveal_all_mines(rows, cols, g_board, b_board)
        return True
    return False


def block_all_buttons(rows, cols, g_board, s_board, b_board):
    for i in range(rows):
        for j in range(cols):
            if g_board[i][j] == 'X' and s_board[i][j] != State.BOMB_SIGN:
                b_board[i][j].config(text=g_board[i][j], background='#cfcfcf', relief='groove', state='disabled')
            elif g_board[i][j] != 'X' and s_board[i][j] == State.BOMB_SIGN:
                b_board[i][j].config(text='Z', background='#c2c2c2', relief='groove', state='disabled')
            else:
                b_board[i][j].config(state='disabled')


def reveal_all_mines(rows, cols, g_board, b_board):
    for i in range(rows):
        for j in range(cols):
            if g_board[i][j] == 'X':
                b_board[i][j].config(text='M', background='#ca94d6')


def reveal_button(row_index, col_index, g_board, s_board, b_board):
    if not index_validate(row_index, col_index, rows_number, cols_number):
        return
    if b_board[row_index][col_index]['state'] == 'normal' and s_board[row_index][col_index] == State.COVERED:
        if g_board[row_index][col_index] == 'X':
            block_all_buttons(rows_number, cols_number, g_board, s_board, b_board)
            b_board[row_index][col_index].config(background='#cf5f5f')
        elif g_board[row_index][col_index] == '0':
            b_board[row_index][col_index].config(text='', background='#eeeeee', relief='groove', state='disabled')
            s_board[row_index][col_index] = State.UNCOVERED
            for i in range(-1, 2):
                for j in range(-1, 2):
                    reveal_button(row_index + i, col_index + j, g_board, s_board, b_board)
        else:
            b_board[row_index][col_index].config(text=g_board[row_index][col_index], background='#eeeeee', relief='groove', state='disabled')
            s_board[row_index][col_index] = State.UNCOVERED
    check_if_ending(rows_number, cols_number, g_board, s_board, b_board)


def mark_button(row_index, col_index, g_board, s_board, b_board):
    if b_board[row_index][col_index]['state'] != 'disabled':
        if s_board[row_index][col_index] == State.BOMB_SIGN:
            s_board[row_index][col_index] = State.COVERED
            b_board[row_index][col_index].config(text='', background='#f0f0f0')
        else:
            s_board[row_index][col_index] = State.BOMB_SIGN
            b_board[row_index][col_index].config(text='M', background='#ca94d6')
    check_if_ending(rows_number, cols_number, g_board, s_board, b_board)


def restart_game():
    global game_board, state_board, buttons, rows_number, cols_number
    game_board = generate_board(rows_number, cols_number, number_of_mines)
    print_board(rows_number, cols_number, game_board)
    state_board = generate_state_board(rows_number, cols_number)
    for i in range(rows_number):
        for j in range(cols_number):
            buttons[i][j].config(text='', background='#f0f0f0', relief='raised', state='normal')


def game():
    root = tk.Tk()
    root.title('Minesweeper')
    root.resizable(False, False)
    global game_board, state_board, buttons, rows_number, cols_number, number_of_mines
    buttons = []
    for i in range(rows_number):
        row_of_buttons = []
        for j in range(cols_number):
            one_button = tk.Button(root, background='#f0f0f0', height=2, width=5, relief='raised')
            one_button.grid(row=i + 1, column=j, padx=1, pady=1)
            one_button.bind('<Button-1>', lambda event, param1=i, param2=j: reveal_button(param1, param2, game_board, state_board, buttons))
            one_button.bind('<Button-3>', lambda event, param1=i, param2=j: mark_button(param1, param2, game_board, state_board, buttons))
            row_of_buttons.append(one_button)
        buttons.append(row_of_buttons)

    restart_button = tk.Button(root, text='R', background='#f0f0f0', height=2, width=5, relief='raised', command=restart_game)
    restart_button.grid(row=0, column=0, pady=5, columnspan=cols_number)
    root.mainloop()


rows_number = 8
cols_number = 8
number_of_mines = 10
game_board = generate_board(rows_number, cols_number, number_of_mines)
state_board = generate_state_board(rows_number, cols_number)
print_board(rows_number, cols_number, game_board)
buttons = []

game()
