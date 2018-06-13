#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
import numpy as np
import os

from ant import Ant

class Problem:
        
    def getheader(self, file, string):
        header = 0
        with open(file) as f:
            for line in f:
                header += 1
                if string in line:
                    break
        f.close()
        return header
    
    def skiprows(self):
        path = os.getcwd()
        return self.getheader(path + '/ALL_tsp/' + self.name + '.tsp', 'NODE_COORD_SECTION')
    
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
    
    
    #TRY COORDINATE TRANSFORMATION; ALL DISTANCES BETWEEN 0 and 1
    def getmatrices(self):
        xI, xJ = np.meshgrid(self.x,self.x, sparse=False, indexing='ij')
        yI, yJ = np.meshgrid(self.y,self.y, sparse=False, indexing='ij')
        distmatrix = np.sqrt((xI-xJ)**2 + (yI-yJ)**2)
        probmatrix = np.divide(1, distmatrix, out=np.zeros_like(distmatrix), where=distmatrix!=0)
        distmatrix = (distmatrix + 0.5).astype(int)
        return distmatrix, (probmatrix**self.beta)
    
    def initguess(self):
        a = Ant(self.size)
        return a.naivewalk(self.distances)
    
    def initpheromones(self):
        ph0 = self.size/self.currentbest
        #ph0 = 0.1
        #print('pheromone initialized: ', ph0)
        return np.full((self.size, self.size), ph0)
    
    
    
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
        
        
        
        
    def readsol(self):
        path = os.getcwd()
        solutionname = self.name + '.opt.tour'
        solution = np.genfromtxt(path + '/ALL_tsp/' + solutionname,  
                                 skip_header = self.getheader(path + '/ALL_tsp/' + solutionname, 'TOUR_SECTION'), 
                                 skip_footer = 2, 
                                 dtype = 'i4')
        solution -=1
        return solution
    
    def antsinit(self, antnumber):
        self.ants = [Ant(self.size) for _ in range(antnumber)]
        #print(antnumber, 'ants initialised with tourlength ' , self.ants[0].tourlength)
            
    def decay(self):
        #old = np.copy(self.pheromones[0,1])
        self.pheromones *= (1 - self.ro)
        #print('decay: ', old, 'to ', self.pheromones[0,1])
        
#UPDATE FOR ALL CANDIDATE SOLUTIONS   
    def update(self):
        for index, a in enumerate(self.ants):
            if(a.candidate == True):
                if (a.tourlength < self.currentbest):
                    self.currentbest = a.tourlength
                    self.bestant = a
                    
                i = a.tour[0]
                for j in a.tour[1:]:
                    self.pheromones[i,j] += 1./a.tourlength
                    self.pheromones[j,i] = self.pheromones[i,j]
                    i=j
                self.pheromones[j,a.tour[0]] += 1./a.tourlength
                self.pheromones[a.tour[0], j] = self.pheromones[j,a.tour[0]]
                
                #print('updated for ant no. ', index)

    def weigh(self):
        #old = np.copy(self.pheromones[0,1])
        self.probabilities = self.pheromones**self.alpha * self.heuristics
        #print('max', np.amax(self.probabilities), 'min', np.amin(self.probabilities))
        #print('recalculated probabilities. ')
        
    def reset(self):
        self.distances, self.heuristics = self.getmatrices()
        self.currentbest = self.initguess()
        self.pheromones = self.initpheromones()
        self.probabilities = self.pheromones**self.alpha * self.heuristics 
        