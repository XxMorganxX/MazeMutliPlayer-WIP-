class gameHandle:
    def __init__(self, id):
        self.p1Submit = False
        self.p2Submit = False
        self.ready = False
        self.boardPhase = True
        self.solutionPhase = False
        self.id = id
        self.boards = [None,None]
        self.solutions = [None, None]
        self.wins = [0,0]
    
    def get_player_board(self, p):
        return self.boards[p]

    def play(self, player, boards):
        self.boards[player] = [boards[0], boards[1]]
        if player == 0:
            self.p1Submit = True
        else:
            self.p2Submit = True

    def connected(self):
        return self.ready
    
    def bothSubmittedBoard(self):
        if self.p1Submit and self.p2Submit:
            self.boardPhase = False
            self.solutionPhase = True
    

    def valid_solution(self, rectangleArr, numberArr):
        start = self.indexAtLocation(rectangleArr[0].topleft[0], rectangleArr[0].topleft[1])
        index = start
        end = (rectangleArr[1].topleft[0], rectangleArr[1].topleft[1])
        boxPerLen = self.dimension // self.BOX_DIMENSION

        path = []
        decisions = []

        stillRunning = True
        counter = 0
        while stillRunning :
            if end in path:
                return True
            if (counter < 500):
                return False
            numOptions = 0
            for delta in [(index+1),(index-1),(index+boxPerLen),(index-boxPerLen)]:
                if numberArr[delta] == 4 or numberArr[delta] == 3:
                    if self.locationOfIndex(delta) not in path and self.locationOfIndex(delta) not in decisions:
                        numOptions += 1
                        d = delta
            
            
            if numOptions == 1:
                path.append(self.locationOfIndex(d))
                index = d
            if numOptions == 0:
                path = []
                index = start
            if numOptions >= 2:
                path.append(self.locationOfIndex(d))
                decisions.append(self.locationOfIndex(d))
                index = self.indexAtLocation(decisions[-1][0], decisions[-1][1])
                print(decisions)

            

            counter += 1
            print(counter)

    def nextPhase(self):
        self.boardPhase = False
        self.solutionPhase = True
        print("Solving Phase")
    
    def winner(self):
        p1 = self.boards[0]
        p2 = self.boards[1]

        winner = -1
        return winner
        #if self.valid_solution(self.boards[0][0], self.boards[0][1]):
    
    def reset(self):
        self.p1Submit = False
        self.p2Submit = False
        self.boardPhase = True
        self.solutionPhase = False
        self.boards = [None,None]
        self.solutions = [None, None]