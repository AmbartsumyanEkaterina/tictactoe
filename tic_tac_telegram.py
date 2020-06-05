from math import inf as infinity
from random import choice
from telebot import types
import telebot

bot = telebot.TeleBot('1101157557:AAEbuY7qdr9xHROQOEuAC5hZ3UyWWuz1S7U')

h_move = -1
HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def render(message, state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: '   '
    }
    str_line = '------------------'

    msg = '\n' + str_line + '\n'
    for row in state:
        for cell in row:
            symbol = chars[cell]
            msg += f'| {symbol} |'
        msg += '\n' + str_line + '\n'

    bot.send_message(message.chat.id, msg)


def ai_turn(message, c_choice, h_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    global h_move
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    while h_move == -1:  # ждём хода пользователя
        pass

    render(message, board, c_choice, h_choice)
    bot.send_message(message.chat.id, f'Computer turn [{c_choice}]')

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    h_move = -1


def human_turn(message, c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    render(message, board, c_choice, h_choice)
    bot.send_message(message.chat.id, f'Human turn [{h_choice}]')

    bot.send_message(message.from_user.id, "Use numpad (1..9): ")


@bot.message_handler(func=lambda message: message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
def m_handler_digits(message):
    global h_move
    chat_id = message.chat.id

    # Dictionary of valid moves
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    h_move = int(message.text)
    coord = moves[h_move]
    can_move = set_move(coord[0], coord[1], HUMAN)
    bot.send_message(chat_id, 'Your move: ' + message.text)

    if not can_move:
        bot.send_message(chat_id, 'Bad move: ' + message.text)
        h_move = -1
        # bot.send_message(chat_id, 'Bad move: ' + message.text + '. Repeat your turn')
        # human_turn(message, c_choice, h_choice)  # не работает
        # bot.register_next_step_handler(message, human_turn, c_choice, h_choice)  # не работает


@bot.message_handler(func=lambda message: message.text in ['✅', '❎'])
def m_handler_first(message):
    global first, h_move
    if message.text == '✅':
        first = 'YES'
    elif message.text == '❎':
        first = 'NO'
        h_move = -2  # указатель на то, что пользователь ещё не сходил, но при этом уступает ход AI
    bot.send_message(message.chat.id, 'Chosen: ' + message.text)
    start_game(message, first)


def who_first(message):
    btn_y = types.KeyboardButton('✅')
    btn_n = types.KeyboardButton('❎')
    markup = types.ReplyKeyboardMarkup()
    markup.add(btn_y, btn_n)
    bot.send_message(message.from_user.id, "First to start?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['❌', '⭕'])
def m_handler(message):
    global h_choice, c_choice
    if message.text == '❌':
        h_choice = '❌'
        c_choice = '⭕'
    elif message.text == '⭕':
        h_choice = '⭕'
        c_choice = '❌'
    bot.send_message(message.chat.id, 'Chosen: ' + message.text)
    who_first(message)


def start_game(message, first):
    # Main loop of this game
    global c_choice, h_choice
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'NO':
            ai_turn(message, c_choice, h_choice)
            first = ''

        human_turn(message, c_choice, h_choice)
        ai_turn(message, c_choice, h_choice)

    # Game over message
    chat_id = message.chat.id
    if wins(board, HUMAN):
        render(message, board, c_choice, h_choice)
        bot.send_message(chat_id, 'YOU WIN!')
    elif wins(board, COMP):
        render(message, board, c_choice, h_choice)
        bot.send_message(chat_id, 'YOU LOSE!')
    else:
        render(message, board, c_choice, h_choice)
        bot.send_message(chat_id, 'DRAW!')


@bot.message_handler(commands=['start'])  # бот запускается по команде /start]
def start(message):
    # Human chooses X or O to play
    btn_x = types.KeyboardButton('❌')
    btn_o = types.KeyboardButton('⭕')
    markup = types.ReplyKeyboardMarkup()
    markup.add(btn_x, btn_o)
    bot.send_message(message.from_user.id, "Welcome to the TicTacToe")
    bot.send_message(message.from_user.id, "Choose ❌ or ⭕", reply_markup=markup)


bot.polling(none_stop=True, interval=0)
