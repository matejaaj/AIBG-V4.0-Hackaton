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
        self.energy = int(data['energy'])
        self.xp = int(data['xp'])
        self.coins = int(data['coins'])
        self.position = [data['position']]
        self.increased_backpack_duration = int(data['increased_backpack_duration'])
        self.daze_turns = int(data['daze_turns'])
        self.frozen_turns = int(data['frozen_turns'])
        self.backpack_capacity = int(data['backpack_capacity'])
        self.raw_minerals = int(data['raw_minerals'])
        self.processed_minerals = int(data['processed_minerals'])
        self.raw_diamonds = int(data['raw_diamonds'])
        self.processed_diamonds = int(data['processed_diamonds'])
    
    def MoveAction(self,x,y):
        return f'move {x} {y}'
    
    def MineAction(self,x,y):
        return f'mine {x} {y}'
    
    def BuildAction(self,x,y):
        return f'build {x} {y}'
    
    def RestAction():
        return 'rest'
    
    def ShopAction(self,action):
        return f'shop {action}'
    
    def AttackAction(self,x,y):
        return f'attack {x} {y}'
    
    def ConversionsAction(self,dCoins,mCoins,dEnergy,mEnergy,dXp,mXp):
        return f"conv {dCoins} diamond {mCoins} mineral to coins, {dEnergy} diamond {mEnergy} mineral to energy, {dXp} diamond {mXp} mineral to xp"
        
    def PutAction(self,X,Y,N,M):
        return f'refinement-take {X} {Y} mineral {N} diamond {M}'

    def TakeAction(self,X,Y,N,M):
        return f'refinement-take {X} {Y} mineral {N} diamond {M}'

    def GetLegalPositions(self, board):
        retVal = []
        
        return retVal

    def ConversionsSplit(self):
        total_minerals = int(self.raw_minerals)  # Pretpostavljamo da koristimo samo procesuirane minerale
        total_diamonds = int(self.raw_diamonds)  # Pretpostavljamo da koristimo samo procesuirane dijamante

        # Konverzija minerala
        if total_minerals > 1:
            m_energy = 1  # Jedan mineral za energiju
            m_xp = total_minerals - 1  # Ostatak minerala za XP
        else:
            m_energy = 0  # Nema dovoljno minerala za energiju
            m_xp = total_minerals  # Svi minerali idu na XP

        # Konverzija dijamanata
        if total_diamonds > 1:
            d_coins = 1  # Jedan dijamant za kovanice (gold)
            d_xp = total_diamonds - 1  # Ostatak dijamanata za XP
        else:
            d_coins = 0  # Nema dovoljno dijamanata za kovanice
            d_xp = total_diamonds  # Svi dijamanti idu na XP

        m_coins = 0  # Ne koristimo minerale za kovanice
        d_energy = 0  # Ne koristimo dijamante za energiju

        return self.ConversionsAction(d_coins, m_coins, d_energy, m_energy, d_xp, m_xp)
    
    

   
def main():
    while True:
        line= sys.stdin.readline().strip()
        state= GameState(line)
        player1= Player(state.player1)
        player2= Player(state.player2)
        action="rest"
        if player2.daze_turns<=1:
            action= DazeEnemyInBase(player1,player2)
        elif player1.raw_diamonds!=0 or player1.raw_minerals!=0:
            action='move [9,1]'
            action= player1.ConversionsAction()
        else:
            action= player1.RestAction()

        action="rest"

        print(action,flush=True)
     


def DazeEnemyInBase(me,enemy):
    if enemy.position==[9,9]:
        if enemy.daze_turns >1:
            if me.coins> 15:
                return "shop daze"
        else:
            return 'rest'
    else:
        return 'rest'
    


main()


