import numpy as np
import cv2
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
    stuck_counter = 0
    while np.any(data_object.fixed_points-1):
        if stuck_counter == 3:
            print "STUCK - Need to guess"
            break

        sys.stderr.write("\x1b[2J\x1b[H")
        print "Pass # ",counter
        for i,item in enumerate(data_object.required_points):
            if i % 2 == 0:
                print " ",item
            elif i % 2 == 1:
                print item
        print data_object.fixed_points
        not_fixed = np.where(data_object.fixed_points != 1)
        last_pass = np.copy(data_object.required_points)
        for i in range(len(not_fixed[0])):
            m = not_fixed[0][i]
            n = not_fixed[1][i]
#            print "Working on cell (" + str(m) +  "," + str(n) + ")"
            shape_type = data_object.shape_matrix[m,n]
            neighbors = data_object.search_neighbors(m,n)
            pos_required = np.where(neighbors == 1)[0]
            zero_required = np.where(neighbors == 0)[0]
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
                if len(neg_required) == 2 and (abs(neg_required[0] -\
                        neg_required[1]) == 1 or abs(neg_required[0] -\
                        neg_required[1]) == 3):
                  data_object.set_fixed_points(m, n, 1)
                # For both
                if len(pos_required) == 1 and len(neg_required) == 1:
                    if abs(pos_required[0] - neg_required[0]) == 1 or \
                        abs(pos_required[0] - neg_required[0]) == 3:
                        data_object.set_fixed_points(m, n, 1)

                # For one neg 
                if len(pos_required) == 0 and len(neg_required) == 1:
                    pos_neighbors = neg_required
                    index = neg_required[0] + 2
                    if index > len(neighbors)-1:
                        index = index - 4
                    neighbors[index] = 1
                    data_object.set_required_points((m, n), neighbors[0], 
                            neighbors[1], neighbors[2], 
                            neighbors[3], 1)

                # For one pos 
                if len(neg_required) == 0 and len(pos_required) == 1:
                    pos_neighbors = pos_required
                    index = pos_required[0] + 2
                    if index > len(neighbors)-1:
                        index = index - 4
                    neighbors[index] = -1
                    neighbors = neighbors * -1
                    data_object.set_required_points((m, n), neighbors[0], 
                            neighbors[1], neighbors[2], 
                            neighbors[3], -1)

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

            elif shape_type == 5 or shape_type == 0:
                print "Error: Shape type ",shape_type," should have been solved previously"
            else:
                print "Error: Invalid shape value cannot be solved"

        current_pass = np.copy(data_object.required_points)
        counter += 1
        if np.array_equal(current_pass,last_pass):
            stuck_counter += 1

    print "SOLVED"

def check(data_object):
    """
    Check that the puzzle was solved correctly, and display the solved puzzle
    as an image.

    Current only checks that all required points are set and work for the shape
    type.

    Input: Data_object item

    """

    #Checking
    fixed_location = np.where(data_object.fixed_points == 1)
    template_path = "/home/joseph/scratch/CV/app_vm/data/templates/inf_loop_1_1.png"
    template = cv2.imread(template_path)
    print template
    (tH, tW) = template.shape[:2]
    image_shape = data_object.fixed_points.shape
    image_out = np.zeros((tH*image_shape[0], tW*image_shape[1],3), np.uint8)
    image_out += 255
    for i in range(len(fixed_location[0])):
        m = fixed_location[0][i]
        n = fixed_location[1][i]
        shape_type = data_object.shape_matrix[m,n]
        neighbors = data_object.search_neighbors(m,n)
        pos_neighbors = np.where(neighbors == 1)[0]
        neg_neighbors = np.where(neighbors == -1)[0]
        if np.where(neighbors == 0)[0] != 0:
            print "Required point not set at (",str(m),",",str(n),")"
            break

        if shape_type == 1:
            if len(pos_neighbors) != 1 or len(neg_neighbors) != 3:
                print "Incorrect state at (",str(m),",",str(n),")"
            else:
                print "Point (",str(m),",",str(n),") correct"
        elif shape_type == 2:
            # Lsb should be 1 for neighboring points (ie base num 3 or 1)
            if len(pos_neighbors) != 2 or len(neg_neighbors) != 2 or\
                abs(pos_neighbors[0] - pos_neighbors[1]) & 0b1 != 1:
                print "Incorrect state at (",str(m),",",str(n),")"
            else:
                print "Point (",str(m),",",str(n),") correct"
        elif shape_type == 3:
            # Lsb should be 1 for neighboring points (ie base num 4 or 2)
            if len(pos_neighbors) != 2 or len(neg_neighbors) != 2 or\
                abs(pos_neighbors[0] - pos_neighbors[1]) & 0b1 != 0:
                print "Incorrect state at (",str(m),",",str(n),")"
            else:
                print "Point (",str(m),",",str(n),") correct"
        elif shape_type == 4:
            if len(pos_neighbors) != 3 or len(neg_neighbors) != 1:
                print "Incorrect state at (",str(m),",",str(n),")"
            else:
                print "Point (",str(m),",",str(n),") correct"
        elif shape_type == 5:
            if len(pos_neighbors) != 4:
                print "Incorrect state at (",str(m),",",str(n),")"
            else:
                print "Point (",str(m),",",str(n),") correct"

    #Displaying
        image_type = "/home/joseph/scratch/CV/app_vm/data/templates/"
        if shape_type == 1:
            if neighbors[3] == 1:
                #1_1
                image_type += "inf_loop_1_1.png"
            elif neighbors[0] == 1:
                #1_2
                image_type += "inf_loop_1_2.png"
            elif neighbors[1] == 1:
                #1_3
                image_type += "inf_loop_1_3.png"
            elif neighbors[2] == 1:
                image_type += "inf_loop_1_4.png"
                #1_4
        elif shape_type == 2:
            if neighbors[3] == 1 and neighbors[2] == 1:
                #2_1
                image_type += "inf_loop_2_1.png"
            elif neighbors[0] == 1 and neighbors[3] == 1:
                #2_2
                image_type += "inf_loop_2_2.png"
            elif neighbors[0] == 1 and neighbors[1] == 1:
                #2_3
                image_type += "inf_loop_2_3.png"
            elif neighbors[2] == 1 and neighbors[1] == 1:
                #2_4
                image_type += "inf_loop_2_4.png"
        elif shape_type == 3:
            if neighbors[1] == 1:
                #3_1
                image_type += "inf_loop_3_1.png"
            elif neighbors[0] == 1:
                #3_2
                image_type += "inf_loop_3_2.png"
        elif shape_type == 4:
            if neighbors[3] == -1:
                #4_1
                image_type += "inf_loop_4_1.png"
            elif neighbors[0] == -1:
                #4_2
                image_type += "inf_loop_4_2.png"
            elif neighbors[1] == -1:
                #4_3
                image_type += "inf_loop_4_3.png"
            elif neighbors[2] == -1:
                #4_4
                image_type += "inf_loop_4_4.png"
        elif shape_type == 5:
            #5_1
            image_type += "inf_loop_5_1.png"

        if shape_type == 0:
            image_type = np.zeros((tH,tW,3),np.uint8)
            image_type += 255
        else:
            image_type = cv2.imread(image_type)
        current_loc = (m * tH, n * tW)
        image_out[current_loc[0]:current_loc[0]+tH, current_loc[1]:current_loc[1]+tW] = image_type

    cv2.namedWindow("output",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("output",400,600)
    cv2.imshow("output",image_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
