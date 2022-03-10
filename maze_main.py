from collections import defaultdict
import pygame, random, maze_solution, time


"""
NUMBER ARR KEY:
0 = empty
1 = Boarder
2 = Start
3 = Stop
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

#Constants
FPS = 1
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
    for y in range(0, dim, box_dimension):
        for x in range(0, dim, box_dimension):
            numArr.append(0)
    
    #index1 = random.randint(0, int(len(numArr) * .25))
    index1 = 400
    index2 = random.randint(int(len(numArr) * .75), int(len(numArr) * .99))
    
    rectArr.append(pygame.Rect(locationOfIndex(index1), (box_dimension, box_dimension)))
    rectArr.append(pygame.Rect(locationOfIndex(index2), (box_dimension, box_dimension)))
    numArr[index1] = 2
    numArr[index2] = 3

    button = pygame.Rect(((dimension*0.015), dimension + (margin*0.1), (dimension*0.15), (margin*0.8)))

    return numArr, rectArr, button
    

def draw_board(dim, button, numberArr, rectangleArr):
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

   
    #Drawing Button
    submit_text = MAIN_FONT.render("Submit", 1, BLACK)
    pygame.draw.rect(WIN, BLUE, button, border_radius=100)
    WIN.blit(submit_text, (int(dimension*0.04), int(dimension-(dimension*0.0025))))
    
    #Draws the lines
    for x in range(0, dim+box_dimension, box_dimension):
        pygame.draw.line(WIN, BLACK, (x, 0), (x, dim))
        pygame.draw.line(WIN, BLACK, (0, x), (dim, x))

def changePoint(pos, numberArr, rectangleArr):
    x = (pos[0] // box_dimension) * box_dimension
    y = (pos[1] // box_dimension) * box_dimension
    index = indexAtLocation(x, y)
    
    if pygame.Rect(x, y, box_dimension, box_dimension) not in rectangleArr:
        rectangleArr.append(pygame.Rect(x, y, box_dimension, box_dimension))
        numberArr[index] = 1
    boxPerLen = dimension // box_dimension
    print(indexAtLocation(rectangleArr[-1].topleft[0], rectangleArr[-1].topleft[1]))
    print(index > boxPerLen, index < (box_dimension**2-boxPerLen),index % boxPerLen != 0, index % boxPerLen != (boxPerLen-1))

    return numberArr, rectangleArr
        
def validate_board(numberArr, rectanlgeArr):
    start = indexAtLocation(rectanlgeArr[0].topleft[0], rectanlgeArr[0].topleft[1])
    end = indexAtLocation(rectanlgeArr[1].topleft[0], rectanlgeArr[1].topleft[1])

    boxPerLen = dimension // box_dimension
    boxDrawnSize = (box_dimension, box_dimension)

    solved = False
    firstRun = True
    closed_set = []
    curr_set = []
    temp = []
    
    turns = 0

    while turns <= 30:
        temp = []
        if (rectanlgeArr[1].topleft[0], rectanlgeArr[1].topleft[1]) in curr_set or (rectanlgeArr[1].topleft[0], rectanlgeArr[1].topleft[1]) in closed_set:
            solved = True
            print("found")

        if firstRun:
            for i in [(1), (-1), (-boxPerLen), (boxPerLen)]:
                if numberArr[start+i] == 0:
                    currentLoc = locationOfIndex(start+i)
                    curr_set.append((currentLoc[0], currentLoc[1]))
                    pygame.draw.rect(WIN, BLACK, (currentLoc[0], currentLoc[1], boxDrawnSize[0], boxDrawnSize[1]))
                    temp = curr_set
            print("\n First Done")
            print(curr_set)
            
        elif not firstRun:
            print("Other Runs")
            for location in curr_set:
                index = indexAtLocation(location[0], location[1])
                for delta in [(index+1),(index-1),(index+boxPerLen),(index-boxPerLen)]:
                    if not (index % (boxPerLen-1 ) == 0 and delta % boxPerLen == 0):
                        if ((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in closed_set) and ((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in temp) and numberArr[delta] == 0:
                            if delta > boxPerLen or delta < (box_dimension**2-boxPerLen) or delta % boxPerLen != 0 or delta % boxPerLen != (boxPerLen-1):
                                temp.append(locationOfIndex(delta))
                    elif not (index % (boxPerLen) == 0 and delta % boxPerLen-1 == 0):
                        if ((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in closed_set) and ((locationOfIndex(delta)[0], locationOfIndex(delta)[1]) not in temp) and numberArr[delta] == 0:
                            if delta > boxPerLen or delta < (box_dimension**2-boxPerLen) or delta % boxPerLen != 0 or delta % boxPerLen != (boxPerLen-1):
                                temp.append(locationOfIndex(delta))
                    #else:
                        #continue

        for location in closed_set:
            pygame.draw.rect(WIN, DARKGREEN, (location[0], location[1], boxDrawnSize[0], boxDrawnSize[1]))
            print("DRAW 1")
        for location in temp:
            pygame.draw.rect(WIN, GREEN, (location[0], location[1], boxDrawnSize[0], boxDrawnSize[1]))
            print("DRAW 2")

        for location in temp:
            closed_set.append(location) 
        curr_set = temp
        """for location in closed_set:
            curr_set.remove(location)"""
        #temp.clear()
        

        
        firstRun = False
        
        
        turns += 1
    
    print(len(temp))
    print("\n Done \n")
    



def main():    
    mouseDown = False
    num_board, rect_board, submit  = buildBoard(dimension)   


    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP: mouseDown = False
            elif event.type == pygame.QUIT: run = False

        if mouseDown:      
            pos = pygame.mouse.get_pos()
            if pos[1] < dimension:
                num_board, rect_board = changePoint(pos, num_board, rect_board)
            if submit.collidepoint(pos):
                print("Submit")
                validate_board(num_board, rect_board) # W.I.P.

                mouseDown = False
                

        
        
        draw_board(dimension, submit, num_board, rect_board)

        pygame.display.update()








if __name__ == "__main__":
    main()