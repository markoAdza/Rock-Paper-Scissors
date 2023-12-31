class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = [False, False]
        self.id = id
        self.moves = [None, None]
        self.names = ['', '']
        self.scores = [0,0]
        self.countdown = 0


    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]
    
    def setName(self, player, name):
        self.names[player] = name

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

        if self.bothWent():
            winner = self.winner()
            if winner >= 0:
                self.scores[winner] += 1

    def playerReady(self, player):
        self.ready[player] = True
        if self.canStart():
            if player == 0:
                self.p1Went = False
            else:
                self.p2Went = False

    def canStart(self):
        return self.ready[0] and self.ready[1]
    
    def reset(self):
        self.ready[0] = False
        self.ready[1] = False
        self.p1Went = False
        self.p2Went = False

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner
        