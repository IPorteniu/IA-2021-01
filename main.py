
from Grid import Grid
from GridUtils import Node 



#El ancho y el largo no se puede automatizar porque no tenemos generadores de aristas
lenght = 40
width = 40 

#Se asigna la meta y el inicio

goal = (30,30)
start = (0,0)
graph = Grid()
graph.buildGrid(lenght, width,start, goal)
n = graph.findPath()
sol = []
while True:
    sol.append(n.position)
    if n.parentNode == None:
        break
    n = n.parentNode
sol.reverse()
print(list(sol))




