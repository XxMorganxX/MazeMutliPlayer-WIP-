import pygame, random, pickle
from game_Network import Network
from game_Handler import gameHandle


"""
NUMBER ARR KEY:
0 = empty
1 = Boarder
2 = Start
3 = Stop
4 = Solution
"""

class mazeGame():
    #Initialize
    def __init__(self):
        #Pygame General Setup
        pygame.init
        pygame.font.init()
        self.clock = pygame.time.Clock()

        #Pygame Window Setup
        self.dimension =  795
        self.margin = 30
        WIN_SIZE = self.dimension, self.dimension + self.margin
        self.WIN = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption("MAZE SINGLE PLAYER")

        #Fonts
        self.MAIN_FONT = pygame.font.SysFont("comicsans", 22)


        #Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.TEAL = (0,128,128)
        self.ORANGE = (255, 203, 62)
        self.BLUE = (51, 102, 255)
        self.DARKGREEN = (62, 160, 85)
        self.GREEN = (0, 124, 0)
        self.PURPLE = (128,0,128)

        #Constants
        self.FPS = 60
        self.BOX_DIMENSION = 15

    #Helping Conversion Functions
    def indexOfBox(self, box):
        return int(box.topleft[0] // self.BOX_DIMENSION) + ((box.topleft[1] // self.BOX_DIMENSION) * (self.dimension//self.BOX_DIMENSION))

    def indexAtLocation(self, x, y):
        return int((x // self.BOX_DIMENSION) + ((y // self.BOX_DIMENSION) * (self.dimension//self.BOX_DIMENSION)))

    def locationOfIndex(self, index):
        row = (index % (self.dimension // self.BOX_DIMENSION)) * self.BOX_DIMENSION
        col = (index // (self.dimension // self.BOX_DIMENSION)) * self.BOX_DIMENSION
        return row, col

    #Game Operation Functions
    def buildBoard(self, ): 
        numArr = []
        rectArr = []
        boxPerLen = (self.dimension//self.BOX_DIMENSION)
        for y in range(0, self.dimension, self.BOX_DIMENSION):
            for x in range(0, self.dimension, self.BOX_DIMENSION):
                numArr.append(0)
        

        #index1 = random.randint(0, int(len(numArr) * .25))
        index1 = 400
        index2 =  random.randint(int(len(numArr) * .75), int(len(numArr) * .99))
        
        rectArr.append(pygame.Rect(self.locationOfIndex(index1), (self.BOX_DIMENSION, self.BOX_DIMENSION)))
        rectArr.append(pygame.Rect(self.locationOfIndex(index2), (self.BOX_DIMENSION, self.BOX_DIMENSION)))
        numArr[index1] = 2
        numArr[index2] = 3

        for i in range(0, boxPerLen):
            numArr[i] = 1
            numArr[boxPerLen*i] = 1
            numArr[(boxPerLen*i)-1] = 1
            numArr[(boxPerLen**2-1) - i] = 1
            
            rect1 = pygame.Rect(self.locationOfIndex(i), (self.BOX_DIMENSION, self.BOX_DIMENSION))
            rect2 = pygame.Rect(self.locationOfIndex(boxPerLen**2-1 - i), (self.BOX_DIMENSION, self.BOX_DIMENSION))
            rect3 = pygame.Rect(self.locationOfIndex(boxPerLen*i-1), (self.BOX_DIMENSION, self.BOX_DIMENSION))
            rect4 = pygame.Rect(self.locationOfIndex(boxPerLen*i), (self.BOX_DIMENSION, self.BOX_DIMENSION))

            if rect1 not in rectArr:
                rectArr.append(rect1)
            if rect2 not in rectArr:
                rectArr.append(rect2)
            if rect3 not in rectArr:
                rectArr.append(rect3)
            if rect4 not in rectArr:
                rectArr.append(rect4)

        submit_button = pygame.Rect(((self.dimension*0.015), self.dimension + (self.margin*0.1), (self.dimension*0.15), (self.margin*0.8)))
        solve_button = pygame.Rect(((self.dimension*0.175), self.dimension + (self.margin*0.1), (self.dimension*0.15), (self.margin*0.8)))

        return numArr, rectArr, submit_button, solve_button

    def draw_buttons(self, buttonDict):
        for rect, string in buttonDict.items():
            text = self.MAIN_FONT.render(string[1], 1, self.BLACK)
            pygame.draw.rect(self.WIN, self.BLUE, (rect[0], rect[1]), border_radius=100)
            self.WIN.blit(text, (string[0]))

    def draw_board(self, dim, submit_button, solve_button,  numberArr, rectangleArr):
        self.WIN.fill(self.WHITE)
          
        #Draw Rects
        for box in rectangleArr:
            index = self.indexOfBox(box)
            if numberArr[index] == 0:
                pygame.draw.rect(self.WIN, self.WHITE, box)
            elif numberArr[index] == 1:
                pygame.draw.rect(self.WIN, self.BLACK, box)
            elif numberArr[index] == 2:
                pygame.draw.rect(self.WIN, self.ORANGE, box)
            elif numberArr[index] == 3:
                pygame.draw.rect(self.WIN, self.TEAL, box)
            elif numberArr[index] == 4:
                pygame.draw.rect(self.WIN, self.PURPLE, box)

        buttons = {
            (submit_button.topleft,  submit_button.size) : ((int(self.dimension*0.04), int(self.dimension-(self.dimension*0.0025))), "Submit"),
            (solve_button.topleft,  solve_button.size) : ((int(self.dimension*0.2125), int(self.dimension-(self.dimension*0.0025))), "Solve")
        }
        #Drawing Button
        self.draw_buttons(buttons)
        
        #Draws the lines
        for x in range(0, dim+self.BOX_DIMENSION, self.BOX_DIMENSION):
            pygame.draw.line(self.WIN, self.BLACK, (x, 0), (x, dim))
            pygame.draw.line(self.WIN, self.BLACK, (0, x), (dim, x))

    def changePoint(self, mouseNum, pos, numberArr, rectangleArr):
        x = (pos[0] // self.BOX_DIMENSION) * self.BOX_DIMENSION
        y = (pos[1] // self.BOX_DIMENSION) * self.BOX_DIMENSION
        index = self.indexAtLocation(x, y)

        boxPerLen = (self.dimension//self.BOX_DIMENSION)
        
        if mouseNum == 1 or mouseNum == 4:
            if pygame.Rect(x, y, self.BOX_DIMENSION, self.BOX_DIMENSION) not in rectangleArr:
                rectangleArr.append(pygame.Rect(x, y, self.BOX_DIMENSION, self.BOX_DIMENSION))
                numberArr[index] = mouseNum
            

        if mouseNum == 3:
            if index > boxPerLen and index < (boxPerLen**2)-boxPerLen and index % boxPerLen != 0 and index % boxPerLen != boxPerLen-1 and (numberArr[index] == 1  or numberArr[index] == 4):
                numberArr[index] = 0
                rectangleArr.remove(pygame.Rect(x,y, self.BOX_DIMENSION, self.BOX_DIMENSION))


        return numberArr, rectangleArr


    def main(self):
        net = Network() #
        playerNum = int(net.getP())  #
        print(f"You are Player {playerNum}")

        #Display Var
        _firstConn = True


        mouse_L_Down, mouse_R_Down = False, False
        num_board, rect_board, submit, solve  = self.buildBoard()   

        run = True
        while run:
            self.clock.tick(self.FPS)
            try:
                game = net.send(pickle.dumps("get"))
            except:
                run = False
                print("Couldn't get game")
                break
            
            if game.connected() and _firstConn:
                print("GAME CONNECTED!")
                _firstConn = False

            if game.bothSubmittedBoard():
                print("Double Sub")
                pygame.time.delay(200)
                try:
                    game = net.send(pickle.dumps("nextPhase"))
                except:
                    run = False
                    print("Couldn't get game")
                    break

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if event.button == 1: mouse_L_Down = True
                    elif event.button == 3: mouse_R_Down = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        print("Checking...")
                        self.valid_solution(rect_board, num_board) 
                elif event.type == pygame.MOUSEBUTTONUP: mouse_L_Down, mouse_R_Down = False, False
                elif event.type == pygame.QUIT: 
                    run = False
                    pygame.quit()

            if mouse_L_Down: # If left clicked       
                pos = pygame.mouse.get_pos()
                if pos[1] < self.dimension:
                    if game.boardPhase:
                        num_board, rect_board = self.changePoint(1, pos, num_board, rect_board)
                    elif game.solutionPhase:
                        num_board, rect_board = self.changePoint(4, pos, num_board, rect_board)
                
                elif submit.collidepoint(pos) and game.connected():
                    print(f"{playerNum}submit")
                    game = net.send(pickle.dumps(f"{playerNum}submit"))
                    mouse_L_Down = False

            elif mouse_R_Down: # If right clicked
                pos = pygame.mouse.get_pos()
                if pos[1] < self.dimension:
                    num_board, rect_board = self.changePoint(3, pos, num_board, rect_board)

            self.draw_board(self.dimension, submit, solve, num_board, rect_board) # Update Visuals

            pygame.display.update()




if __name__ == "__main__":
    gameInstance = mazeGame()
    gameInstance.main()