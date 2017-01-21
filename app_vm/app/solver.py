import numpy as np
import objects
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

def solve(data_object):
    # Steps
    # 1. init req. matrix correctly => moved to obj
    data_object.setup_required_matrix()
    print data_object.required_points
