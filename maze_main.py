from collections import defaultdict
import a_star, pygame, random, maze_solution


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

#Constants
FPS = 100
box_dimension = 15

#Getting Functions
def indexOfBox(box):
    return (box.topleft[0] // box_dimension) + ((box.topleft[1] // box_dimension) * (dimension//box_dimension))

def indexAtLocation(x, y):
    return (x // box_dimension) + ((y // box_dimension) * (dimension//box_dimension))

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
    
    index1 = random.randint(0, int(len(numArr) * .25))
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
    
    print(len(rectangleArr))

    return numberArr, rectangleArr
        
def validate(numberArr, rectangleArr): #WIP - This is supposed to validate the maze
    maze_solution.validate_board(numberArr, rectangleArr, dimension, box_dimension)

    



def main():    
    mouseDown = False
    num_board, rect_board, submit  = buildBoard(dimension)   


    run = True
    while run:
        WIN.fill(WHITE)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP: mouseDown = False
            elif event.type == pygame.QUIT: run = False

        if mouseDown:      
            pos = pygame.mouse.get_pos()
            if pos[1] <= dimension:
                num_board, rect_board = changePoint(pos, num_board, rect_board)
            elif submit.collidepoint(pos):
                print("Submit")
                validate(num_board, rect_board) # W.I.P.
                mouseDown = False
                

        
        
        draw_board(dimension, submit, num_board, rect_board)

        pygame.display.update()








if __name__ == "__main__":
    main()