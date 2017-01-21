import numpy as np

class Data_storage:

    """
        Data Object
        Controls passing of data from image detector to solver and main

        Data Members
            Shape type at location
                mxn matrix with values 0-5
                    0: Empty space
                    1: Shape with 1
                    2: Shape with 2 curved
                    3: Shape with 2 straight
                    4: Shape with 3
                    5: Shape with 4
            Required Points
                Not points, lines
                    Line counter for an mxn matrix
                        m*2+1xn+1 shape

                        4 zeros make 1 dot
                        1 2 =>      1
                        4 3     4       2
                                    3
                        1: m, n*2
                        2: m+1, n*2+1
                        3: m, n*2+2
                        4: m, n*2+1

                    Spaces are holes, 0's are lines, x's are edges, ? is undef
                     x x x x ?
                    x 0 0 0 x
                     0 0 0 0 ?
                    x 0 0 0 x
                     0 0 0 0 ?
                    x 0 0 0 x
                     x x x x ?

                    

                    Fixed points
                        mxn matrix
                            0 for unknown
                            1 for fixed
                            2+ for number of possibilities
                            -1 for empty (necessary? can get empty from other)
    """

    def set_size(self,m,n):
        """
        Input: Integer m (x) length of grid
        Input: Integer n (y) length of grid

        """
        self.shape_matrix = np.zeros((m,n))
        self.required_points = np.zeros((m*2+1,n+1))
        self.fixed_points = np.zeros((m,n))

    # -1 == edge of grid
    # -9 == artifact of data storage => ignore
    # 0 == unknown
    # 1 == fixed
    def setup_required_matrix(self):
        for i in range(self.required_points.shape[0]):
            for j in range(self.required_points.shape[1]):
                if i == 0 or i == self.required_points.shape[0]-1:
                    if j == self.required_points.shape[1]-1:
                        self.required_points[i,j] = -9
                    else:
                        self.required_points[i,j] = -1
                elif i % 2 == 1:    #odd rows
                    if j == 0 or j == self.required_points.shape[1]-1:
                        self.required_points[i,j] = -1
                elif j == self.required_points.shape[1]-1: #even rows
                    self.required_points[i,j] = -9
