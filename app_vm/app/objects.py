import numpy as np
import time

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

        if a == 1:
            self.required_points[x*2,y] = value
        if b == 1:
            self.required_points[x*2+1,y+1] = value
        if c == 1:
            self.required_points[x*2+2,y] = value
        if d == 1:
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

    def search_neighbors(self,x,y):
        """
        Helper function to find neighboors from required matrix

        Input: Integer x coordinate
        Input: Integer y coordinate

        Output: 1x4 matrix of neighboring points in the required matrix object
        Output: 1x4 matrix of indexes with positive points
        Output: 1x4 matrix of indexes with negative points
        Output: 1x4 matrix of indexes with zero points

        """
        output = np.zeros(4)
        output[0] = self.required_points[x*2,y]
        output[1] = self.required_points[x*2+1,y+1]
        output[2] = self.required_points[x*2+2,y]
        output[3] = self.required_points[x*2+1,y]

        pos_neigh = np.where(output == 1)[0]
        neg_neigh = np.where(output == -1)[0]
        zero_neigh = np.where(output == 0)[0]

        return output,pos_neigh,neg_neigh,zero_neigh

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
        the fixed points matrix.

        Input: Integer x value
        Input: Integer y value
        Input: Integer value to set fixed points to (should be 0 or 1)

        """

        self.fixed_points[x,y] = value
        # Different values set to fixed impact the required points matrix in
        # different ways
        if value == 1:
            # If fixed is 1, updated required matrix using the surrounding 
            # required values to see what other required values can be set

            # What follows is a huge ugly and inelegant switch statement with
            # the same basic structure
            # 1. Find neighboors
            # 2. If enough positive required lines = 4-shape num (along with
            #       some bordering conditions), set other lines as negative
            #       required
            # 3. If enough negative required lines = 4-shape num (along with
            #       some bordering conditions), set other lines as positive
            #       required
            # This could be replaced with a carefully designed switch
            neighbors, pos_fixed, neg_fixed, zero_fixed = \
                self.search_neighbors(x,y)

            if self.shape_matrix[x,y] == 1:
                # For pos fixed
                # Iff there are 3 required lines bordering the cell
                # set the other line as non_req
                if len(pos_fixed) == 1:
                    neg_neighbors = (neighbors - 1)*-1 # if point is fixed,
                    # some all other grids set as pos_required
#                    print "Neg neighbors: "+str(x)+" "+str(y)
#                    print neg_neighbors
                    self.set_required_points((x,y), neg_neighbors[0],
                            neg_neighbors[1], neg_neighbors[2],
                            neg_neighbors[3], -1)
                # For neg fixed
                # Iff there are 3 non_required lines bordering the cell
                # set the other line as req 
                elif len(neg_fixed) == 3:
                    pos_neighbors = neighbors + 1 # if point is fixed,
                    # set all other grids set as pos_required
                    self.set_required_points((x,y), pos_neighbors[0],
                            pos_neighbors[1], pos_neighbors[2],
                            pos_neighbors[3], 1)
                else:
                    print "Fixed but no updates! 1"

            elif self.shape_matrix[x,y] == 2:
                # For pos fixed
                # Iff there are 2 required lines bordering the cell and they're
                # next to each other, set the other grids as non_req
                if len(pos_fixed) == 2 and (abs(pos_fixed[0] - pos_fixed[1])\
                        == 1 or abs(pos_fixed[0]-pos_fixed[1]) == 3):
                    neg_neighbors = (neighbors - 1)*-1 # if point is fixed,
                    # set all other grids set as neg_required
                    self.set_required_points((x,y), neg_neighbors[0],
                            neg_neighbors[1], neg_neighbors[2],
                            neg_neighbors[3], -1)

                # For neg fixed
                # Iff there are 2 non_required lines bordering the cell and
                # they're next to each other, set the other grids as req
                elif len(neg_fixed) == 2 and (abs(neg_fixed[0] - neg_fixed[1])\
                        == 1 or abs(neg_fixed[0]-neg_fixed[1]) == 3):
                    pos_neighbors = neighbors + 1 # if point is fixed,
                    # set all other grids set as pos_required
                    self.set_required_points((x,y), pos_neighbors[0],
                        pos_neighbors[1], pos_neighbors[2],
                        pos_neighbors[3], 1)

                # For 1 neg and 1 postive
                elif len(pos_fixed) == 1 and len(neg_fixed) == 1:
                    if abs(pos_fixed[0] - neg_fixed[0]) == 1 or\
                    abs(pos_fixed[0] - neg_fixed[0]) == 3:
                        index = pos_fixed[0] - neg_fixed[0]
                        loc_pos = pos_fixed[0]+index
                        loc_neg = neg_fixed[0]-index
                        if loc_neg > len(neighbors)-1:
                            loc_neg = loc_neg - 4
                        if loc_pos > len(neighbors)-1:
                            loc_pos = loc_pos - 4
                        
                        # If x is >0 loops around in array
                        pos_neighbors = np.copy(neighbors)
                        neg_neighbors = np.copy(neighbors)
                        pos_neighbors[loc_pos] = 1 
                        neg_neighbors[loc_neg] = -1
                        neg_neighbors = (neg_neighbors)*-1
                        self.set_required_points((x,y), pos_neighbors[0],
                            pos_neighbors[1], pos_neighbors[2],
                            pos_neighbors[3], 1)
                        self.set_required_points((x,y), neg_neighbors[0],
                            neg_neighbors[1], neg_neighbors[2],
                            neg_neighbors[3], -1)
                    else:
                        print "ERROR:(",str(x),",",str(y),"):",\
                                str(self.shape_matrix[x,y])

                else:
                    print "Fixed but no updates! 2"
                    print str(x) + ", " + str(y) + ": " + str(pos_fixed) +\
                    "\t"+str(neg_fixed)

            elif self.shape_matrix[x,y] == 3:
                # For pos fixed
                # Iff there are >= 1 required lines bordering the cell set,
                # the other grids as non_req
                if len(pos_fixed) >= 1:
                    # If only one grid was required, set opposite to required
                    if len(pos_fixed) == 1:
                        index = pos_fixed[0] + 2
                        if index > len(neighbors)-1:
                            index = index - 4
                        neighbors[index] = 1
                        # Update neighbors with new value
                        self.set_required_points((x,y), neighbors[0], 
                            neighbors[1], neighbors[2], neighbors[3], 1)
                    neg_neighbors = (neighbors - 1)*-1 # if point is fixed,
                    # set all other grids set as neg_required
                    self.set_required_points((x,y), neg_neighbors[0],
                            neg_neighbors[1], neg_neighbors[2],
                            neg_neighbors[3], -1)

                # For neg fixed
                # Iff there are >= 1 non_required lines bordering the cell,
                # set the other grids as req
                elif len(neg_fixed) >= 1:
                    # If only one grid was required, set opposite to required
                    if len(neg_fixed) == 1:
                        index = neg_fixed[0] + 2
                        if index > len(neighbors)-1:
                            index = index - 4
                        neighbors[index] = -1
                        # Update neighbors with new value
                        # Needs to use negative neighbors for -1 values to mark
                        # true
                        self.set_required_points((x,y), neighbors[0]*-1, 
                            neighbors[1]*-1, neighbors[2]*-1, neighbors[3]*-1,
                            -1)
                    pos_neighbors = neighbors + 1 # if point is fixed,
                    # set all other grids set as pos_required
                    self.set_required_points((x,y), pos_neighbors[0],
                            pos_neighbors[1], pos_neighbors[2],
                            pos_neighbors[3], 1)

                else:
                    print "Fixed but no updates! 3"

            elif self.shape_matrix[x,y] == 4:
                # For pos fixed
                # Iff there is 1 required line bordering the cell, set the 
                # other grids as non_req
                if len(pos_fixed) == 3:
                    neg_neighbors = (neighbors - 1)*-1 # if point is fixed,
                    # set all other grids set as neg_required
                    self.set_required_points((x,y), neg_neighbors[0],
                            neg_neighbors[1], neg_neighbors[2],
                            neg_neighbors[3], -1)

                # For neg fixed
                # Iff there is 1 non_required line bordering the cell, set the 
                # other grids as req
                elif len(neg_fixed) == 1:
                    pos_neighbors = neighbors + 1 # if point is fixed,
                    # set all other grids set as pos_required
                    self.set_required_points((x,y), pos_neighbors[0],
                            pos_neighbors[1], pos_neighbors[2],
                            pos_neighbors[3], 1)

                else:
                    print "Fixed but no updates!"

            elif self.shape_matrix[x,y] == 5:
                self.set_required_points((x,y), 1, 1, 1, 1, 1)
                #neighbors not neeeded, all need to be pos fixed

            elif self.shape_matrix[x,y] == 0:
                self.set_required_points((x,y), 1, 1, 1, 1, -1)
                #neighbors not neeeded, all need to be neg fixed

            else:
                print "Error: Invalid shape value cannot be fixed"
                pass

        else:
            "Error: Value is not defined"
