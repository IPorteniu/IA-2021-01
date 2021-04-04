
# A* algorithm has 3 parameters:

# g : the cost of moving from the initial cell to the current cell. Basically, it is the sum of all the cells that have been visited since leaving the first cell.
# h : also known as the heuristic value, it is the estimated cost of moving from the current cell to the final cell. 
# The actual cost cannot be calculated until the final cell is reached. Hence, h is the estimated cost. We must make sure that there is never an over estimation of the cost.

# f : it is the sum of g and h. So, f = g + h

# The way that the algorithm makes its decisions is by taking the f-value into account. 
# The algorithm selects the smallest f-valued cell and moves to that cell. 
# This process continues until the algorithm reaches its goal cell.

class Node(object):
    def __init__(self,position):
        self.position = position
        self.heuristicValue = None
        self.fs = 0
        self.parentNode = None

    def isGoal(self,goalNode):
        return goalNode == self.position

class Edge(object):
    def __init__(self, pointB, distance):
        self.pointB = pointB
        self.distance = distance

def Manhatthan(x, y, goalNode):
    return (abs(x - goalNode.position[0]) + abs(y - goalNode.position[1]))

def aStar(start, goal, grid):
    #The open and closed sets
    openset = set()
    closedset = set()
    #Current point is the starting point
    current = start
    #Add the starting point to the open set
    openset.add(current)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children/siblings
        for node in children(current,grid):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score 
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                openset.add(node)

