
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

def manhatthan(x, y, goalNode):
    return (abs(x - goalNode.position[0]) + abs(y - goalNode.position[1]))

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
            exit(1);
        #Se selecciona el node de menor peso en su f, el primero MEJORNODO
        node = min(openList, key=lambda x: x.fs)
        #Se remueve de la openList porque ya será visitado
        openList.remove(node)
        #Se añade de la closeList porque...
        closeList.append(node)
        #Condición de victoria
        if node.isGoal(goalNode):
            endNode = node
            break
        #Se calcula el g(node) actual
        node_gs = node.fs - node.heuristicValue
        #Al no llegar a la solución con el node actual, se selecciona uno mejor del grafo 
        # respecto a MEJORNODO
        for v in graph.adjacencyList[node.position]:
            pointB = v.pointB
            sucesor = openList.find(pointB)
            #Se alamcena la distancia en variable para sumas posteriores
            distance = v.distance
            #el node node (actual) pasa a ser el node node (viejo) ahora
            if sucesor:         #n_gs + sucesor.hs + distance = f(node)    
                #Si el peso total (f) de sucesor > f(node)
                if sucesor.fs > node_gs + sucesor.hs + distance:
                    sucesor.fs = node_gs + sucesor.hs + distance
                    #Se le añade su nodoviejo al ser correcto que es mayor
                    sucesor.parent_node = node
            else:
                sucesor = closeList.find(pointB)
                if sucesor:
                    if sucesor.fs > node_gs + sucesor.hs + distance:
                        sucesor.fs = node_gs + sucesor.hs + distance
                        sucesor.parent_node = node
                        openList.append(sucesor)
                        closeList.remove(sucesor)
                else:
                    sucesor = Node(pointB)
                    sucesor.fs = node_gs + sucesor.hs + distance
                    sucesor.parent_node = node
                    openList.append(sucesor)
                    print(node.position + ' a ' + sucesor.position + ': ' + str(sucesor.hs+distance) + ' = ' + str(distance) + ' + ' + str(sucesor.heuristicValue))
#node = endNode
#sol = []
#while True:
#    sol.append(node.city)
#    if node.parent_node == None:
#        break
#    node = node.parent_node
#sol.reverse()
#print(list(sol))