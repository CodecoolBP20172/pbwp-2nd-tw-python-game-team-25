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
    height = get_input_from_user('int', 7, 11)
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


def get_coordinate_from_user(sizes, coordinate):
    abc = 'ABCDEFGHIJKLOMN'
    get_input = input('Coordinate: ')
    get_input = get_input.split(':')
    if len(get_input) == 2:
        if get_input[0] in abc[:sizes[1]]:
            try:
                get_input[1] = int(get_input[1])
                if get_input[1] <= sizes[0] and get_input[1] >= 0:
                    get_input[0] = abc.find(get_input[0])
                    get_input[1] -= 1
                    coordinate.append(get_input[0])
                    coordinate.append(get_input[1])
                    return None
            except ValueError:
                pass
    return create_error_message('Invalid coordinate!')


def create_battleground(sizes):
    battleground = []
    for y in range(sizes[0]):
        line = []
        for x in range(sizes[1]):
            line.append(0)
        battleground.append(line)
    return battleground


def show_battleground(battleground, settings, PLACE_CONSTANTS, own=True):
    cell_height = 3
    cell_width = 5
    ships = settings[5]['value']
    abc = 'ABCDEFGHIJKLOMN'
    single_line(cols, '-')
    for i in range(-cell_height, len(battleground) * cell_height):
        y = i // cell_height
        center_y = (i % cell_height == cell_height // 2)
        for j in range(-cell_width, len(battleground[1]) * cell_width):
            x = j // cell_width
            center_x = (j % cell_width == cell_width // 2)
            if y >= 0:
                if x >= 0:
                    if battleground[y][x] in [x + PLACE_CONSTANTS['SHIP_START'] for x in range(len(ships))] and own:
                        bgcolor = 45
                    elif battleground[y][x] == PLACE_CONSTANTS['HIT']:
                        bgcolor = 41
                    elif battleground[y][x] == PLACE_CONSTANTS['MISSED'] and center_x and center_y:
                        bgcolor = 47
                    elif ((y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1)):
                        bgcolor = 46
                    else:
                        bgcolor = 44
                    print('\033[0;37;{}m \033[0m'.format(bgcolor), end='')
                elif center_y and center_x:
                    print('%{}s'.format(cell_width) % str((y + 1)).center(cell_width, ' '), end='')
                elif not center_y:
                    print(' ', end='')
            elif center_y and center_x and x != -1:
                print(abc[x], end='')
            else:
                print(' ', end='')
        print()


def ship_can_be_placed(PLACE_CONSTANTS, ships, sizes, ship_index, battleground, coordinate, rotation):
    x = 0
    y = 0
    length = 0
    # print(coordinate)
    # print(sizes)
    # input()
    # print(ships)
    # print([i + PLACE_CONSTANTS['SHIP_START'] for i in range(len(ships))])
    # input()
    while length < ships[ship_index][1]:
        current_x = coordinate[0] + x
        current_y = coordinate[1] + y
        if current_x > (sizes[1] - 1) or current_y > (sizes[0] - 1):
            return False
        current_value = battleground[current_y][current_x]
        # Left
        if current_x - 1 >= 0:
            if battleground[current_y][current_x - 1] != 0:
                return False
        # Top left
        if current_x - 1 >= 0 and current_y - 1 >= 0:
            if battleground[current_y - 1][current_x - 1] != 0:
                return False
        # Top
        if current_y - 1 >= 0:
            if battleground[current_y - 1][current_x] != 0:
                return False
        # Top right
        if current_x + 1 <= sizes[1] - 1 and current_y - 1 >= 0:
            if battleground[current_y - 1][current_x + 1] != 0:
                return False
        # Right
        if current_x + 1 <= sizes[1] - 1:
            if battleground[current_y][current_x + 1] != 0:
                return False
        # Bottom right
        if current_x + 1 <= sizes[1] - 1 and current_y + 1 <= sizes[0] - 1:
            if battleground[current_y + 1][current_x + 1] != 0:
                return False
        # Bottom
        if current_y + 1 <= sizes[0] - 1:
            if battleground[current_y + 1][current_x] != 0:
                return False
        # Bottom left
        if current_x - 1 >= 0 and current_y + 1 <= sizes[0] - 1:
            if battleground[current_y + 1][current_x - 1] != 0:
                return False
        if current_value in [i + PLACE_CONSTANTS['SHIP_START'] for i in range(len(ships))] or current_value != 0:
            return False
        if rotation == 'h':
            x += 1
        elif rotation == 'v':
            y += 1
        length += 1
    return True


def place_ship_into_battleground(PLACE_CONSTANTS, ships, ship_index, battleground, coordinate, rotation):
    x = 0
    y = 0
    for i in range(ships[ship_index][1]):
        battleground[coordinate[1] + y][coordinate[0] + x] = ship_index + PLACE_CONSTANTS['SHIP_START']
        if rotation == 'h':
            x += 1
        elif rotation == 'v':
            y += 1


def placing_phase(settings, PLACE_CONSTANTS, battleground):
    sizes = settings[4]['value']
    ships = settings[5]['value']
    message = ''
    ships_placed = []
    while len(ships_placed) < len(ships):
        # Print out the battleground
        # Print out the remaining ships
        clear_screen(message)
        print_title('Player No. {}'.format(1), '=')
        show_battleground(battleground, settings, PLACE_CONSTANTS)
        print_title('Ships left to place:', '-')
        for index in range(len(ships)):
            if index not in ships_placed:
                print('{}:{}\t- {} wide'.format((index + 1), ships[index][0], ships[index][1]))
        single_line(cols, '-')
        try:
            ship_index = int(input('Please give the index of a ship: ')) - 1
        except ValueError:
            ship_index = -1
        if ship_index in ships_placed or ship_index < 0 or ship_index > len(ships):
            message = create_error_message('The ship index should be one from the list below!').format(len(ships))
            continue
        single_line(cols, '-')
        coordinate = []
        message = get_coordinate_from_user(sizes, coordinate)
        if message:
            continue
        single_line(cols, '-')
        rotation = input('Rotation: h(orizontal) or v(ertical): ')
        if rotation not in ['h', 'v']:
            message = create_error_message('Invalid rotation! It should be \'h\' or \'v\'!').format(len(ships))
            continue
        if not ship_can_be_placed(PLACE_CONSTANTS, ships, sizes, ship_index, battleground, coordinate, rotation):
            message = create_error_message('The ship doesn\'t fit in, or there is an overflow!')
            continue
        place_ship_into_battleground(PLACE_CONSTANTS, ships, ship_index, battleground, coordinate, rotation)
        ships_placed.append(ship_index)
        message = create_success_message('The {} has been placed into the battleground!'.format(ships[ship_index][0]))


def start_game(settings, PLACE_CONSTANTS):
    # Placing phase started
    # Show the battleground and the ships
    # Place the ships: ID, coordinate, rotation
    # Check if the ship can place
    # Place
    player1 = create_battleground(settings[4]['value'])
    player2 = create_battleground(settings[4]['value'])
    placing_phase(settings, PLACE_CONSTANTS, player1)
    show_battleground(player1, settings, PLACE_CONSTANTS)
    input()


def main():
    try:
        message = ''
        global cols, rows
        rows = 60
        cols = 100
        reset_terminal(rows, cols)
        # Defining the values of the battleground
        PLACE_CONSTANTS = {
            'FREE': 0,
            'MISSED': 1,
            'HIT': 2,
            'SHIP_START': 3
        }

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
                start_game(settings, PLACE_CONSTANTS)
            else:
                message = create_error_message('The input should be a number between 1-6!')
                continue
    except KeyboardInterrupt:
        game_exit()


main()
