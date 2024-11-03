import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
rolls = int(8e6)
L = 1
counter = 0
track = []


def compute_nearest(array):
    x, y = array[0], array[1]
    distances = np.array([y, x, L - y, L - x])
    # Find the index of the minimum distance
    position = {0: 'bottom', 1: 'left', 2: 'top', 3: 'right'}
    nearest_side_index = np.argmin(distances)
    return position[nearest_side_index]


def area_in_target(position: str, red_dot: np.array, blue_dot: np.array):
    if position == 'bottom':
        sides = np.array([[0, 0], [1, 0]])
    if position == 'left':
        sides = np.array([[0, 0], [0, 1]])
    if position == 'top':
        sides = np.array([[0, 1], [1, 1]])
    if position == 'right':
        sides = np.array([[1, 0], [1, 1]])
    distance_0 = np.linalg.norm(red_dot - sides[0])
    distance_1 = np.linalg.norm(red_dot - sides[1])

    distance_ref_0 = np.linalg.norm(blue_dot - sides[0])
    distance_ref_1 = np.linalg.norm(blue_dot - sides[1])

    if (distance_0 <= distance_ref_0 or distance_1 <= distance_ref_1) and not (distance_0 <= distance_ref_0 and distance_1 <= distance_ref_1):
        return 1
    else:
        return 0


def uniform_exclusive(lower, upper, size):
    values = np.random.uniform(lower, upper, size)
    while np.any(values == lower) or np.any(values == upper):
        mask = (values == lower) | (values == upper)
        values[mask] = np.random.uniform(lower, upper, np.sum(mask))
    return values

for i in tqdm(range(rolls)):
    # blue = np.random.uniform(0, L, 2)
    red = np.random.uniform(0, L, 2)
    blue = uniform_exclusive(0, L, 2)
    red = uniform_exclusive(0, L, 2)
    side = compute_nearest(blue)
    counter += area_in_target(side, red, blue)
    track.append(counter)

track = np.array(track)
track = track / np.arange(1, len(track)+1)
plt.plot(track[2:])
plt.grid(True)
plt.show()
print(track[-1])
