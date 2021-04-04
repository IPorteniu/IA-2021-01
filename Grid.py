from GridUtils import Node
from GridUtils import Edge
from GridUtils import manhatthan
from GridUtils import astar

class Grid(object):
    def __init__(self):
        self._lenght = 0
        self._width = 0
        self._startNode = Node
        self._goalNode = Node
        self._heuristics = dict()
        self._graph = dict()
        self._adjacencyList = dict()
    
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
                self._heuristics[(x,y)] = manhatthan(x, y, self._goalNode)

    def __createGraph(self):
        for point in self._heuristics:
            actualNode = Node(point)
            actualNode.heuristicValue = self._heuristics[point]
            self._graph[point] = actualNode
        
    def __createAdjacencyList(self):
        for key in self._heuristics:
            self._adjacencyList[key] = []
    
    def addEdge(self, pointA, pointB, distance):   
        self._adjacencyList[pointA].append(Edge(pointB, distance))
        self._adjacencyList[pointB].append(Edge(pointA, distance))
  
    def findNode(self, position):
        return self._graph[position]
    
    def findPath(self):
        astar(self._startNode,self._goalNode,self._graph)

    def buildGrid(self, lenght, width, startNode,goalNode):
        self._lenght = lenght
        self._width = width
        self._startNode = startNode
        self._goalNode = goalNode
        self.__createHeuristics()
        self._startNode = self.findNode(startNode)
        self._goalNode = self.findNode(goalNode)
        self.__createGraph()
        self.__createAdjacencyList()
        self.__createEdges()

        
    

   


