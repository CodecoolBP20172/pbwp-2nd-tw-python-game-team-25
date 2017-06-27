import random
import subprocess
import sys
import time


def clearScreen():
    subprocess.call(['tput', 'reset'])


def resetTerminal():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=60, cols=70))
    clearScreen()


def decorMain(func):
    def wrap(string):
        print("==================================================")
        func(string)
        print("==================================================")
    return wrap


def decorSmall(func):
    def wrap(string):
        print("----------------------------------------")
        func(string)
        print("----------------------------------------")
    return wrap


def decorSingleLine(i):
    return i * '-'


@decorMain
def printMainTitle(string):
    print('\033[1m{}\033[0m'.format(string))


@decorSmall
def printSmallTitle(string):
    print(string)


def createTitle(num, phase):
    title = 'BattleShip version 2.0'
    if num == 1:
        title += ' - Single Player'
    else:
        title += ' - Multi Player'
    if onStrike:
        title += ' - Strike Mode'
    if phase:
        title += ('\n' + phase)
    return title


def createErrorMessage(string):
    return '\033[1;31m{}\033[0m'.format(string)


def createSuccessMessage(string):
    return '\033[1;32m{}\033[0m'.format(string)


# Trying to make it a single and multi player game
def createBattleGround(width, height):
    battleGround = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(0)
        battleGround.append(line)
    return battleGround


def createCoordinateByInput():
    coor = input('Coordinates(e.g. A:1): ')
    coorList = coor.split(':')
    if len(coorList) == 2:
        try:
            coorList[1] = int(coorList[1])
            if abc.find(coorList[0]) != -1:
                if coorList[1] >= 1 and coorList[1] <= 10:
                    coorList[0] = abc.find(coorList[0])
                    coorList[1] -= 1
                    return coorList
        except ValueError:
            pass
    return []


def createCoordinateByAI():
    x = random.randint(0, 9)  # A-J
    y = random.randint(0, 9)  # 1-10
    return [x, y]


# Formats the given coordinate to a human readable form
# Returns with the readable form
def formatCoordinate(coordinate):
    return '{}:{}'.format(abc[coordinate[0]], coordinate[1] + 1)


# It is used on the start of the game, in the placing phrase
# Shows the players own battleground, where (s)he placed the ships
def showOwnBattleground(battleground):
    for i in range(-1, len(battleground)):
        if i == -1:
            print('%2s' % ' ', end=' ')
            for j in range(len(abc)):
                print('\033[1m' + abc[j] + '\033[0m', end=' ')
        else:
            print('\033[1m%2d\033[0m' % (i + 1), end=' ')
            for j in range(len(battleground[i])):
                if battleground[i][j] == 0:
                    print('\033[0;36m0\033[0m', end=' ')
                elif battleground[i][j] == 1:
                    print('\033[0;30mx\033[0m', end=' ')
                elif battleground[i][j] == 2:
                    print('\033[0;31m*\033[0m', end=' ')
                elif battleground[i][j] in range(3, 3 + len(ships)):
                    print('\033[0;35m¤\033[0m', end=' ')
        print()


# It is used in the fighting phrase, where the players cannot see where are the opponent's ships.
# Only the places which haven't been fired earlier, the places of hit fire
# and missed fire are shown.
def showOppositeBattleground(p):  # p => battleground
    noShow = [i for i in range(3, 3 + len(ships))]
    noShow.append(0)
    for i in range(-1, len(p)):
        if i == -1:
            print('%2s' % ' ', end=' ')
            for j in range(len(abc)):
                print('\033[1m' + abc[j] + '\033[0m', end=' ')
        else:
            print('\033[1m%2d\033[0m' % (i + 1), end=' ')
            for j in range(len(p[i])):
                if p[i][j] in noShow:
                    print('\033[0;36m0\033[0m', end=' ')
                elif p[i][j] == 1:
                    print('\033[0;30mx\033[0m', end=' ')
                elif p[i][j] == 2:
                    print('\033[0;31m*\033[0m', end=' ')
        print()


def shipFitsInCoordinateSystem(shipIndex, battleground, coordinate, rotation):
    lastGoodIndex = len(battleground) - ships[shipIndex]['length']
    if (rotation == 'h' and coordinate[0] > lastGoodIndex) or (
            rotation == 'v' and coordinate[1] > lastGoodIndex):
        return False
    else:
        return True


def shipOverflowsAnotherShips(shipIndex, battleground, coordinate, rotation):
    x = 0
    y = 0
    length = 0
    while length < ships[shipIndex]['length']:
        # print('length: {}\ncurrent length: {}\nrotation: {}'.format(ships[shipIndex]['length'], length, rotation))
        # print('x: {}, y: {}'.format(x, y))
        # print('{} : {}'.format(coordinate[0], coordinate[1]))
        # print('{} : {}'.format(coordinate[0] + x, coordinate[1] + y))
        # if coordinate[1] > 9 or coordinate[0] > 9:
        #    return True
        # Checks the current coordinate
        if not battleground[coordinate[1] + y][coordinate[0] + x] == 0:
            return True
        # Checks the left coordinate
        if coordinate[1] > 0 and coordinate[1] - 1 + y >= 0:
            if not battleground[coordinate[1] - 1 + y][coordinate[0] + x] == 0:
                return True
        # Checks the top left corner coordinate
        if coordinate[1] > 0 and coordinate[1] - 1 + \
                y >= 0 and coordinate[0] > 0 and coordinate[0] - 1 + x >= 0:
            if not battleground[coordinate[1] -
                                1 + y][coordinate[0] - 1 + x] == 0:
                return True
        # Checks the top coordinate
        if coordinate[0] > 0 and coordinate[0] - 1 + x >= 0:
            if not battleground[coordinate[1] + y][coordinate[0] - 1 + x] == 0:
                return True
        # Checks the top right corner coordinate
        if coordinate[1] < 9 and coordinate[1] + 1 + \
                y <= 9 and coordinate[0] > 0 and coordinate[0] - 1 + x >= 0:
            if not battleground[coordinate[1] +
                                1 + y][coordinate[0] - 1 + x] == 0:
                return True
        # Checks the right coordinate
        if coordinate[1] < 9 and coordinate[1] + 1 + y <= 9:
            if not battleground[coordinate[1] + 1 + y][coordinate[0] + x] == 0:
                return True
        # Checks the bottom right corner coordinate
        if coordinate[1] < 9 and coordinate[1] + 1 + \
                y <= 9 and coordinate[0] < 9 and coordinate[0] + 1 + x <= 9:
            if not battleground[coordinate[1] +
                                1 + y][coordinate[0] + 1 + x] == 0:
                return True
        # Checks the bottom coordinate
        if coordinate[0] < 9 and coordinate[0] + 1 + x <= 9:
            if not battleground[coordinate[1] + y][coordinate[0] + 1 + x] == 0:
                return True
        # Checks the bottom left corner coordinate
        if coordinate[1] > 0 and coordinate[1] - 1 + \
                y >= 0 and coordinate[0] < 9 and coordinate[0] + 1 + x <= 9:
            if not battleground[coordinate[1] -
                                1 + y][coordinate[0] + 1 + x] == 0:
                return True
        if rotation == 'h':
            x += 1
        elif rotation == 'v':
            y += 1
        length += 1
    if length < ships[shipIndex]['length']:
        return True
    else:
        return False


def placeShipIntoBattleground(shipIndex, battleground, coordinate, rotation):
    x = 0
    y = 0
    for i in range(ships[shipIndex]['length']):
        battleground[coordinate[1] + y][coordinate[0] + x] = shipIndex + 3
        if rotation == 'h':
            x += 1
        elif rotation == 'v':
            y += 1


def placingPhase(player, battleground):
    global message
    placedShips = []
    while len(placedShips) != len(ships):
        if player != 'AI':
            clearScreen()
            printMainTitle(title)
            if message:
                print(message)
            printMainTitle('Player No. {}\'s turn!'.format(player))
            showOwnBattleground(battleground)
            printSmallTitle('Ships left:')
            for i in ships:
                if i not in placedShips:
                    print('{}: {}\t- {} wide'.format(str(i + 1),
                                                     ships[i]['name'], ships[i]['length']))
            print(decorSingleLine(50))
            try:
                shipIndex = int(
                    input('Which ship do you want to place(ID): ')) - 1
            except ValueError:
                shipIndex = -1
        else:
            shipIndex = random.randint(0, len(ships) - 1)
        if shipIndex not in placedShips and shipIndex >= 0 and shipIndex <= 4:
            if player == 'AI':
                coordinate = createCoordinateByAI()
            else:
                print(decorSingleLine(50))
                print(ships[shipIndex]['name'] + ' starting coordinates:')
                coordinate = createCoordinateByInput()
            # print(coordinate)
            # input()
            if len(coordinate) == 2:
                if player == 'AI':
                    rotation = ['h', 'v'][random.randint(0, 1)]
                else:
                    print(decorSingleLine(50))
                    rotation = input('Rotation: h(orizontal) or v(ertical): ')
                if rotation in ['h', 'v']:
                    if shipFitsInCoordinateSystem(
                            shipIndex, battleground, coordinate, rotation):
                        if not shipOverflowsAnotherShips(
                                shipIndex, battleground, coordinate, rotation):
                            placeShipIntoBattleground(
                                shipIndex, battleground, coordinate, rotation)
                            if player != 'AI':
                                message = createSuccessMessage(
                                    'The {} ship has been placed into the battleground!'.format(
                                        ships[shipIndex]['name']))
                            placedShips.append(shipIndex)
                        elif player != 'AI':
                            message = createErrorMessage(
                                'There is an overflow!')
                    elif player != 'AI':
                        message = createErrorMessage(
                            'The ship does not fit in!')
                elif player != 'AI':
                    message = createErrorMessage('Invalid rotation!')
            elif player != 'AI':
                message = createErrorMessage('Invalid coordinate!')
        elif player != 'AI':
            message = createErrorMessage('Invalid ID.')


def fightingPhase(player, battlegroundCurrent, battlegroundBefore):
    global message
    while True:
        clearScreen()
        printMainTitle(title)
        if message:
            print(message)
        if player != 'AI':
            if playersNumber == 2:
                printSmallTitle(
                    'Player No. {}\'s last turn!'.format(
                        player %
                        2 + 1))
            else:
                printSmallTitle('AI\'s last turn!')
            # showOwnBattleground(battlegroundCurrent)
            showOppositeBattleground(battlegroundBefore)
            if playersNumber == 2:
                printSmallTitle('Player No. {}\'s turn!'.format(player))
            else:
                printSmallTitle('Player No. {}\'s turn!'.format(playersNumber))
            # showOwnBattleground(battlegroundBefore)
            showOppositeBattleground(battlegroundCurrent)
        if player == 'AI':
            coordinate = createCoordinateByAI()
        else:
            print(decorSingleLine(50))
            coordinate = createCoordinateByInput()
        if len(coordinate) == 2:
            available = [i for i in range(3, 3 + len(ships))]
            available.append(0)
            if battlegroundCurrent[coordinate[1]][coordinate[0]] in available:
                if player == 'AI':
                    printSmallTitle('Waiting for AI to shot...')
                    time.sleep(3)
                if battlegroundCurrent[coordinate[1]][coordinate[0]] in range(
                        3, 3 + len(ships)):
                    shipIndex = battlegroundCurrent[coordinate[1]
                                                    ][coordinate[0]] - 3
                    if player == 'AI' or player == 2:
                        playerHaveShot = 2
                    elif player == 1:
                        playerHaveShot = 1
                    shipsHP[shipIndex][playerHaveShot - 1] -= 1
                    battlegroundCurrent[coordinate[1]][coordinate[0]] = 2
                    message = createSuccessMessage(
                        'The fire hit a ship on {} coordinate!'.format(
                            formatCoordinate(coordinate)))
                    if shipsHP[shipIndex][playerHaveShot - 1] == 0:
                        message += createSuccessMessage(
                            '\nThe {} ship sank.'.format(
                                ships[shipIndex]['name']))
                        shipsLeft[playerHaveShot - 1] -= 1
                        message += createSuccessMessage(
                            '\nThere are {} ship(s) remaining!'.format(shipsLeft[playerHaveShot - 1]))
                        # Check if the opposite player has more ships left
                        if shipsLeft[playerHaveShot - 1] == 0:
                            # print('Player One Wins!!')
                            return 0
                    return 1
                else:
                    battlegroundCurrent[coordinate[1]][coordinate[0]] = 1
                    message = createErrorMessage(
                        'The fire missed on {} coordinate!'.format(
                            formatCoordinate(coordinate)))
                    return 2
            elif player != 'AI':
                message = createErrorMessage(
                    'This place has been already shot!')
        elif player != 'AI':
            message = createErrorMessage('Invalid coordinate!')


abc = 'ABCDEFGHIJ'
ships = {
    0: {
        'name': 'Carrier',
        'length': 5
    },
    1: {
        'name': 'Battleship',
        'length': 4
    },
    2: {
        'name': 'Cruiser',
        'length': 3
    },
    3: {
        'name': 'Submarine',
        'length': 3
    },
    4: {
        'name': 'Destroyer',
        'length': 2
    }
}


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
try:
    resetTerminal()
    title = 'BattleShip version 2.0'
    playersNumber = 0
    playerOnTurn = 1

    battleGroundPlayer1 = createBattleGround(10, 10)
    battleGroundPlayer2 = createBattleGround(10, 10)

    shipsHP = []
    for i in range(len(ships)):
        shipsHP.append([ships[i]['length'], ships[i]['length']])
    shipsLeft = [len(ships), len(ships)]

    AIonStrike = [False, 0, 0]

    onStrike = False
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'strike':
            onStrike = True

    message = ''

    while True:
        clearScreen()
        printMainTitle(title)
        if message:
            print(message)
        try:
            playersNumber = int(input('Player\'s number(1/2): '))
            if playersNumber in [1, 2]:
                break
        except ValueError:
            pass
        message = createErrorMessage('Player\'s number can only be 1 or 2!')

    title = createTitle(playersNumber, 'Placing Phase')

    placingPhase(playerOnTurn, battleGroundPlayer1)
    message = ''
    if playersNumber == 1:
        placingPhase('AI', battleGroundPlayer2)
    elif playersNumber == 2:
        playerOnTurn = 2
        placingPhase(playerOnTurn, battleGroundPlayer2)

    message = ''
    playerOnTurn = 1

    clearScreen()
    title = createTitle(playersNumber, 'Fighting Phase')

    print('AI\'s battleground')
    decorSingleLine(40)
    showOwnBattleground(battleGroundPlayer2)
    time.sleep(5)

    while True:
        if playerOnTurn == 1:
            result = fightingPhase(
                playerOnTurn,
                battleGroundPlayer2,
                battleGroundPlayer1)
            if result == 2 or (result == 1 and not onStrike):
                if playersNumber == 1:
                    playerOnTurn = 'AI'
                else:
                    playerOnTurn = 2
            elif result == 1 and onStrike:
                continue
            elif result == 0:
                break
        elif playerOnTurn == 2 or playerOnTurn == 'AI':
            result = fightingPhase(
                playerOnTurn,
                battleGroundPlayer1,
                battleGroundPlayer2)
            if result == 2 or (result == 1 and not onStrike):
                playerOnTurn = 1
            elif result == 1 and onStrike:
                continue
            elif result == 0:
                break

    clearScreen()
    title = createTitle(playersNumber, 'END')
    printMainTitle(title)
    if playerOnTurn == 'AI':
        printMainTitle('AI wins!!')
    else:
        printMainTitle('Player No. {} wins!!'.format(playerOnTurn))
    if playersNumber == 2:
        player = 'Player 2'
    else:
        player = 'AI'
    if playerOnTurn == 1:
        print(createSuccessMessage('Player 1'))
        showOwnBattleground(battleGroundPlayer1)
        print(createErrorMessage(player))
        showOwnBattleground(battleGroundPlayer2)
    elif playerOnTurn == 2 or playerOnTurn == 'AI':
        print(createSuccessMessage(player))
        showOwnBattleground(battleGroundPlayer2)
        print(createErrorMessage('Player 1'))
        showOwnBattleground(battleGroundPlayer1)
except KeyboardInterrupt:
    print('\n\033[1;31mThe game has ended. Hope you had a wonderful time playing it.\033[0m')
