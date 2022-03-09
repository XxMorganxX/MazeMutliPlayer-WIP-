import maze_main as main

def validate_board(numberArr, rectanlgeArr, dim, box_size):
    start = main.indexAtLocation(rectanlgeArr[0].topleft[0], rectanlgeArr[0].topleft[1])
    end = main.indexAtLocation(rectanlgeArr[1].topleft[0], rectanlgeArr[1].topleft[1])

    boxPerLen = dim // box_size

    Solved = False
    closed_set = []

    while not Solved:
        for index in range(0, len(numberArr)):
            if index > boxPerLen and index < (boxPerLen*(boxPerLen-1)) and index % boxPerLen > 0 and index % boxPerLen < boxPerLen: 
                print(index)
                #for i in [(1), (-1), (-boxPerLen), (boxPerLen)]:


                
    

