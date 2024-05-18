
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
        self.position = [int(pos) for pos in data['position']]
        self.increased_backpack_duration = str(data['increased_backpack_duration'])
        self.daze_turns = str(data['daze_turns'])
        self.frozen_turns = str(data['frozen_turns'])
        self.backpack_capacity = str(data['backpack_capacity'])
        self.raw_minerals = str(data['raw_minerals'])
        self.processed_minerals = str(data['processed_minerals'])
        self.raw_diamonds = str(data['raw_diamonds'])
        self.processed_diamonds = str(data['processed_diamonds'])
        self.movesSequence = []
    

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

    def find_nearest_accessible_target(self, board, target_label):
        min_distance = float('inf')
        nearest_accessible_coords = None

        for i in range(len(board)):
            for j in range(len(board[i])):
                cell = board[i][j]
                if cell.startswith(target_label):
                    neighbors = [
                        (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)
                    ]
                    for ni, nj in neighbors:
                        if 0 <= ni < len(board) and 0 <= nj < len(board[0]):
                            if board[ni][nj] == 'E':
                                distance = ((self.position[0] - ni) ** 2 + (self.position[1] - nj) ** 2) ** 0.5
                                if distance < min_distance:
                                    min_distance = distance
                                    nearest_accessible_coords = (ni, nj)

        return nearest_accessible_coords

    def GetMiningSequence(self, board, objectToMine):
        coordinates = self.find_nearest_accessible_target(board, objectToMine)
        path = self.GetPathTo(coordinates)
        actions = ["move 1 0", "move 0 0"]
        # zakucan jedan mine
        # treba mi najblizi mineral
        #actions.add(self.MineAction())
        actions.append("rest")
        actions.append("move ")
        return actions
    

    def GetDestroyFactorySequence(self, board):
        return  ["rest", "rest", "shop daze"]

    def GetPathTo(self, coordinates):
        return []

    def MineAction(self, x, y):
        return []

moves_sequence = []


file = open('test.json', 'r')
data = json.load(file)
    


gameState = GameState(data)
closest = gameState.player1.find_nearest_accessible_target(gameState.board, 'M')
print(closest)
    # #ako je prazan dodeli mu novi sequence
    # if not moves_sequence:
    #     # Prvo definišemo listu funkcija koje možemo izabrati
    #     possible_sequences = [
    #         gameState.player1.GetMiningSequence,  # funkcija bez poziva
    #         gameState.player1.GetDestroyFactorySequence  # funkcija bez poziva
    #     ]
        
    #     # Nasumično biramo jednu od funkcija
    #     moves_sequence = random.choice(possible_sequences)


    # if moves_sequence:
    #     temp = moves_sequence.pop(0)
    #     print(temp, flush=True)  # Obradite trenutni potez i štampajte ga




        
