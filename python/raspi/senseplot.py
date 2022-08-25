import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 255])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

plt.show()