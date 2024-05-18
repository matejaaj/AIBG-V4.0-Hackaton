import sys
import time
import json
import random
from abc import *
from collections import deque

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
    

    def get_legal_positions(self, board):
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
                if isinstance(cell, str) and cell.startswith(target_label):
                    neighbors = [
                        (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)
                    ]
                    for ni, nj in neighbors:
                        if 0 <= ni < len(board) and 0 <= nj < len(board[0]):
                            if board[ni][nj] == 'E':
                                distance = ((self.position[0] - ni) ** 2 + (self.position[1] - nj) ** 2) ** 0.5
                                if distance < min_distance:
                                    min_distance = distance
                                    nearest_accessible_coords = [ni, nj]  # Promenjeno da vrati listu

        return nearest_accessible_coords





    def GetMiningSequence(self, gameState, objectToMine):
        target_coordinates = self.find_nearest_accessible_target(gameState.board, objectToMine)
        actions = self.get_move_sequence(gameState, target_coordinates)
        # zakucan jedan mine
        # treba mi najblizi mineral
        #actions.add(self.MineAction())
        # actions.append("rest")
        # actions.append("move ")
        return actions
    
    def get_move_sequence(self, gameState, target_coordinates):
        search = BreadthFirstSearch(gameState)
        if gameState.firstPlayerTurn:
            initial_state = RobotState(gameState, None, gameState.player1.position, target_coordinates)
        else:
            initial_state = RobotState(gameState, None, gameState.player2.position, target_coordinates)

        path, _, _ = search.search(lambda: initial_state)

        return self.create_move_command(path)

    def create_move_command(self, actions):
        commands = []
        for action in actions:  
            commands.append(f"move {action[0]} {action[1]}")

        return commands

class Search(object):

    def __init__(self, gameState):
        self.board = gameState.board
        if gameState.firstPlayerTurn:
            self.player = gameState.player1
        else:
            self.player = gameState.player2

    def search(self, initial_state):

        initial_state = initial_state()  
        states_list = deque([initial_state]) 
        states_set = {initial_state.unique_hash()}  

        processed_list = deque([])  
        processed_set = set() 

        while len(states_list) > 0: 
            curr_state = self.select_state(states_list)  
            states_set.remove(curr_state.unique_hash())  

            processed_list.append(curr_state) 
            processed_set.add(curr_state.unique_hash())  

            if curr_state.is_final_state():  
                return Search.reconstruct_path(curr_state), processed_list, states_list

            new_states = curr_state.get_next_states()
            new_states = [new_state for new_state in new_states if
                          new_state.unique_hash() not in processed_set and
                          new_state.unique_hash() not in states_set]

            states_list.extend(new_states)

            states_set.update([new_state.unique_hash() for new_state in new_states])
        return None, processed_list, states_list

    @staticmethod
    def reconstruct_path(final_state):
        path = []
        while final_state is not None:
            path.append(final_state.position)
            final_state = final_state.parent
        return list(reversed(path))

    @abstractmethod
    def select_state(self, states):
        pass

class BreadthFirstSearch(Search):
    def select_state(self, states):
        return states.popleft()     
class State(object):

    @abstractmethod
    def __init__(self, gameState, parent=None, position=None, goal_position=None):

        self.board = gameState.board 
        self.parent = parent 
        self.gameState = gameState

        if self.parent is None:
            if gameState.firstPlayerTurn:
                  self.position = gameState.player1.position
                  self.player_code = "1"
                  self.player = gameState.player1
            else:
                self.position = gameState.player2.position
                self.player_code = "2"
                self.player = gameState.player2
            self.goal_position = goal_position  
        else: 
            self.position = position
            self.goal_position = goal_position
            self.player = self.parent.player
            self.player_code = self.parent.player_code

        self.depth = parent.depth + 1 if parent is not None else 1  

    def get_next_states(self):
        new_positions = self.get_legal_positions()
        next_states = []
        for new_position in new_positions:
            next_state = self.__class__(self.gameState, self, new_position, self.goal_position)
            next_states.append(next_state)
        return next_states

    def get_agent_code(self):
        return self.player_code

    @abstractmethod
    def get_legal_positions(self):
        """
        Apstraktna metoda koja treba da vrati moguce (legalne) sledece pozicije na osnovu trenutne pozicije.
        :return: list
        """
        pass

    @abstractmethod
    def is_final_state(self):
        """
        Apstraktna metoda koja treba da vrati da li je treuntno stanje zapravo zavrsno stanje.
        :return: bool
        """
        pass

    @abstractmethod
    def unique_hash(self):
        """
        Apstraktna metoda koja treba da vrati string koji je JEDINSTVEN za ovo stanje
        (u odnosu na ostala stanja).
        :return: str
        """
        pass
    
    
    @abstractmethod
    def get_current_cost(self):
        """
        Apstraktna metoda koja treba da vrati stvarnu dosadašnju trenutnu cenu za ovo stanje, odnosno g(n)
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass
class RobotState(State):

    def __init__(self, gameState, parent=None, position=None, goal_position=None):
        super().__init__(gameState, parent, position, goal_position)
        if parent is None:
            self.cost = 0
        else: 
            self.cost = self.parent.cost + 1

    def get_legal_positions(self):
        retVal = []
        
        x = int(self.position[0])
        y = int(self.position[1])

        if y < 9:
            for i in range(y + 1, len(self.board[x])):
                if self.board[x][i] != "E":
                    break
                else:
                    retVal.append([x, i])

        if y > 0:
            for i in range(y - 1, -1, -1):
                if self.board[x][i] != "E":
                    break
                else:
                    retVal.append([x, i])

        if x < 9:
            for i in range(x + 1, len(self.board)):
                if self.board[i][y] != "E":
                    break
                else:
                    retVal.append([i, y])

        if x > 0:
            for i in range(x - 1, -1, -1):
                if self.board[i][y] != "E":
                    break
                else:
                    retVal.append([i, y])

        return retVal

    def is_final_state(self):
        return self.position == self.goal_position

    def unique_hash(self):
        return f"{self.position}{self.player.energy}"

    def manhattan_distance(self, pointA, pointB):
        return abs(pointA[0] - pointB[0]) + abs(pointA[1] - pointB[1])

    
    def get_current_cost(self):
        return self.cost




move_sequence = []

while True:
    line = sys.stdin.readline().strip()
    json_data = json.loads(line)

    gameState = GameState(json_data)

    if not move_sequence:
        move_sequence = gameState.player1.GetMiningSequence(gameState, 'M')

    
    temp = move_sequence.pop(0)
    print(temp, flush=True)
