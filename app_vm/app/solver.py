import numpy as np
import time
import sys

import objects

def solve(data_object):
    """
    Problem solver functions

    Tasks completed
        Read in object with data
        Solve problem
            Iterate over data with several passes
                Set fixed points
                ID && Update required locations
                    Both postive and negative
                    Required here, required not here
                Repeat until all points fixed
                    But what about furcations?
    """

    # Steps
    # 1. init req. matrix correctly => moved to obj
    data_object.setup_required_matrix()

    # 2. ID fixed points at start
    # shape 5 means all points around it are required
    locations_5 = np.where(data_object.shape_matrix == 5)
    for i in range(len(locations_5[0])):
        data_object.set_fixed_points(locations_5[0][i], locations_5[1][i], 1)
    # shape 0 means all points around it are neg required
    locations_0 = np.where(data_object.shape_matrix == 0)
    for i in range(len(locations_0[0])):
        data_object.set_fixed_points(locations_0[0][i], locations_0[1][i], 1)

    # corners - shape 2 only
    corners = data_object.shape_matrix[tuple(slice(None, None, j-1) for j in
        data_object.shape_matrix.shape)] # 4x4 matrix
    locations_corners = np.where(corners == 2)
    shape = data_object.shape_matrix.shape
    for i in range(len(locations_corners[0])):
        if locations_corners[0][i] != 0:
            locations_corners[0][i] = shape[0] - locations_corners[0][i]
        if locations_corners[1][i] != 0:
            locations_corners[1][i] = shape[1] - locations_corners[1][i]
        # need to convert the corner locations to matrix locations
        data_object.set_fixed_points(locations_corners[0][i], 
                locations_corners[1][i], 1)

    # edges - shapes 3 and 4 only
    locations_edges = []
    shape = data_object.shape_matrix.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i == 0 or i == shape[0]-1 or j == 0 or j == shape[1]-1:
                if data_object.shape_matrix[i,j] == 3 or \
                data_object.shape_matrix[i,j] == 4:
                    data_object.set_fixed_points(i,j, 1)

    # 3. from required points generate fixed points
    # while fixed_points != 1
    counter = 0
    while np.any(data_object.fixed_points-1):
        sys.stderr.write("\x1b[2J\x1b[H")
        print "Pass # ",counter
        for i,item in enumerate(data_object.required_points):
            if i % 2 == 0:
                print " ",item
            elif i % 2 == 1:
                print item
        print data_object.fixed_points
        not_fixed = np.where(data_object.fixed_points != 1)
        for i in range(len(not_fixed[0])):
            m = not_fixed[0][i]
            n = not_fixed[1][i]
#            print "Working on cell (" + str(m) +  "," + str(n) + ")"
            shape_type = data_object.shape_matrix[m,n]
            neighbors = data_object.search_neighbors(m,n)
            pos_required = np.where(neighbors == 1)[0]
            neg_required = np.where(neighbors == -1)[0]

            if shape_type == 1:
                # For pos required
                if len(pos_required) == 1:
                    data_object.set_fixed_points(m, n, 1)
                # For neg required
                if len(neg_required) == 3:
                    data_object.set_fixed_points(m, n, 1)

            elif shape_type == 2:
                # For pos required
                if len(pos_required) == 2 and (abs(pos_required[0] -
                        pos_required[1]) == 1 or abs(pos_required[0] -
                            pos_required[1]) == 3):
                    data_object.set_fixed_points(m, n, 1)
                # For neg required
                if len(neg_required) == 2 and (abs(neg_required[0] -
                        neg_required[1]) == 1 or abs(neg_required[0] -
                            neg_required[1]) == 3):
                    data_object.set_fixed_points(m, n, 1)

            elif shape_type == 3:
                # For pos required
                if len(pos_required) >= 1:
                    data_object.set_fixed_points(m, n, 1)
                # For neg required
                if len(neg_required) >= 1:
                    data_object.set_fixed_points(m, n, 1)

            elif shape_type == 4:
                # For pos required
                if len(pos_required) == 3:
                    data_object.set_fixed_points(m, n, 1)
                # For neg required
                if len(neg_required) == 1:
                    data_object.set_fixed_points(m, n, 1)

                pass
            elif shape_type == 5 or shape_type == 0:
                print "Error: Shape type ",shape_type," should have been solved previously"
            else:
                print "Error: Invalid shape value cannot be solved"

        time.sleep(0.5)
        counter += 1

