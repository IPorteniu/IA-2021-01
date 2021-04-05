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

class Node(object):
    def __init__(self,position):
        self.position = position
        self.heuristicValue = 0
        self.fs = 0
        self.parentNode = None
        self.adjacencyList = []

    def isGoal(self,goalNode):
        return goalNode == self.position

class Edge(object):
    def __init__(self, pointB, distance):
        self.pointB = pointB
        self.distance = distance

def manhatthan(x, y, goalNode):
    return (abs(x - goalNode[0]) + abs(y - goalNode[1]))

class NodeList(list):
    def find(self, position):
        actual = [node for node in self if node.position == position]
        return actual[0] if actual != [] else None
       

    def remove(self, node):
        del self[self.index(node)]

def astar(startNode,goalNode,graph):
    #Se crea openList y closeList
    openList = NodeList()
    closeList = NodeList()
    #Se añade el startNode a la openList
    openList.append(startNode)
    while True:
        #Si la openList está vacia ya fue la vida
        if openList == []:
            print("No fue posible encontrar una ruta")
            exit(1)
        #Se selecciona el node de menor peso en su f, el primero MEJORNODO
        node = min(openList, key=lambda x: x.fs)
        #Se remueve de la openList porque ya será visitado
        openList.remove(node)
        #Se añade de la closeList porque...
        closeList.append(node)
        #Condición de victoria
        if node.isGoal(goalNode.position):
            endNode = node
            return endNode
        #Se calcula el g(node) actual
        node_gs = node.fs - node.heuristicValue
        #Al no llegar a la solución con el node actual, se selecciona uno mejor del grafo 
        # respecto a MEJORNODO
        for v in node.adjacencyList:
            nodeB = graph.findNode(v.pointB)
            sucesor = openList.find(nodeB)
            #Se alamcena la distancia en variable para sumas posteriores
            distance = v.distance 
            #el node node (actual) pasa a ser el node node (viejo) ahora
            if sucesor:         #n_gs + sucesor.heuristicValue + distance = f(node)    
                #Si el peso total (f) de sucesor > f(node)
                if sucesor.fs > node_gs + sucesor.heuristicValue + distance:
                    sucesor.fs = node_gs + sucesor.heuristicValue + distance
                    #Se le añade su nodoviejo al ser correcto que es mayor
                    sucesor.parentNode = node
            else:
                sucesor = closeList.find(nodeB.position)
                if sucesor:
                    if sucesor.fs > node_gs + sucesor.heuristicValue + distance:
                        sucesor.fs = node_gs + sucesor.heuristicValue + distance
                        sucesor.parentNode = node
                        openList.append(sucesor)
                        closeList.remove(sucesor)
                else:
                    sucesor = graph.findNode(nodeB.position)
                    sucesor.fs = node_gs + sucesor.heuristicValue + distance
                    sucesor.parentNode = node
                    openList.append(sucesor)
                    print(str(node.position) + ' a ' + str(sucesor.position) + ': ' + str(sucesor.heuristicValue+distance) + ' = ' + str(distance) + ' + ' + str(sucesor.heuristicValue))

#El ancho y el largo no se puede automatizar porque no tenemos generadores de aristas
lenght = 40
width = 40 

def findSol(graph):
    n = graph.findPath()
    sol = []
    while True:
        sol.append(n.position)
        if n.parentNode == None:
            break
        n = n.parentNode
    sol.reverse()
    print(list(sol))


#Se asigna la meta y el inicio
goal = (30,30)
start = (0,0)
graph = Grid()
graph.buildGrid(lenght, width,start, goal)
findSol(graph)