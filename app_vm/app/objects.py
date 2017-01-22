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

            Value of 1 means points required here
            Value of -1 means points required not here
            Value of 0 means unknown

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
        self.shape_matrix = np.zeros((m,n),dtype=np.int)
        self.required_points = np.zeros((m*2+1,n+1))
        self.fixed_points = np.zeros((m,n))

    def set_required_points(self, point, a, b, c, d, value):
        """
        Set required points in object

        Input: Tuple point to be set
        Input: Bool if point 1 is required
        Input: Bool if point 2 is required
        Input: Bool if point 3 is required
        Input: Bool if point 4 is required
        Input: Integer for value to be set to (1 for required, -1 for required not)
        Input: Data_storage object to set points

        """
        x = point[0]; y = point[1]
        if a:
            self.required_points[x*2,y] = value
        if b:
            self.required_points[x*2+1,y+1] = value
        if c:
            self.required_points[x*2+2,y] = value
        if d:
            self.required_points[x*2+1,y] = value

    def get_required_points(self,m,n):
        """
        Get shape from required points coordinates

        Input: Integer m coordinate
        Input: Integer n coordinate
        Input: Data_storage object to get points from
        Output: Array of Tuples with the grid spaces boarding the required lines
                Either veritically touching or horizontally touching
                Either length two or length one

        """
        if m % 2: #if m is even
            
            pass    #do something
        else:
            pass


    # -1 == edge of grid
    # -9 == artifact of data storage => ignore
    # 0 == unknown
    # 1 == fixed
    def setup_required_matrix(self):
        """
        Initializes the required points matrix in the notation shown above.
        Needs to be called after set_size

        """
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

    def set_fixed_points(self,x,y,value):
        """
        Wrapper function to set the required points matrix at the same time as
        the fixed points matrix

        Input: Integer x value
        Input: Integer y value
        Input: Integer value to set fixed points to (should be 0 or 1)

        """

        self.fixed_points[x,y] = value
        if value == 1:
            if self.shape_matrix[x,y] == 1:
                #self.set_required_points((x,y), 1, 1, 1, 1, 1)
                pass
            elif self.shape_matrix[x,y] == 2:
                #self.set_required_points((x,y), 1, 1, 1, 1, 1)
                pass
            elif self.shape_matrix[x,y] == 3:
                #self.set_required_points((x,y), 1, 1, 1, 1, 1)
                pass
            elif self.shape_matrix[x,y] == 4:
                #self.set_required_points((x,y), 1, 1, 1, 1, 1)
                pass
            elif self.shape_matrix[x,y] == 5:
                print "Shape 5"
                self.set_required_points((x,y), 1, 1, 1, 1, 1)
                pass
            elif self.shape_matrix[x,y] == 0:
                print "Shape 0"
                self.set_required_points((x,y), 1, 1, 1, 1, -1)
                pass
            else:
                pass

