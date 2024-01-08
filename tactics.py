from collections import Counter
import random

class Tactic:
    def __init__(self):
        self.prevMovesAI = []
        self.prevMovesPlayer = []
        self.currentTactic = None
        self.roundsRemaining = 0
        self.currentWinner = None


    def get_previous_moves(self, id):
        if id == 0:
            return self.prevMovesAI
        else:
            return self.prevMovesPlayer

    def add_AI_move(self, move):
        self.prevMovesAI.append(move)

    def add_player_move(self, move):
        self.prevMovesPlayer.append(move)

    def get_tactic_name(self):
        return self.currentTactic

    def select_tactic(self, id):
        tactics = ["Random", "Counter", "PersistSwitch", "P1history", "P1AIhistory"]
        self.currentTactic = tactics[id]
        self.roundsRemaining = 1000  # tactic for 1000 rounds

    def get_AI_move(self):
        if self.currentTactic == "Random":
            return random.choice(["R", "P", "S"])
        elif self.currentTactic == "Counter":
            if self.prevMovesPlayer:
                last_player_move = self.prevMovesPlayer[-1]
                return self.counter_move(last_player_move)
            else:
                return random.choice(["R", "P", "S"])
        elif self.currentTactic == "PersistSwitch":
            if self.prevMovesAI:
                if self.currentWinner == 0:
                    return self.prevMovesAI[-1]
                else:
                    return random.choice(["R", "P", "S"])
        elif self.currentTactic == "P1history":
            return self.p1_history_move()
        elif self.currentTactic == "P1AIhistory":
            return self.p1_ai_history_move()
        
    def p1_history_move(self):
        if self.prevMovesPlayer:
            player_moves_counter = Counter(self.prevMovesPlayer)
            most_common_move = player_moves_counter.most_common(1)[0][0]
            return self.counter_move(most_common_move)
        else:
            return random.choice(["R", "P", "S"])
        
    def p1_ai_history_move(self):
        if len(self.prevMovesPlayer) > 1 and len(self.prevMovesAI) > 0:
            combined_moves = list(zip(self.prevMovesAI, self.prevMovesPlayer[1:]))
            combined_moves_counter = Counter(combined_moves)
            
            most_common_move_pair = combined_moves_counter.most_common(1)[0][0]
            ai_most_common_move = most_common_move_pair[0]

            return self.counter_move(ai_most_common_move)
        else:
            return random.choice(["R", "P", "S"])

    def counter_move(self, move):
        counter_moves = {"R": "P", "P": "S", "S": "R"}
        return counter_moves.get(move)
    


