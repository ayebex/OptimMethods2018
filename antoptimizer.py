# %load ../project/antoptimizer.py
#!/usr/bin/env python3

import numpy as np
import os

#from problem import Problem
#from ant import Ant


class AntOptimizer:
    
    # AntOptimizer performs the optimization process for a given problem
    # attributes:
        # pro: Problem with given parameters
        # maxit: amount of iterations for one optimization process
        # solution: order and length of known solution
        # bestvalues: array of best solution for every iteration
        # bestsamples: array of arrays: bestvalues for several repetitions of optimization process

    def __init__(self, problemname, ro = 0.5, alpha = 1., beta = 1.5, maxiterations = 100, antnumber = 20, solution = 'False'):
        self.pro = Problem(problemname, ro, alpha, beta)
        self.pro.currentbest = self.pro.initguess()
        self.pro.antsinit(antnumber)
        self.maxit = maxiterations+1
        if solution:
            self.solutiontour, self.solutionlength = self.getsolution()
        self.bestvalues = np.zeros(self.maxit)
        self.besttour = np.zeros(self.pro.size)
        self.bestsamples = np.zeros(self.maxit)
        self.alltours = []
        self.globalbesttour = np.zeros(self.pro.size)
        self.globalbestvalue = self.pro.currentbest
        print('\nAnt colony optimization for Travelling Salesman problem: ', self.pro.name, ' with ', antnumber, ' ants')

    # get path and length of known solution
    # OUT: array of indices, length            
    def getsolution(self):
        sol = self.pro.readsol()
        solant = Ant(self.pro.size)
        optlen = solant.solutionwalk(sol, self.pro.distances)
        return sol, optlen
    
    # do the optimization: 
        # in each iteration, all ants find a solution, the problem gets updated, 
        # the best solution and it's length are stored
    def optimization(self):
        
        self.bestvalues[0] = self.pro.currentbest
        self.alltours.append(self.pro.greedytour)
        print('initial guess: ', self.pro.currentbest)
        for iteration in range(1,self.maxit):
            #print('\n_______________________ iteration:', iteration, '____________________________\n')

            for index, ant in enumerate(self.pro.ants):
                ant.walk(0, self.pro.currentbest, self.pro.distances, self.pro.probabilities)
                #print('ant index: ', index, ';  ant tourlength = ', ant.tourlength, ';  candidate? ', ant.candidate)

            self.pro.decay()
            self.pro.update()
            self.pro.weigh()
            
            self.bestvalues[iteration] = self.pro.currentbest
            self.besttour = np.copy(self.pro.bestant.tour)
            self.alltours.append(self.besttour)
            #print('current best: ', self.pro.currentbest)
            #print('best tour by: ', self.pro.bestant)
        
            for ant in self.pro.ants:
                ant.reset()
        
        print('\nsolution found: ', self.pro.currentbest)
        print('found best tour: ', self.besttour)
        print('\nknown solution: ' , self.solutionlength)
        print('known best tour: ', self.solutiontour)
        
    # does (samples) repetitions of the optimization process to get statistics            
    def optsamples(self, samples = 500):
        self.bestsamples = np.zeros((self.maxit, samples))
        for s in range(samples):
            self.pro.reset()
            self.optimization()
            self.bestsamples[:,s] = np.copy(self.bestvalues)
            #print('best: ', self.pro.currentbest)
            if self.pro.currentbest < self.globalbestvalue:
                self.globalbestvalue = self.pro.currentbest
                self.globalbesttour = self.besttour
                print('global best: ', self.globalbestvalue)   
        
        return np.mean(self.bestsamples, axis = 1)