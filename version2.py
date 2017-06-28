import random
import subprocess
import sys
import time


def clear_screen(message=''):
    subprocess.call(['tput', 'reset'])
    print_title('Battleship Version 2'.center(cols, ' '), '=')
    print(message.center(cols, ' '))


def reset_terminal(rows, cols):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))
    clear_screen()


def print_message(string):
    sys.stdout.write("\x1b7\x1b[5;0f{}\x1b8".format(string))
    sys.stdout.flush()


def game_exit():
    print('\033[1;36m')
    print_title('You exited from the game!'.center(cols, ' '), "=")
    print('\033[0m')
    exit()


def single_line(cols, decorator):
    print(decorator * cols)


def decor(func):
    def wrap(string, decorator):
        if decorator == "=":
            print('\033[1m', end='')
        print(decorator * cols)
        func(string, decorator)
        print(decorator * cols)
        if decorator == "=":
            print('\033[0m')
    return wrap


@decor
def print_title(string, decorator):
    print(string)


def create_success_message(string):
    return '\033[1;32m{}\033[0m'.format(string.center(cols, ' '))


def create_warning_message(string):
    return '\033[1;33m{}\033[0m'.format(string.center(cols, ' '))


def create_error_message(string):
    return '\033[1;31m{}\033[0m'.format(string.center(cols, ' '))


def import_ships(filename="ships.txt"):
    file = open(filename, "r")
    content = file.read()
    ships = []
    for line in content.split("\n"):
        ship = line.split("-")
        if len(ship) == 2:
            try:
                ship[1] = int(ship[1])
            except ValueError:
                continue
            if ship[1] > 7:
                continue
            ships.append(ship)
    return ships


def game_datas(settings):
    print_title('Game datas', '-')
    print('Number of players: {}'.format(settings[1]['value']))
    if settings[1]['value'] == 1:
        print('AI\'s difficulty: {}'.format(settings[2]['value']['difficulty']))
    print('Game mode: ', end='')
    if settings[3]['value'] == 1:
        print('normal')
    elif settings[3]['value'] == 2:
        print('strike')
    print('Battleground size: {} x {}'.format(settings[4]['value'][1], settings[4]['value'][0]))
    print('Number of ships: {}'.format(len(settings[5]['value'])))
    return None


def main_menu():
    print_title('Main menu'.center(cols, ' '), '-')
    print('''\t0: Exit
    \t1: Choose number of player
    \t2: Choose AI difficulty
    \t3: Choose game mode
    \t4: Choose the battleground size
    \t5: Choose ships
    \t6: Start the game''')
    single_line(cols, '-')
    try:
        action = int(input('Please choose the action: '))
    except ValueError:
        action = None
    return action


def create_action(action, settings):
    func = settings[action]['function']
    if action != 5:
        result = func()
    else:
        result = func(settings[action]['value'])
    if result is not None:
        # settings[action][settings[action]['name']] = result
        settings[action]['value'] = result
        return create_success_message(settings[action]['success'])
    else:
        return create_warning_message('You have returned to the main menu!')


def get_input_from_user(input_type, start_int=0, end_int=1):
    while True:
        get_input = input("Input: ")
        if get_input == "b":
            return None
        if input_type == 'int':
            try:
                get_input = int(get_input)
                if get_input in [x for x in range(start_int, end_int + 1)]:
                    return get_input
                else:
                    message = create_error_message(
                        'Invalid input: {}. The number should be between {} and {}!'.format(
                            get_input, start_int, end_int))
            except ValueError:
                message = create_error_message("Invalid input: {}".format(get_input))
            print_message(message)
        elif input_type == 'string':
            return get_input


def choose_player_number():
    clear_screen()
    print_title('Choose number of players'.center(cols, ' '), '-')
    return get_input_from_user('int', 1, 2)


def choose_ai_difficulty():
    return


def choose_game_mode():
    clear_screen()
    print_title('Choose game mode'.center(cols, ' '), '-')
    print('1: Normal mode\n2: Strike mode')
    single_line(cols, '-')
    return get_input_from_user('int', 1, 2)


def choose_battleground_sizes():
    clear_screen()
    print_title("Change battleground sizes".center(cols, " "), "-")
    print_title('Please give the width:', '-')
    width = get_input_from_user('int', 7, 15)
    if width is None:
        return None
    print_title('Please give the height:', '-')
    height = get_input_from_user('int', 7, 15)
    if height is None:
        return None
    return [height, width]


def add_new_ship_to_ships(ships):
    ships = ships[:]
    print_title('Please give the name of the ship:', '-')
    ship_name = get_input_from_user('string')
    print_title('Please give the size of the ship:', '-')
    ship_size = get_input_from_user('int', 2, 7)
    if ship_size:
        ships.append([ship_name, ship_size])
        return ships
    else:
        return None


def remove_ship_from_ships(ships):
    print_title('Please give the ID of the ship: ', '-')
    ship_id = get_input_from_user('int', 1, len(ships))
    if ship_id is not None:
        ship_id -= 1
        return ships[:ship_id] + ships[ship_id + 1:]
    else:
        return None


def choose_ships(ships):
    clear_screen()
    single_line(cols, '-')
    for i in range(len(ships)):
        print('{}:{}\t{}'.format((i + 1), ships[i][0], ships[i][1]))
    print_title('Choose an action', '-')
    print('1. Add ship\n2. Remove ship')
    single_line(cols, '-')
    action = get_input_from_user('int', 1, 2)
    if action is None:
        return None
    elif action == 1:
        return add_new_ship_to_ships(ships)
    elif action == 2:
        return remove_ship_from_ships(ships)


def start_game():
    pass


def create_battleground(width, height):
    battleground = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(0)
        battleground.append(line)
    return battleground


def main():
    try:
        message = ''
        global cols, rows
        rows = 60
        cols = 100
        reset_terminal(rows, cols)
        # Defining the values of the battleground
        FREE = 0
        MISSED = 1
        HIT = 2

        # Defining the basic settings
        settings = {
            1: {
                'name': 'player_number',
                'value': 1,
                'function': choose_player_number,
                'success': 'The number of players updated successfully!'
            },
            2: {
                'name': 'ai',
                'value': {
                    'difficulty': 'easy',
                    'onStrike': False,
                    'hitX': None,
                    'hitY': None,
                    'dirX': None,
                    'dirY': None
                },
                'function': choose_ai_difficulty,
            },
            3: {
                'name': 'game_mode',
                'value': 1,
                'function': choose_game_mode,
                'success': 'The game mode updated successfully!'
            },
            4: {
                'name': 'sizes',
                'value': [10, 10],
                'function': choose_battleground_sizes,
                'success': 'The battleground sizes updated successfully!'
            },
            5: {
                'name': 'ships',
                'value': import_ships(),
                'function': choose_ships,
                'success': 'The ships updated successfully!'
            }
        }
        while True:
            clear_screen(message)
            game_datas(settings)
            action = main_menu()
            message = create_warning_message("You returned back to the main menu!")
            if action == 0:
                game_exit()
            elif action in list(settings.keys()):
                message = create_action(action, settings)
            elif action == 6:
                start_game()
            else:
                message = create_error_message('The input should be a number between 1-6!')
                continue
    except KeyboardInterrupt:
        game_exit()


main()
