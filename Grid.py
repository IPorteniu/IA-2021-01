from GridUtils import Node
from GridUtils import Edge
from GridUtils import manhatthan
from GridUtils import astar

class Grid(object):
    def __init__(self):
        self._lenght = 0
        self._width = 0
        self._start = None
        self._goal = None
        self._heuristics = dict()
        self._graph = dict()
    
    def getLenght(self):
        return self._lenght

    def getWidth(self):
        return self._width

    def __createEdges(self):
        self.addEdge((0,0), (10,0), 10)
        self.addEdge((10,0), (20,0), 10)
        self.addEdge((20,0), (30,0), 10)

        self.addEdge((0,0), (0,10), 10)
        self.addEdge((0,10), (0,20), 10)
        self.addEdge((0,20), (0,30), 10)

        self.addEdge((0,30), (10,30), 10)
        self.addEdge((10,30), (20,30), 10)
        self.addEdge((20,20), (30,30), 10)

        self.addEdge((30,0), (30,10), 10)
        self.addEdge((30,10), (30,20), 10)
        self.addEdge((30,20), (30,30), 10)

        self.addEdge((0,10), (10,10), 10)
        self.addEdge((10,10), (10,0), 10)
        self.addEdge((10,10), (10,20), 10)
        self.addEdge((10,10), (20,10), 10)

        self.addEdge((10,20), (10,30), 10)
        self.addEdge((10,20), (0,20), 10)
        self.addEdge((10,20), (20,20), 10)
        self.addEdge((20,20), (20,30), 10)

        self.addEdge((20,20), (30,20), 10)
        self.addEdge((20,20), (20,10), 10)
        self.addEdge((20,10), (30,10), 10)
        self.addEdge((20,10), (20,0), 10)
      
    def __createHeuristics(self):
        # Para la creacion de las heuristicas usaremos Manhatthan
        for x in range(0,self._lenght,10):
            for y in range(0, self._width,10):
                self._heuristics[(x,y)] = manhatthan(x, y, self._goal)

    def __createGraph(self):
        for point in self._heuristics:
            actualNode = Node(point)
            actualNode.heuristicValue = self._heuristics[point]
            self._graph[point] = actualNode
    
    def addEdge(self, pointA, pointB, distance): 
        nodeA = self.findNode(pointA)  
        nodeB = self.findNode(pointB)  
        
        nodeA.adjacencyList.append(Edge(pointB, distance))
        nodeB.adjacencyList.append(Edge(pointA, distance))
  
    def findNode(self, position):
        return self._graph[position]
    
    def findPath(self):
        startNode = self.findNode(self._start)
        goalNode = self.findNode(self._goal)
        return astar(startNode , goalNode, self)

    def buildGrid(self, lenght, width, start,goal):
        self._lenght = lenght
        self._width = width
        self._start = start
        self._goal = goal
        self.__createHeuristics()
        self.__createGraph()
        self.__createEdges()

        
    

   


