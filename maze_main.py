import a_star, pygame



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


#Constants
FPS = 30


def buildBoard(dim):
    board = []
    for y in range(0, dim, 10):
        temp_row = []
        for x in range(0, dim, 10):
            temp_row.append(0)
        board.append(temp_row)
    return board

def draw_board(dim):
    box_dimension = 15
    for x in range(0, dim, box_dimension):
        pygame.draw.line(WIN, BLACK, (x, 0), (x, dim))
        pygame.draw.line(WIN, BLACK, (0, x), (dim, x))
        


def main():
    empty_board = buildBoard(dimension)
    print(empty_board)
    run = True
    while run:
        WIN.fill(WHITE)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
        
        draw_board(dimension)

        pygame.display.update()








if __name__ == "__main__":
    main()