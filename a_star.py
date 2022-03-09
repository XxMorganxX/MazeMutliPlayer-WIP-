"""
CREDIT:
VaibhavSaini19 - Github
For A* algorithm
https://github.com/VaibhavSaini19/A_Star-algorithm-in-Python/blob/master/A-Star%20Algorithm

"""
from queue import PriorityQueue

    
def reconstruct_path(came_from, current):
    final_path = [current]
    while current in came_from:
        current = came_from[current]
        final_path.append(current)
    return final_path


def heauristic(cell, goal):
    x1, y1 = cell
    x2, y2 = goal

    dist = (((x2-x1)**2 + (y2-y1)**2))**0.5
    return dist


def A_star_func(graph, start, goal):

    closed_set = []  # nodes already evaluated 
    # Arr representing nodes that have already been checked

    open_set = [start]  # nodes discovered but not yet evaluated
    #Nodes currently dealing with

    came_from = {}  # most efficient path to reach from
    #Dictionary 

    gscore = {}  # cost to get to that node from start

    for key in graph:
        gscore[key] = 100  # intialize cost for every node to inf

    gscore[start] = 0

    fscore = {}  # cost to get to goal from start node via that node

    for key in graph:
        fscore[key] = 100

    fscore[start] = heauristic(start, goal)  # cost for start is only h(x)

    while open_set:
        min_val = 1000  # find node in openset with lowest fscore value
        for node in open_set:
            if fscore[node] < min_val:
                min_val = fscore[node]
                min_node = node

        current = min_node  # set that node to current
        if current == goal:
            return reconstruct_path(came_from, current)
        open_set.remove(current)  # remove node from set to be evaluated and
        closed_set.append(current)  # add it to set of evaluated nodes

        for neighbor in graph[current]:  # check neighbors of current node
            if neighbor in closed_set:  # ignore neighbor node if its already evaluated
                continue
            if neighbor not in open_set:  # else add it to set of nodes to be evaluated
                open_set.append(neighbor)

            # dist from start to neighbor through current
            tentative_gscore = gscore[current] + 1

            # not a better path to reach neighbor
            if tentative_gscore >= gscore[neighbor]:
                continue
            came_from[neighbor] = current  # record the best path untill now
            gscore[neighbor] = tentative_gscore
            fscore[neighbor] = gscore[neighbor] + heauristic(neighbor, goal)
    return False