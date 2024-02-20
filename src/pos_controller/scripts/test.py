import unittest, json
import numpy as np
# from mobility import random_direction

# rw = random_waypoint(200, dimensions=(100, 100), velocity=(0.1, 1.0), wt_max=1.0)
# rd = random_direction(20, dimensions=(100, 100,100), velocity=(0.1, 1.0), wt_max=1.0)
# array = next(rd).tolist()
# px,py,pz = [],[],[]
# for p in array:
#     px.append(p[0])
#     py.append(p[1])
#     pz.append(p[2])

# for goal_x, goal_y, goal_z in zip(px,py, pz):
#     print('Goal is', goal_x, goal_y, goal_z)
import numpy as np

def generate_random_positions(n, x_range, y_range,z_range):
    positions = []
    
    for _ in range(n):
        x = np.random.uniform(*x_range)
        y = np.random.uniform(*y_range)
        z = np.random.uniform(*z_range)
        # Ensure z is greater than 0
        while z <= 0:
            z = np.random.uniform(*z_range)
        positions.append([x, y, z])

    return positions

# Example usage
n_positions = 5
x_range = (-50, 50)  # Example x-axis range
y_range = (-50, 50)  # Example y-axis range
z_range = (1, 50) 

allPositions = generate_random_positions(5,(-50, 50),(-50, 50),(10, 50))
px,py,pz = [],[],[]
for p in allPositions:
    px.append(p[0])
    py.append(p[1])
    pz.append(p[2])

print(f'x {px}')
print(f'y {py}')
print(f'z {pz}')