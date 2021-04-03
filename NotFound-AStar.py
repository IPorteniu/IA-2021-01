# A* algorithm has 3 parameters:

# g : the cost of moving from the initial cell to the current cell. Basically, it is the sum of all the cells that have been visited since leaving the first cell.
# h : also known as the heuristic value, it is the estimated cost of moving from the current cell to the final cell. 
# The actual cost cannot be calculated until the final cell is reached. Hence, h is the estimated cost. We must make sure that there is never an over estimation of the cost.

# f : it is the sum of g and h. So, f = g + h

# The way that the algorithm makes its decisions is by taking the f-value into account. 
# The algorithm selects the smallest f-valued cell and moves to that cell. 
# This process continues until the algorithm reaches its goal cell.


class Node(object):
    def __init__(self,pointA):
        self.pointA = pointA
        self.heuristic_value = heuristics[pointA]
        self.fs = 0
        self.parent_node = None
    
    def isGoal(self):
        return goalNode == self.point

class Edge(object):
    def __init__(self, pointB, distance):
        self.pointB = pointB
        self.distance = distance
        
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

def Manhatthan(x, y, goalNode):
    return (abs(x - goalNode[0]) + abs(y - goalNode[1]))

def createHeuristics(lenght,width,goalNode):
    heuristics = dict()
    # Para la creacion de las heuristicas usaremos Manhatthan
    for x in range(0,lenght,10):
        for y in range(0, width,10):
            heuristics[(x,y)] = Manhatthan(x, y, goalNode)
    return heuristics

def createAdjacencyList(heuristics):

    adjacencyList = dict()

    for key in heuristics:
        adjacencyList[key] = []
    return adjacencyList

def addEdge(pointA, pointB, distance):   
    graph[pointA].append(Edge(pointB, distance))
    graph[pointB].append(Edge(pointA, distance))

def createEdges():
    addEdge((0,0), (10,0), 10)
    addEdge((10,0), (20,0), 10)
    addEdge((20,0), (30,0), 10)

    addEdge((0,0), (0,10), 10)
    addEdge((0,10), (0,20), 10)
    addEdge((0,20), (0,30), 10)
    
    addEdge((0,30), (10,30), 10)
    addEdge((10,30), (20,30), 10)
    addEdge((20,20), (30,30), 10)
   
    addEdge((30,0), (30,10), 10)
    addEdge((30,10), (30,20), 10)
    addEdge((30,20), (30,30), 10)
   
    addEdge((0,10), (10,10), 10)
    addEdge((10,10), (10,0), 10)
    addEdge((10,10), (10,20), 10)
    addEdge((10,10), (20,10), 10)
   
    addEdge((10,20), (10,30), 10)
    addEdge((10,20), (0,20), 10)
    addEdge((10,20), (20,20), 10)
   
    addEdge((20,20), (20,30), 10)
    addEdge((20,20), (30,20), 10)
    addEdge((20,20), (20,10), 10)
   
    addEdge((20,10), (30,10), 10)
    addEdge((20,10), (20,0), 10)

def main():

    lenght = 40 # x
    width = 40 # y
    goalNode = (40, 30)
    heuristics = createHeuristics(lenght,width,goalNode)

    #Convertir graph en una clase con width y lenght, goalnode y startnode
    global graph
    graph = createAdjacencyList(heuristics)
    createEdges()
    print(graph.values())

main()



