import numpy as np
import copy
import random


class Item:
    def __init__(self, id=0, value=0, weight=0):
        self.id = id
        self.value = value
        self.weight = weight


class Backpack:
    def __init__(self, cap, items = []):
        self.capacity = cap
        self.items = items
        self.best = []
        self.maxValue = 0

    def add_item(self, value, weight):
        id = len(self.items) + 1
        self.items.append(Item(id, value, weight))

    def hill_climbing(self):
        for i, _ in enumerate(self.items):
            weight = 0
            value = 0
            end = False
            init = copy.deepcopy(self.items)
            random.shuffle(init)
            start = init.pop(i)
            sol = []
            sol.append(start)
            weight += start.weight
            value += start.value
            print("INICIO: %i %i" % (start.value, start.weight))
            while not end:
                bestit = sol[-1]
                auxw = 9999
                auxv = 0
                for item in init:
                    if (item.weight + weight) <= self.capacity and (item.value + value) > auxv and (item.weight + weight) < auxw:
                        auxv = item.value
                        bestit = item
                if bestit != sol[-1]:
                    weight += bestit.weight
                    value += bestit.value
                    init.remove(bestit)
                    sol.append(bestit)
                else:
                    if value > self.maxValue:
                        self.best = copy.deepcopy(sol)
                        self.maxValue = value
                    print("Máximo hasta ahora: %i" % (self.maxValue))
                    print("Valor: %i, Peso: %i de %i\n" % (value, weight, self.capacity))
                    end = True
        
    def find_solution(self):
        self.hill_climbing()
        self.print_solution()

    def print_solution(self):
        print("\nMEJOR SOLUCION: ")
        print("Valor: %i, Peso: %i de %i" %
            (sum([x.value for x in self.best]), sum([x.weight for x in self.best]), self.capacity))
        for item in self.best:
            print('\t', item.id, item.value, item.weight)

    

backpack = Backpack(16)
backpack.add_item(8, 5)
backpack.add_item(7, 6)
backpack.add_item(12, 10)
backpack.add_item(6, 4)
backpack.add_item(2, 1)
backpack.add_item(3, 1)
backpack.find_solution()

