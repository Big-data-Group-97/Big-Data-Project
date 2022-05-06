import os
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from time import time

'''
TODO:
- finish basic implementation
    - check ouput aganist correct values
    - use time to compute performance
- optimize
    - see what kind of debug tools can be used to check performance
    - precompute distances
        - optmize precomputeation to avoid usless and doubles
    - find other methods
    - see if numpy helps with performance
- other
    - show em how to setup either SSH keys for linux automatic login in github or credential storage in Windows 
    - we might want to use only one branch, and everyone has a differetn file, line HW2_l, HW2_m, HW2_p, and we combine them together, and push the final version only to the main branch
'''



# euclidean distance function
# copied from the prof
def euclidean(point1, point2):
    res = 0
    for i in range(len(point1)):
        diff = (point1[i]-point2[i])
        res += diff*diff
    return math.sqrt(res)


def compute_rmin(points):
    #jesus christ
    rmin = math.inf
    for point1 in points:
        for point2 in points:
            if point1 != point2:
                dist=euclidean(point1, point2)
                if dist < rmin:
                    rmin = dist
    return rmin/2



def SeqWeightedOutliers(points, weights, k, z, alpha):
    '''
    r ← (min distance between first k + z + 1 points)/2
    # this init for rmin confuses me, i'll skip it
    
    while (true) do
    # so until we reach a good result
        Z ← P
        S ← ∅
        WZ = ∑ x ∈ P w(x)
        # init values for this loop
        while ((| S | < k) AND (WZ > 0)) do
            # internal loop for this value of r
            max ← 0
            foreach x ∈ P do
                ball-weight ← ∑ y ∈ BZ(x, (1+2α)r) w(y)
                if (ball-weight > max) then
                    max ← ball-weight
                    newcenter ← x
        # so we compute the ball weight for all points and choose the one that maximises the weight inside the ball
            S ← S ∪{newcenter}
            foreach(y ∈ BZ(newcenter, (3 + 4α)r)) do
                remove y from Z
                subtract w(y) from WZ
            # add it to the centers and remove the points that are inside the ball
        if (WZ ≤ z) then 
            return S
            #termination condition
        else r ← 2r
        # we raise r
        '''
    iteration = 0
    r_min = compute_rmin(points.copy()[k+z+1:])
    r=r_min
    solution = {}
    free_points = []
    free_points_weight = sum(weights)
    while True and iteration < 100:
        iteration += 1
        print("ITER: ", iteration)
        print("R: ", r)
        free_points = points.copy()
        free_weights = weights.copy()
        solution = {}
        free_points_weight = sum(free_weights) 
        inside_iter = 0
        while (len(solution) < k) and (free_points_weight > 0):
            inside_iter += 1
            maxim = 0
            new_center = None
            for point in free_points:
                ball_weight = compute_ball_weight(
                    point, free_points, free_weights, r, alpha)
                if ball_weight > maxim:
                    maxim = ball_weight
                    new_center = point
            solution[new_center] = []

            del free_weights[free_points.index(new_center)]
            free_points.remove(new_center)
            new_points = free_points.copy()
            for point in new_points:
                distance = euclidean(new_center, point)
                if distance < (3+4*alpha)*r:
                    i = new_points.index(point)
                    free_weights[i] = 0
                    free_points.remove(point)
                    solution[new_center].append(point)
            free_points_weight = sum(free_weights)
        if free_points_weight <= z:
            return solution, r_min, r, iteration
        else:
            r = 2*r

def ComputeObjective(inputPoints, solution, z):
    max_value = 0
    for cluster in solution.keys():
        for points in solution[cluster]:
            distance = euclidean(cluster, points)
            max_value = max(distance, max_value)
    return max_value

def compute_ball_weight(center, free_points, free_weights, r, alpha):
    #inefficent, precomputer distances are probably better
    ball_weight = 0
    iteration = 0
    for point in free_points:
        distance = euclidean(center, point)
        if distance < (1+2*alpha)*r:
            ball_weight += free_weights[iteration]
        iteration+=1
    return ball_weight


def main():
    #declare variables

    filename = "Homework2/testdataHW2.csv"
    k = 3
    z = 0
    alpha = 0

    
    # read file data
    with open(filename) as csv_file:
        csv_data = csv.reader(csv_file)
        inputPoints = []
        weights = []
        for line in csv_data:
            inputPoints.append((float(line[0]), float(line[1])))
            weights.append(1)
    start = time()
    solution, rmin, r, n_iters = SeqWeightedOutliers(inputPoints, weights, k, z, 0)
    diff = time() - start
    objective = ComputeObjective(0, solution, 0)

    # output as required
    print("input size n = ", len(inputPoints))
    print("Number of centers k = ", k)
    print("Number of outliers z = ", z)
    print("Initial guess = ", rmin) 
    print("Final guess = ", r)
    print("Number of guesses = ", n_iters)
    print("Objective function = ", objective)  # ok idk
    print("Time of SeqWeightedOutliers = ", diff * 1000) # ok we need time.time

    #need to visualize the results
    fig, ax = plt.subplots(figsize=(8,8))
    input_points_x = []
    input_points_y = []
    for point in inputPoints:
        input_points_x.append(point[0])
        input_points_y.append(point[1])

    ax.scatter(input_points_x, input_points_y)

    solution_x = []
    solution_y = []    
    for center in solution.keys():
        solution_x.append(center[0])
        solution_y.append(center[1])
        circle = Ellipse((center[0], center[1]), width=3*r, height=3*r,facecolor=None, edgecolor="green")
        ax.add_patch(circle)

    ax.scatter(solution_x, solution_y, c="red")


    plt.show()




if __name__=="__main__":
    main()
