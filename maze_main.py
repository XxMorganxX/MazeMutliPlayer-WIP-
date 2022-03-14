import math
import pygame, random


"""
NUMBER ARR KEY:
0 = empty
1 = Boarder
2 = Start
3 = Stop
4 = Solution
"""

#Pygame General Setup
pygame.init
pygame.font.init()
clock = pygame.time.Clock()

#Pygame Window Setup
dimension =  795
margin = 30
WIN_SIZE = dimension, dimension + margin
WIN = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("MAZE SINGLE PLAYER")

#Fonts
MAIN_FONT = pygame.font.SysFont("comicsans", 22)


#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0,128,128)
ORANGE = (255, 203, 62)
BLUE = (51, 102, 255)
DARKGREEN = (62, 160, 85)
GREEN = (0, 124, 0)
PURPLE = (128,0,128)

#Constants
FPS = 60
box_dimension = 15

#Getting Functions
def indexOfBox(box):
    return int(box.topleft[0] // box_dimension) + ((box.topleft[1] // box_dimension) * (dimension//box_dimension))

def indexAtLocation(x, y):
    return int((x // box_dimension) + ((y // box_dimension) * (dimension//box_dimension)))

def locationOfIndex(index):
    row = (index % (dimension // box_dimension)) * box_dimension
    col = (index // (dimension // box_dimension)) * box_dimension
    return row, col


#Operating Functions
def buildBoard(dim): 
    numArr = []
    rectArr = []
    boxPerLen = (dimension//box_dimension)
    for y in range(0, dim, box_dimension):
        for x in range(0, dim, box_dimension):
            numArr.append(0)
    

    #index1 = random.randint(0, int(len(numArr) * .25))
    index1 = 400
    index2 =  random.randint(int(len(numArr) * .75), int(len(numArr) * .99))
    
    rectArr.append(pygame.Rect(locationOfIndex(index1), (box_dimension, box_dimension)))
    rectArr.append(pygame.Rect(locationOfIndex(index2), (box_dimension, box_dimension)))
    numArr[index1] = 2
    numArr[index2] = 3

    for i in range(0, boxPerLen):
        numArr[i] = 1
        numArr[boxPerLen*i] = 1
        numArr[(boxPerLen*i)-1] = 1
        numArr[(boxPerLen**2-1) - i] = 1
        
        rect1 = pygame.Rect(locationOfIndex(i), (box_dimension, box_dimension))
        rect2 = pygame.Rect(locationOfIndex(boxPerLen**2-1 - i), (box_dimension, box_dimension))
        rect3 = pygame.Rect(locationOfIndex(boxPerLen*i-1), (box_dimension, box_dimension))
        rect4 = pygame.Rect(locationOfIndex(boxPerLen*i), (box_dimension, box_dimension))

        if rect1 not in rectArr:
            rectArr.append(rect1)
        if rect2 not in rectArr:
            rectArr.append(rect2)
        if rect3 not in rectArr:
            rectArr.append(rect3)
        if rect4 not in rectArr:
            rectArr.append(rect4)

    submit_button = pygame.Rect(((dimension*0.015), dimension + (margin*0.1), (dimension*0.15), (margin*0.8)))
    solve_button = pygame.Rect(((dimension*0.175), dimension + (margin*0.1), (dimension*0.15), (margin*0.8)))

    return numArr, rectArr, submit_button, solve_button

def valid_solution(rectangleArr, numberArr):
    index = indexAtLocation(rectangleArr[0].topleft[0], rectangleArr[0].topleft[1])
    end = (rectangleArr[1].topleft[0], rectangleArr[1].topleft[1])
    boxPerLen = dimension // box_dimension

    path = []
    temp = []

    #path.append(locationOfIndex(delta))

    stillRunning = True
    counter = 0
    while stillRunning and (counter < 1000):
        if end in path:
            print("SOLUTION VALID")
            stillRunning = False
            break

        for delta in [(index+1),(index-1),(index+boxPerLen),(index-boxPerLen)]:
            if numberArr[delta] == 4 or numberArr[delta] == 3:
                if locationOfIndex(delta) not in path:
                    path.append(locationOfIndex(delta))
        
        """
        dist = 10000
        min_location = None
        for location in temp:
            temp_dist = math.hypot(location[0]-end[0], location[1]-end[1]) 
            if temp_dist < dist:
                dist = temp_dist
                min_location = location
        print(f"next box {min_location}")
        """

        #if min_location != None:
        #    index = indexAtLocation(min_location[0], min_location[1])
        #    path.append(min_location)

        counter += 1
        print(counter)


def draw_buttons(buttonDict):
    for rect, string in buttonDict.items():
        text = MAIN_FONT.render(string[1], 1, BLACK)
        pygame.draw.rect(WIN, BLUE, (rect[0], rect[1]), border_radius=100)
        WIN.blit(text, (string[0]))

def draw_board(dim, submit_button, solve_button,  numberArr, rectangleArr):
    
    #Draw Rects
    for box in rectangleArr:
        index = indexOfBox(box)
        if numberArr[index] == 0:
            pygame.draw.rect(WIN, WHITE, box)
        elif numberArr[index] == 1:
            pygame.draw.rect(WIN, BLACK, box)
        elif numberArr[index] == 2:
            pygame.draw.rect(WIN, ORANGE, box)
        elif numberArr[index] == 3:
            pygame.draw.rect(WIN, TEAL, box)
        elif numberArr[index] == 4:
            pygame.draw.rect(WIN, PURPLE, box)

    buttons = {
        (submit_button.topleft,  submit_button.size) : ((int(dimension*0.04), int(dimension-(dimension*0.0025))), "Submit"),
        (solve_button.topleft,  solve_button.size) : ((int(dimension*0.2125), int(dimension-(dimension*0.0025))), "Solve")
    }
    #Drawing Button
    draw_buttons(buttons)
    
    #Draws the lines
    for x in range(0, dim+box_dimension, box_dimension):
        pygame.draw.line(WIN, BLACK, (x, 0), (x, dim))
        pygame.draw.line(WIN, BLACK, (0, x), (dim, x))

def changePoint(mouseNum, pos, numberArr, rectangleArr):
    x = (pos[0] // box_dimension) * box_dimension
    y = (pos[1] // box_dimension) * box_dimension
    index = indexAtLocation(x, y)

    boxPerLen = (dimension//box_dimension)
    
    if mouseNum == 1 or mouseNum == 4:
        if pygame.Rect(x, y, box_dimension, box_dimension) not in rectangleArr:
            rectangleArr.append(pygame.Rect(x, y, box_dimension, box_dimension))
            numberArr[index] = mouseNum
        

    if mouseNum == 3:
        if index > boxPerLen and index < (boxPerLen**2)-boxPerLen and index % boxPerLen != 0 and index % boxPerLen != boxPerLen-1 and (numberArr[index] == 1  or numberArr[index] == 4):
            numberArr[index] = 0
            rectangleArr.remove(pygame.Rect(x,y, box_dimension, box_dimension))


    return numberArr, rectangleArr

        
def validate_board(numberArr, rectangleArr):
    start = indexAtLocation(rectangleArr[0].topleft[0], rectangleArr[0].topleft[1])

    boxPerLen = dimension // box_dimension
    boxDrawnSize = (box_dimension, box_dimension)

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
                    currentLoc = locationOfIndex(start+i)
                    curr_set.append((currentLoc[0], currentLoc[1]))
                    pygame.draw.rect(WIN, BLACK, (currentLoc[0], currentLoc[1], boxDrawnSize[0], boxDrawnSize[1]))
                    temp = curr_set
            
        elif not firstRun:
            for location in curr_set:
                index = indexAtLocation(location[0], location[1])
                for delta in [(index+1),(index-1),(index+boxPerLen),(index-boxPerLen)]:
                    if((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in closed_set) and ((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in temp) and ((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in curr_set) and (numberArr[delta] == 0 or numberArr[delta] == 3):
                            temp.append(locationOfIndex(delta))

        
        for location in temp:
            pygame.draw.rect(WIN, GREEN, (location[0], location[1], boxDrawnSize[0], boxDrawnSize[1]))



        for location in temp:
            closed_set.append(location) 
        curr_set = temp

        
        firstRun = False
        turns += 1
        

    

    print("\nDone \n")
    



def main():    
    mouse_L_Down, mouse_R_Down = False, False
    num_board, rect_board, submit, solve  = buildBoard(dimension)   

    Solve_Or_Draw = 1

    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: mouse_L_Down = True
                elif event.button == 3: mouse_R_Down = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    print("Checking...")
                    valid_solution(rect_board, num_board) 
            elif event.type == pygame.MOUSEBUTTONUP: mouse_L_Down, mouse_R_Down = False, False
            elif event.type == pygame.QUIT: run = False

        if mouse_L_Down: # If left clicked       
            pos = pygame.mouse.get_pos()
            if pos[1] < dimension:
                num_board, rect_board = changePoint(Solve_Or_Draw, pos, num_board, rect_board)
            if submit.collidepoint(pos):
                print("Submit")
                mouse_L_Down = False
                validate_board(num_board, rect_board)
            if solve.collidepoint(pos):
                print("Solve")
                if Solve_Or_Draw == 1:
                    Solve_Or_Draw = 4
                elif Solve_Or_Draw == 4:
                    Solve_Or_Draw = 1
                mouse_L_Down = False


        elif mouse_R_Down: # If right clicked
            pos = pygame.mouse.get_pos()
            if pos[1] < dimension:
                num_board, rect_board = changePoint(3, pos, num_board, rect_board)

                
                

        
        
        draw_board(dimension, submit, solve, num_board, rect_board) # Update Visuals

        pygame.display.update()








if __name__ == "__main__":
    main()