
from Grid import Grid
from GridUtils import Node 



#El ancho y el largo no se puede automatizar porque no tenemos generadores de aristas
lenght = 40
width = 40 

#Se asigna la meta y el inicio

goalNode = Node((40, 30))
startNode = Node((0, 0))
graph = Grid()
graph.buildGrid(lenght, width,startNode,goalNode)
graph.findPath()





