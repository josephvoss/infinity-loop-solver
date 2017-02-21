import numpy as np
import copy

import objects

class Guess:

    def __init__(self):
        self.guess_counter = 0
        self.guess_subcounter = 0
        self.guess_subcounter = 0
        self.list_guesses = []
        self.list_unsolvable = []

    def guess(self,storage):
        data_object = storage
        if len(self.list_guesses) == 0:
            self.list_unsolvable = np.where(data_object.fixed_points==0)
        else:
            data_object = copy.deepcopy(self.list_guesses[0])
        self.list_guesses.append(copy.deepcopy(data_object))
        
        m = self.list_unsolvable[0][self.guess_counter]
        n = self.list_unsolvable[1][self.guess_counter]

        # Find all required points not set 
        neighbors, pos_loc, neg_loc, zero_loc  = \
                data_object.search_neighbors(m,n)

        # Guess all reqs for each fixed point
        if self.guess_subcounter > len(zero_loc):
            self.guess_counter += 1
            self.guess_subcounter = 0
        else:
            index = zero_loc[self.guess_subcounter]
            neighbor_fixer = np.zeros(neighbors.shape)
            neighbor_fixer[index] = 1
            data_object.set_required_points((m,n), neighbor_fixer[0],\
                neighbor_fixer[1], neighbor_fixer[2], neighbor_fixer[3], 1)
        print "Post Guess"
        for i,item in enumerate(data_object.required_points):
            if i % 2 == 0:
                print " ",item
            elif i % 2 == 1:
                print item

        return data_object
