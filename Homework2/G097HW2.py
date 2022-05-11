import os
import math
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from time import time
import argparse
import itertools


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
    while True:
        iteration += 1
        print("iter ", iteration)
        print("r ", r)
        solution = {}
        tmp_points = points.copy()
        tmp_weights = weights.copy()
        free_points_weight = sum(tmp_weights)
        # free_points is now a list of touples that contain both weight and position, so non more two lists
        free_points = list(zip(tmp_points, tmp_weights))
        inside_iter = 0
        while (len(solution) < k) and (free_points_weight > 0):
            inside_iter += 1
            maxim = -1
            new_center = None
            for point, weight in free_points:
                ball_weight = compute_ball_weight(
                    point, free_points, r, alpha)
                if ball_weight > maxim:
                    maxim = ball_weight
                    new_center = point 
                    new_center_weight = weight
            solution[new_center] = []
            free_points.remove((new_center, new_center_weight))
            free_points_weight -= new_center_weight
            new_points = free_points.copy()
            for point, weight in new_points:
                distance = euclidean(new_center, point)
                if distance <= (3+(4*alpha))*r:
                    solution[new_center].append(point)
                    free_points.remove((point, weight))
                    free_points_weight -= weight
        if free_points_weight <= z:
            print("Initial guess = ", r_min)
            print("Final guess = ", r)
            print("Number of guesses = ", iteration)
            return solution
        else:
            r = 2*r

def ComputeObjective(inputPoints, solution, z):
    max_value = 0
    for cluster in solution.keys():
        for points in solution[cluster]:
            distance = euclidean(cluster, points)
            max_value = max(distance, max_value)
    return max_value

def compute_ball_weight(center, free_points, r, alpha):
    #inefficent, precomputer distances are probably better
    ball_weight = 0
    for point, weight in free_points:
        distance = euclidean(center, point)
        if distance <= (1+(2*alpha))*r:
            ball_weight += weight
    return ball_weight


def argument_parser():  # description of the program and command line arguments
    parser = argparse.ArgumentParser(
        description="Homewroks 2 for Group 097 - ann implementation of KcenterOUT for k center clustering with outliers")
    parser.add_argument("-f", dest="filename",
                        help="Filename of .csv data to compute. Defaults to Homework2/testdataHW2.csv", default="Homework2/testdataHW2.csv")
    parser.add_argument("-k", dest="k",
                    help="max value for number of centers. Defaults to 3", default=3, type=int)
    parser.add_argument("-z", dest="z",
                        help="Number of outliers. Defaults to 0", default=0, type=int)
    parser.add_argument("-alpha", dest="alpha",
                    help="added component for the radius of the ball. Defaults to 0", default=0,
                        type=int)
    return vars(parser.parse_args())

def reshape_solution(prev_solution):
    solution = []
    for key in prev_solution.keys():
        solution.append(key)
    return solution

def main():
    #declare variables
    args = argument_parser()  # command line arguments
    if args:
        filename, k, z, alpha = args["filename"], args["k"], args["z"], args["alpha"]
    else:
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
    #moved output around to have a less confusing return
    print("input size n = ", len(inputPoints))
    print("Number of centers k = ", k)
    print("Number of outliers z = ", z)
    start = time()
    # now some printing is done inside SeqWeightedOutliers as it makes for a cleaner return
    solution = SeqWeightedOutliers(inputPoints, weights, k, z, alpha)
    diff = time() - start
    objective = ComputeObjective(0, solution, 0)
    solution = reshape_solution(solution)
    # output remaning values
    print("Objective function = ", objective) 
    print("Time of SeqWeightedOutliers = ", diff * 1000)

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
    for center in solution:
        solution_x.append(center[0])
        solution_y.append(center[1])
        #circle = Ellipse((center[0], center[1]), width=3*r, height=3*r,facecolor=None, edgecolor="green")
        #ax.add_patch(circle)

    ax.scatter(solution_x, solution_y, c="red")


    #plt.show()




if __name__=="__main__":
    main()
