# %load ../project/ant.py
# %load ../project/ant.py
#!/usr/bin/env python3



import numpy as np

import os

# Ants are the agents that perform the walks on the problem graph
# attributes:
    # size: number of cities
    # cities: array of indices of the cities
    # tour: array of cities in the order in which they were visited, returning to the starting point
    # tourlength: length of the tour as sum of distances in km
    # choices: array of probabilities with which a certain city will be chosen as the next to visit
    # candidate: bool, true if this ant's tour is a candidate for the optimal tour
class Ant:
    
    def __init__(self, problemsize):
        self.size = problemsize
        self.cities = np.arange(problemsize)
        self.tour = np.zeros(problemsize, 'i4')
        self.tourlength = 0
        self.choices = np.zeros(problemsize, 'f8')
        self.candidate = False
        
    
    # choose the next city to visit, given the current position and all probabilities  
    # TODO: WITH MASK, COPY WHEN DIVIDING
    def choosenext(self, position, probmatrix):
        self.choices = np.copy(probmatrix[position, :]) # copy row of position
        self.choices[self.tour] = 0. # set to 0 all probabilities referring to cities already visited
        s = self.choices.sum()
        self.choices /= s #DO copy here!!
        #return np.random.choice(self.cities, size=None, replace=True, p = self.choices) --> SLOW
        return np.random.multinomial(1,self.choices).argmax()
    
    # perform a walk on the graph, beginning and ending at position start
    # IN: start, current best tourlength, matrix of all distances, matrix of all probabilities
    def walk(self, start, currentbest, distmatrix, probmatrix):
        self.tourlength = 0
        self.tour = np.zeros(self.size, 'i4')
        i = start
        self.tour[0] = i # add city start to tour
        for k in range(1, self.size):
            j = self.choosenext(i, probmatrix) # choose next city
            self.tour[k] = j # add city to tour
            self.tourlength += distmatrix[i,j] # calculate traveled distance
            i = j # update current position
            if (self.tourlength > currentbest):
                return #return self.tourlength ?# stop if the tourlength exceeds current best tour before all cities are visited
        self.tourlength += distmatrix[j,start] # add distance of the return to start
        if (self.tourlength >= currentbest):
                return self.tourlength # if tourlength exceeds current best tour, it is not a candidate
        self.candidate = True
        return self.tourlength
    
    # given a known solution tour, perform the walk to calculate the length
    def solutionwalk(self, solution, distmatrix):
        self.tour = np.zeros(self.size, 'i4')
        self.tourlength = 0
        i = solution[0]
        for j in solution[1:]:
            self.tourlength += distmatrix[i,j]
            i=j
        self.tourlength += distmatrix[solution[-1], solution[0]]
        return self.tourlength
    
    # def naivewalk(self, distmatrix):
    #     randsol = np.random.permutation(self.size)
    #     self.tour = np.zeros(self.size, 'i4')
    #     self.tourlength = 0
    #     i = randsol[0]
    #     self.tour[0] = 0
    #     for j in randsol[1:]:
    #         self.tourlength += distmatrix[i,j]
    #         i=j
    #     self.tourlength += distmatrix[randsol[-1], randsol[0]]
    #     return self.tourlength

    # naivewalk as nearest neighbour tour: greedy solution
    def naivewalk(self, distmatrix):
        self.tour = np.zeros(self.size, 'i4')
        self.tourlength = 0
        self.tour[0] = 0
        i = 0
        for j in range(1, self.size):
            m = np.isin(np.arange(self.size), self.tour) # mask elements already visited
            #print('m: ', m)
            choice = np.ma.masked_array(distmatrix[i,:], m) # array of possible choices 
            #print(choice)
            self.tour[j] = np.argmin(choice) # choose shortest distance greedily
            self.tourlength += distmatrix[i,j]
            i = j
        self.tourlength += distmatrix[j, 0]
        # print('naive tour: ', self.tour)
        return self.tourlength
    
    # reset the ant's attributes to initial values for the next iteration
    def reset(self):
        self.tour = np.zeros(self.size, 'i4')
        self.tourlength = 0
        self.choices = np.zeros(self.size, 'f8')
        self.candidate = False
        
        