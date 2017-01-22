import numpy as np
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

    # corners
    corners = storage.shape_matrix[[0,0,-1,-1],[0,-1,0,-1]] # 4x4 matrix
    locations_corners = np.where(corners == 2)
    for i in range(len(locations_corners[0])):
        data_object.set_fixed_points(locations_corners[0][i], locations_corners[1][i], 1)
    

    data_objects.shape_matrix
    # find shapes at corners
    if data_object.shape_matrix[0,0] == 2:
        data_object.fixed_points[0,0] = 1
        set_required_points(i,0,1,1,0,data_object) 
    if data_object.shape_matrix[0,-1] == 2:
        data_object.fixed_points[0,-1] = 1
        set_required_points(i,0,0,1,1,data_object) 
    if data_object.shape_matrix[-1,-1] == 2:
        data_object.fixed_points[-1,-1] = 1
        set_required_points(i,1,0,0,1,data_object) 
    if data_object.shape_matrix[-1,0] == 2:
        data_object.fixed_points[-1,0] = 1
        set_required_points(i,1,1,0,0,data_object) 
                                                   

    # edges means depending on shape and surroundings, points required


    for i in range(data_object.required_points.shape[0]):
        for j in range(data_object.required_points.shape[1]):
            pass
