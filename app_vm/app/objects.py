"""
    Data object
    Controls passing of data from image detector to solver and main

    Data types required
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
                    (m-1)*2+1x(n-1)*2+1 shape

                    4 zeros make 1 dot
                    1 2 =>      1
                    4 3     4       2
                                3

                    4x5 ex => 6x9
                            m
                    n
                    - 0 - 0 - 0 - 0 -
                    - 0 0 0 0 0 0 0 0
                    0 0 0 0 0 0 0 0 0
                    0 0 0 0 0 0 0 0 0
                    0 0 0 0 0 0 0 0 0
                    0 0 0 0 0 0 0 0 0
                    0 0 0 0 0 0 0 0 0
                    0 0 0 0 0 0 0 0 0

                    0 0 0 0 - 
                    0 0 0 0 0
                    0 0 0 0 -
                    0 0 0 0 0
                    0 0 0 0 -

                    0 0 0 0 0
                    0 0 0 0 0
                    0 0 0 0 0
                    - 0 - 0 -

                Fixed points
                    mxn matrix
                        0 for unknown
                        1 for fixed
                        2+ for number of possibilities
                        -1 for empty (necessary? can get empty from other)

