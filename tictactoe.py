import math
from random import randint
from tkinter import ttk
from typing import List
from tkinter import *


def home():
    print(hardWin, draw, mediumWin)
    # parameters = input("Input command: ").split(" ")
    parameters = "start hard hard".split(" ")

    if parameters[0] == "exit" or mediumWin == 1:
        exit(11)

    elif len(parameters) != 3:
        print("Bad parameters!")
        home()

    elif not (("start" or "easy" or "medium" or "hard") in a for a in parameters):
        print("Bad parameters!")
        home()

    elif not (("user" or "easy" or "medium" or "hard") in b for b in parameters):
        print("Bad parameters!")
        home()

    if parameters[0] == "start":
        parameters.pop(0)
        start(parameters)


def turn(playerKind, board, player):
    global hardWin, mediumWin, draw
    if playerKind == "user":
        board = makeMove(board, player)

    elif playerKind == "easy":
        print("Making move level \"easy\"")
        board = evaluate1(board, player)

    elif playerKind == "medium":
        print("Making move level \"medium\"")
        board = evaluate2(board, player)

    elif playerKind == "hard":
        print("Making move level \"hard\"")
        board = evaluate3(board, player)

    print(show(board))
    gameStatus = status(board)

    if gameStatus is not None:
        print(gameStatus)
        if gameStatus[0] == "X": mediumWin += 1
        if gameStatus[0] == "O": hardWin += 1
        if gameStatus[0] == "D": draw += 1
        home()

    return board


def start(parameters):
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    print(show(board))

    while True:
        turn(parameters[0], board, "X")
        turn(parameters[1], board, "O")


def load():
    layout = input("Enter the cells: ").strip()
    board = [list(layout[0:3]), list(layout[3:6]), list(layout[6:9])]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "_": board[i][j] = " "

    return board


def emptySpots(board: List[List[str]]):
    moveList = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == " ":
                moveList.append((i, j))

    return moveList


def evaluate1(board: List[List[str]], player):
    moveList = emptySpots(board)
    position = moveList[int(randint(0, len(moveList) - 1))]
    board[position[0]][position[1]] = player

    return board


def adjust(number):
    if number > 0.0000000001:
        return 1

    elif number < -0.0000000001:
        return -1

    else:
        return 0


def queenLook(board, player):
    finalMove = None
    middle = board[1][1]

    for i in range(0, 180, 45):
        i = math.radians(i)

        x = adjust(math.cos(i))
        y = adjust(math.sin(i))

        front = board[1 + y][1 + x]
        back = board[1 - y][1 - x]

        move = checkMove([back, middle, front], [(1 - y, 1 - x), (1, 1), (1 + y, 1 + x)], player)

        if move is not None:
            if move[0]:
                return ["A", move[1]]
            else:
                finalMove = move[1]

    if finalMove == None:
        return None
    else:
        return ["D", finalMove]


def cornerLook(board: List[List[str]], player):
    finalMove = None
    for i in range(0, 8, 2):
        row = []
        position = []

        for j in range(0, 3):
            if i > 3:
                a = j
                b = i - 4

            else:
                a = i
                b = j

            row.append(board[a][b])
            position.append((a, b))

        move = checkMove(row, position, player)

        if move is not None:
            if move[0]:
                return ["A", move[1]]
            else:
                finalMove = move[1]

    if finalMove == None:
        return None
    else:
        return ["D", finalMove]


def checkMove(sigle: List[str], position: List[tuple], player):
    if sigle[0] == sigle[1] and sigle[2] == " " and sigle[0] != " ":
        return [sigle[0] == player, position[2]]

    elif sigle[0] == sigle[2] and sigle[1] == " " and sigle[0] != " ":
        return [sigle[0] == player, position[1]]

    elif sigle[1] == sigle[2] and sigle[0] == " " and sigle[1] != " ":
        return [sigle[1] == player, position[0]]

    else:
        return None


def evaluate2(board: List[List[str]], player) -> tuple:
    moveList = [queenLook(board, player), cornerLook(board, player)]

    final = None

    for move in moveList:
        if move is not None:
            if move[0] == "A":
                board[move[1][0]][move[1][1]] = player
                return board
            else:
                final = move[1]

    if final is not None:
        board[final[0]][final[1]] = player
        return board

    else:
        return evaluate1(board, player)


def status(board: List[List[str]]):
    global status

    for i in range(len(board)):
        text = ""
        for j in range(len(board)):
            if board[j][i] == "X":
                text += "1"
            elif board[j][i] == "O":
                text += "a"
            else:
                text += "$"

        if text.isalpha():
            return "O wins"
        elif text.isnumeric():
            return "X wins"

    for i in range(len(board)):
        if board[i].count("X") == 3:
            return "X wins"
        elif board[i].count("O") == 3:
            return "O wins"

    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[2][2] != " ":
        return board[0][0] + " wins"

    elif board[2][0] == board[1][1] and board[0][2] == board[1][1] and board[1][1] != " ":
        return board[2][0] + " wins"

    elif " " not in [j for i in board for j in i]:
        return "Draw"

    return None


def makeMove(board, player):
    global row
    global column

    while True:
        command = input("Enter the coordinates:").replace(" ", "")

        if not command.isnumeric():
            print("You should enter numbers!")
            continue

        row = int(command[0]) - 1
        column = int(command[1]) - 1

        if not (-1 < row < 3 or -1 < column < 3):
            print("Coordinates should be from 1 to 3!")
            continue

        if board[row][column] != " ":
            print("This cell is occupied! Choose another one!")
            continue

        break

    board[row][column] = player

    return board


def show(board):
    text = "---------"
    for i in range(len(board)):
        row = board[i]
        text += "\n| "
        for j in range(len(row)):
            text += row[j] + " "
        text += "|"

    text += "\n---------"

    return text


def evaluate3(board, player):
    # FIXME well it's more understanding why maximize has to equal "X"
    position = minimax(board, player, player)["position"]
    board[position[0]][position[1]] = player
    return board


def minimax(board, player, maximize) -> dict:
    # find all the empty spots on the board
    availSpots = emptySpots(board)

    winner = status(board)
    if winner is not None:
        if winner[0] == maximize:
            return {"score": 10}

        elif winner[0] == "D":
            return {"score": 0}

        elif winner[0] is not None:
            return {"score": -10}

    moveList = []
    # loop through all the empty spots to start a new game
    for i in range(len(availSpots)):
        # position of the empty spot
        row = availSpots[i][0]
        col = availSpots[i][1]

        # make a move
        board[row][col] = player

        if player == "X":
            # recursive function to find a terminal state in which someone wins
            result = minimax(board, "O", maximize)

        else:
            result = minimax(board, "X", maximize)

        move = {"position": (row, col), "score": result["score"]}
        # reset the game to its original state
        board[row][col] = " "
        moveList.append(move)

    bestMove = 0
    if player == maximize:
        bestScore = -10000
        for i in range(len(moveList)):
            move = moveList[i]
            if move["score"] > bestScore:
                bestScore = move["score"]
                bestMove = i

    else:
        bestScore = 10000
        for i in range(len(moveList)):
            move = moveList[i]
            if move["score"] < bestScore:
                bestScore = move["score"]
                bestMove = i

    return moveList[bestMove]


def run():
    # create a tkinter window
    root = Tk()

    # Open window having dimension 100x100
    root.geometry('700x700')

    # Create a Button
    btn = Button(root, text='Click me !', bd='5',
                 command=root.destroy)

    # Set the position of button on the top of window.
    btn.pack(side='top')

    root.mainloop()


run()
hardWin = 0
mediumWin = 0
draw = 0
