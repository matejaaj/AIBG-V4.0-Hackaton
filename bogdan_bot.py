import sys
import time
import json

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
        
        return retVal

while True:
    line = sys.stdin.readline().strip()

    gameState = GameState(line)
    

    print("rest", flush=True)

    