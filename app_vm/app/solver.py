import numpy as np
import objects

def set_required_points(point, a, b, c, d, data_storage):
    """
    Set required points in object

    Input: Tuple point to be set
    Input: Bool if point 1 is required
    Input: Bool if point 2 is required
    Input: Bool if point 3 is required
    Input: Bool if point 4 is required
    Input: Data_storage object to set points

    """
    x = point[0]; y = point[1]
    if a:
        data_storage.required_points[y*2,x] = 1
    if b:
        data_storage.required_points[y*2+1,x+1] = 1
    if c:
        data_storage.required_points[y*2+2,x] = 1
    if d:
        data_storage.required_points[y*2+1,x] = 1

def get_required_points(m,n,data_storage):
    """
    Get shape from required points coordinates

    Input: Integer m coordinate
    Input: Integer n coordinate
    Input: Data_storage object to get points from
    Output: Array of Tuples with the grid spaces boarding the req. lines
            Either veritically touching or horizontally touching
            Either length two or length one

    """
    if m % 2: #if m is even
        pass    #do something


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
    for i in locations_5:
        data_object.fixed_points[i[1],i[0]] = 1
        set_required_points(i,1,1,1,1,data_object)

"""
    # corners
    corners = storage.shape_matrix[[0,0,-1,-1],[0,-1,0,-1]]
    if 

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
"""
