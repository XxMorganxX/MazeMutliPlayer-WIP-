import re
import a_star, pygame, random

"""
NUMBER ARR KEY:
0 = empty
1 = Boarder
2 = Start
3 = Stop
"""

#Pygame General Setup
pygame.init
clock = pygame.time.Clock()

#Pygame Window Setup
dimension = 900
WIN_SIZE = dimension, dimension
WIN = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("MAZE SINGLE PLAYER")



#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (0,128,128)
ORANGE = (255, 203, 62)

#Constants
FPS = 30


def buildBoard(dim):
    numArr = []
    
    """
    #Generates Rects
    for x in range(0, dim, box_dim):
        for y in range(0, dim, box_dim):
            box = pygame.Rect(x, y, dim, dim)
            rectArr.append(box)
    """
    for y in range(0, dim, box_dimension):
        for x in range(0, dim, box_dimension):
            numArr.append(0)
    return numArr
    

def draw_board(dim, numberArr, rectangleArr):
    #Draw Rects
    for box in rectangleArr:
        index = box.topleft // box_dimension
        if numberArr[index] == 0:
            pygame.draw.rect(WIN, WHITE, box)
        elif numberArr[index] == 1:
            pygame.draw.rect(WIN, BLACK, box)
        elif numberArr[index] == 2:
            pygame.draw.rect(WIN, TEAL, box)
        elif numberArr[index] == 3:
            pygame.draw.rect(WIN, ORANGE, box)
    
    #Draws the lines
    for x in range(0, dim, box_dimension):
        pygame.draw.line(WIN, BLACK, (x, 0), (x, dim))
        pygame.draw.line(WIN, BLACK, (0, x), (dim, x))

def changePoint(mousePos, turn, numberArr, rectangleArr):
    whichBox = None
    x = (mousePos[0] // 15) * box_dimension # x postion of the nearest top left corner
    y = (mousePos[1] // 15) * box_dimension # y position of nearest top left corner

    pygame.draw.rect(WIN, BLACK, (x,y, box_dimension, box_dimension))



    
    return numberArr, rectangleArr
        


def main():
    global box_dimension

    box_dimension = 15  
    num_board = buildBoard(dimension)   
    rect_board = []
    turn = 0
    run = True
    while run:
        WIN.fill(WHITE)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                num_board, rect_board = changePoint(pos, turn, num_board, rect_board)
                turn += 1
        
        
        draw_board(dimension, num_board, rect_board)

        pygame.display.update()








if __name__ == "__main__":
    main()