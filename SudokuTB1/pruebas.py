import numpy as np
import matplotlib.pyplot as plt

plt.axis([1000, 0, 0, 50])
plt.ylabel("Temperatura")
plt.xlabel("Heuristica")
plt.title("Simulated Annealing")
for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)


plt.show()