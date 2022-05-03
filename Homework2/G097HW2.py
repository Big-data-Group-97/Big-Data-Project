import os
import math
import csv 
import matplotlib.pyplot as plt
import numpy as np

# euclidean distance function
# copied from the prof
def euclidean(point1, point2):
    res = 0
    for i in range(len(point1)):
        diff = (point1[i]-point2[i])
        res += diff*diff
    return math.sqrt(res)



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
    r = 0.5 #bad but idc
    solution = []
    free_points = []
    while True:
        iteration += 1
        free_points = points
        solution = []
        free_points_weight = len(points) # not a full weight implementation
        while (len(solution) < k) and (free_points_weight > 0):
            max = 0
            new_center = None
            for point in free_points:
                ball_weight = compute_ball_weight(
                    point, free_points, r, alpha)
                if ball_weight > max:
                    max = ball_weight
                    new_center = point
            solution.append(new_center)
            free_points.remove(new_center)
            for point in free_points:
                distance = euclidean(new_center, point)
                if distance < (3+4*alpha)*r:
                    free_points.remove(point)
            free_points_weight = len(free_points)
            if free_points_weight < z:
                return solution
            else:
                r = 2*r

def ComputeObjective(inputPoints, solution, z):
    objetive = 0 #not roght now
    return objective

def compute_ball_weight(center, free_points, r, alpha):
    #inefficent, precomputer distances are robbly better
    # does not support weights
    ball_weight = 0
    for point in free_points:
        distance = euclidean(center, point)
        if distance < (1+2*alpha)*r:
            ball_weight += 1
    return ball_weight


def main():
    #declare variables
    filename = "Homework2/uber-small.csv"
    filename = "Homework2/testdataHW2.csv"
    k = 2
    z = 2
    alpha = 0

    print("CWD: ", os.getcwd())
    
    # read file data
    with open(filename) as csv_file:
        csv_data = csv.reader(csv_file)
        inputPoints = []
        weights = []
        for line in csv_data:
            inputPoints.append((float(line[0]), float(line[1])))
            weights.append(1)
    solution = SeqWeightedOutliers(inputPoints, weights, k, z, 0)
    print(solution)
    #need to visualize the results
    fig, ax = plt.subplots(figsize=(8,8), layout='constrained')
    
    ax.scatter(inputPoints, inputPoints)
    plt.show()






if __name__=="__main__":
    main()