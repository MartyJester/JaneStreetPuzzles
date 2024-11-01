import numpy as np
import random

rolls = int(1e4)
L = 1
counter = 0

def compute_nearest(array):
    x, y = array[0], array[1]
    distances = np.array([y, x, L - y, L - x])
    # Find the index of the minimum distance
    position = {0: 'bottom', 1: 'left', 2: 'top', 3: 'right'}
    nearest_side_index = np.argmin(distances)
    return position[nearest_side_index]




for i in range(50):
    blue = np.random.uniform(0, L, 2)
    red = np.random.uniform(0, L, 2)
    side = compute_nearest(blue)
    print(side)




