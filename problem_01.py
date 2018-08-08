# %load ../project/problem.py
#!/usr/bin/env python3
# 
import numpy as np
import os

#from ant import Ant

class Problem:

    # the Problem is a set of coordinates read from file 
    # from which the distances are calculated,
    # plus a set of ants which are applied to finding a solution.
    # attributes:
        # name: identifier of data
        # x,y: coordinates of the cities from the data file
        # size: number of cities in the problem
        # ro, alpha, beta: parameters from the equations for the colony
        # phmax: max amount of pheromone
        # distances, heuristics: (size x size) matrices of distances, heuristic factors calculated from the data
        # currentbest: best result from last iteration
        # pheromones: matrix? of pheromone trails for each edge
        # ants: array of Ants for the Problem
        # bestant: Ant that arrived at currentbest solution in last iteration
    def __init__(self, problemname, ro, alpha, beta):
        self.name = problemname
        self.x, self.y = self.readcoords()
        self.size = self.x.size
        self.ro = ro
        self.alpha = alpha
        self.beta = beta
        self.phmax = 0.9
        self.distances, self.heuristics = self.getmatrices()
        self.currentbest = self.initguess()
        self.pheromones = self.initpheromones()
        self.probabilities = self.pheromones**self.alpha * self.heuristics 
        self.ants = []
        self.bestant = Ant(self.size)
        self.greedytour = np.zeros(self.size)
        



    # find a certain string that denotes start of data in data file
    # OUT: no. of rows to be skipped in file
    def getheader(self, file, string):
        header = 0
        with open(file) as f:
            for line in f:
                header += 1
                if string in line:
                    break
        f.close()
        return header
    
    # go to start of data in data file
    # OUT: no. of rows until node coordinate section starts
    def skiprows(self):
        path = os.getcwd()
        return self.getheader(path + '/ALL_tsp/' + self.name + '.tsp', 'NODE_COORD_SECTION')
    
    # read all coordinates from data file, store in array x and y respectively
    def readcoords(self):
        path = os.getcwd()
        coords = np.genfromtxt(path + '/ALL_tsp/' + self.name + '.tsp',  
                                    skip_header = self.skiprows(), 
                                    skip_footer = 1, 
                                    usecols=(1,2), 
                                    dtype = 'f8')
        x = coords[:,0]
        y = coords[:,1]
        return x, y
    

    # calculate distances between all nodes in data as euclidean distances
    # calculate initial probability matrix as inverse distances to the power of beta 
    # TODO: --> is that right? normalize here? CHECK!!!
    # round distances to integer
    # OUT: matrix of distances, matrix of probabilities
    def getmatrices(self):
        xI, xJ = np.meshgrid(self.x,self.x, sparse=False, indexing='ij')
        yI, yJ = np.meshgrid(self.y,self.y, sparse=False, indexing='ij')
        distmatrix = np.sqrt((xI-xJ)**2 + (yI-yJ)**2)
        probmatrix = np.divide(1, distmatrix, out=np.zeros_like(distmatrix), where=distmatrix!=0) # TODO: recheck this function
        distmatrix = (distmatrix + 0.5).astype(int)
        return distmatrix, (probmatrix**self.beta)
    
        #TRY COORDINATE TRANSFORMATION; ALL DISTANCES BETWEEN 0 and 1
    #def disttrans(self):
        

    # get initial guess for a solution
    # OUT: length of greedy solution 
    def initguess(self):
        a = Ant(self.size)
        firstlength = a.naivewalk(self.distances)
        self.greedytour = a.tour
        return firstlength
    
    # initialize pheromones
    # OUT: matrix of bonuses for best path
    def initpheromones(self):
        ph0 = self.size/self.currentbest
        #ph0 = 0.1
        #print('pheromone initialized: ', ph0)
        return np.full((self.size, self.size), ph0)
    
    
    
    # get known solution
    # OUT: array of indices in the order of the solution   
    def readsol(self):
        path = os.getcwd()
        solutionname = self.name + '.opt.tour'
        solution = np.genfromtxt(path + '/ALL_tsp/' + solutionname,  
                                 skip_header = self.getheader(path + '/ALL_tsp/' + solutionname, 'TOUR_SECTION'), 
                                 skip_footer = 2, 
                                 dtype = 'i4')
        solution -=1
        return solution
    
    # ready the ants
    # OUT: array of Ants
    def antsinit(self, antnumber):
        self.ants = [Ant(self.size) for _ in range(antnumber)]
        #print(antnumber, 'ants initialised with tourlength ' , self.ants[0].tourlength)

    # decrease the pheromone          
    def decay(self):
        #old = np.copy(self.pheromones[0,1])
        self.pheromones *= (1 - self.ro)
        #print('decay: ', old, 'to ', self.pheromones[0,1])
        
    #UPDATE FOR ALL CANDIDATE SOLUTIONS   
    def update(self):
        for index, a in enumerate(self.ants):
            # if the Ant is a candidate, check whether it is a new best solution and perform update
            if(a.candidate == True):
                if (a.tourlength < self.currentbest):
                    self.currentbest = a.tourlength
                    self.bestant = a

                # for the edges in the Ant's tour, add 1/tourlength to the pheromone for that edge
                # keep pheromone matrix symmetric    
                i = a.tour[0]
                for j in a.tour[1:]:
                    self.pheromones[i,j] += 1./a.tourlength
                    self.pheromones[j,i] = self.pheromones[i,j]
                    i=j
                self.pheromones[j,a.tour[0]] += 1./a.tourlength
                self.pheromones[a.tour[0], j] = self.pheromones[j,a.tour[0]]
                
                #print('updated for ant no. ', index)
    # adjust the probabilities matrix according to the updated pheromones
    # TODO: check this formula!!
    def weigh(self):
        #old = np.copy(self.pheromones[0,1])
        self.probabilities = self.pheromones**self.alpha * self.heuristics
        #print('max', np.amax(self.probabilities), 'min', np.amin(self.probabilities))
        #print('recalculated probabilities. ')

    # reset all attributes for repetition of optimization   
    def reset(self):
        self.distances, self.heuristics = self.getmatrices()
        self.currentbest = self.initguess()
        self.pheromones = self.initpheromones()
        self.probabilities = self.pheromones**self.alpha * self.heuristics 
        