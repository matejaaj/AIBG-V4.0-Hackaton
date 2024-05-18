import sys
import time
import json
import random

class GameState:
    def __init__(self, data):
        self.turn = str(data['turn'])
        self.firstPlayerTurn = str(data['firstPlayerTurn'])
        self.player1 = Player(data['player1'])
        self.player2 = Player(data['player2'])
        self.board = [[str(cell) for cell in row] for row in data['board']]

class Player:
    def __init__(self, data):
        self.name = str(data['name'])
        self.energy = str(data['energy'])
        self.xp = str(data['xp'])
        self.coins = str(data['coins'])
        self.position = [str(pos) for pos in data['position']]
        self.increased_backpack_duration = str(data['increased_backpack_duration'])
        self.daze_turns = str(data['daze_turns'])
        self.frozen_turns = str(data['frozen_turns'])
        self.backpack_capacity = str(data['backpack_capacity'])
        self.raw_minerals = str(data['raw_minerals'])
        self.processed_minerals = str(data['processed_minerals'])
        self.raw_diamonds = str(data['raw_diamonds'])
        self.processed_diamonds = str(data['processed_diamonds'])
    

    def GetLegalPositions(self, board):
        retVal = []
        
        x = int(self.position[0])
        y = int(self.position[1])

        if y < 9:
            for i in range(y + 1, len(board[x])):
                if board[x][i] != "E":
                    break
                else:
                    retVal.append([x, i])

        if y > 0:
            for i in range(y - 1, -1, -1):
                if board[x][i] != "E":
                    break
                else:
                    retVal.append([x, i])

        if x < 9:
            for i in range(x + 1, len(board)):
                if board[i][y] != "E":
                    break
                else:
                    retVal.append([i, y])

        if x > 0:
            for i in range(x - 1, -1, -1):
                if board[i][y] != "E":
                    break
                else:
                    retVal.append([i, y])

        return retVal

while True:
    line = sys.stdin.readline().strip()
    json_data = json.loads(line)
    
    gameState = GameState(json_data)

    legal_positions = gameState.player1.GetLegalPositions(gameState.board)
    if legal_positions:
        move = random.choice(legal_positions)
        move_str = "move {} {}".format(move[0], move[1])
        print(move_str, flush=True)
    else:
        print("rest", flush=True)

    