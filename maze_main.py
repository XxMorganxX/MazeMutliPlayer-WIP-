import math, pygame, random
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


"""
NUMBER ARR KEY:
0 = empty
1 = Boarder
2 = Start
3 = Stop
4 = Solution
"""
class mazeGame(ConnectionListener):
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

        #Server Connect
        self.Connect()

    #Conversion Functions
    def indexOfBox(self, box):
        return int(box.topleft[0] // self.BOX_DIMENSION) + ((box.topleft[1] // self.BOX_DIMENSION) * (self.dimension//self.BOX_DIMENSION))

    def indexAtLocation(self, x, y):
        return int((x // self.BOX_DIMENSION) + ((y // self.BOX_DIMENSION) * (self.dimension//self.BOX_DIMENSION)))

    def locationOfIndex(self, index):
        row = (index % (self.dimension // self.BOX_DIMENSION)) * self.BOX_DIMENSION
        col = (index // (self.dimension // self.BOX_DIMENSION)) * self.BOX_DIMENSION
        return row, col

    #Game Operation Functions
    def buildBoard(self, dim): 
        numArr = []
        rectArr = []
        boxPerLen = (self.dimension//self.BOX_DIMENSION)
        for y in range(0, dim, self.BOX_DIMENSION):
            for x in range(0, dim, self.BOX_DIMENSION):
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

    def valid_solution(self, rectangleArr, numberArr):
        start = self.indexAtLocation(rectangleArr[0].topleft[0], rectangleArr[0].topleft[1])
        index = start
        end = (rectangleArr[1].topleft[0], rectangleArr[1].topleft[1])
        boxPerLen = self.dimension // self.BOX_DIMENSION

        path = []
        decisions = []

        stillRunning = True
        counter = 0
        while stillRunning and (counter < 500):
            if end in path:
                print("SOLUTION VALID")
                stillRunning = False
                break

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

    def draw_buttons(self, buttonDict):
        for rect, string in buttonDict.items():
            text = self.MAIN_FONT.render(string[1], 1, self.BLACK)
            pygame.draw.rect(self.WIN, self.BLUE, (rect[0], rect[1]), border_radius=100)
            self.WIN.blit(text, (string[0]))

    def draw_board(self, dim, submit_button, solve_button,  numberArr, rectangleArr):
        
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
        
    def validate_board(self, numberArr, rectangleArr):
        start = self.indexAtLocation(rectangleArr[0].topleft[0], rectangleArr[0].topleft[1])

        boxPerLen = self.dimension // self.BOX_DIMENSION
        boxDrawnSize = (self.BOX_DIMENSION, self.BOX_DIMENSION)

        solved = False
        firstRun = True
        closed_set = []
        curr_set = []
        temp = []
        
        turns = 0

        while (not solved):
            
            if (rectangleArr[1].topleft[0], rectangleArr[1].topleft[1]) in closed_set:
                solved = True
                print("found")
                break
            if turns >= 1000:
                print("No Solution")
                break
            temp = []
            if firstRun:
                for i in [(1), (-1), (-boxPerLen), (boxPerLen)]:
                    if numberArr[start+i] == 0:
                        currentLoc = self.locationOfIndex(start+i)
                        curr_set.append((currentLoc[0], currentLoc[1]))
                        pygame.draw.rect(self.WIN, self.BLACK, (currentLoc[0], currentLoc[1], boxDrawnSize[0], boxDrawnSize[1]))
                        temp = curr_set
                
            elif not firstRun:
                for location in curr_set:
                    index = self.indexAtLocation(location[0], location[1])
                    for delta in [(index+1),(index-1),(index+boxPerLen),(index-boxPerLen)]:
                        if((self.locationOfIndex(delta)[0], self.locationOfIndex(delta)[1]) not in closed_set) and ((self.locationOfIndex(delta)[0], self.locationOfIndex(delta)[1]) not in temp) and ((self.locationOfIndex(delta)[0], self.locationOfIndex(delta)[1]) not in curr_set) and (numberArr[delta] == 0 or numberArr[delta] == 3):
                                temp.append(self.locationOfIndex(delta))

            
            for location in temp:
                pygame.draw.rect(self.WIN, self.GREEN, (location[0], location[1], boxDrawnSize[0], boxDrawnSize[1]))



            for location in temp:
                closed_set.append(location) 
            curr_set = temp

            
            firstRun = False
            turns += 1
            

        

        print("\nDone \n")
        

    def main(self): 
        mouse_L_Down, mouse_R_Down = False, False
        num_board, rect_board, submit, solve  = self.buildBoard(self.dimension)   

        Solve_Or_Draw = 1

        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if event.button == 1: mouse_L_Down = True
                    elif event.button == 3: mouse_R_Down = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        print("Checking...")
                        self.valid_solution(rect_board, num_board) 
                elif event.type == pygame.MOUSEBUTTONUP: mouse_L_Down, mouse_R_Down = False, False
                elif event.type == pygame.QUIT: run = False

            if mouse_L_Down: # If left clicked       
                pos = pygame.mouse.get_pos()
                if pos[1] < self.dimension:
                    num_board, rect_board = self.changePoint(Solve_Or_Draw, pos, num_board, rect_board)
                elif submit.collidepoint(pos):
                    print("Submit")
                    mouse_L_Down = False
                    self.validate_board(num_board, rect_board)
                elif solve.collidepoint(pos):
                    print("Solve")
                    mouse_L_Down = False
                    match Solve_Or_Draw:
                        case 1:
                            Solve_Or_Draw = 4
                        case 4:
                            Solve_Or_Draw = 1

            elif mouse_R_Down: # If right clicked
                pos = pygame.mouse.get_pos()
                if pos[1] < self.dimension:
                    num_board, rect_board = self.changePoint(3, pos, num_board, rect_board)

            self.draw_board(self.dimension, submit, solve, num_board, rect_board) # Update Visuals

            pygame.display.update()







game = mazeGame()
if __name__ == "__main__": 
    game.main()