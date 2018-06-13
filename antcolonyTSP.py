#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import numpy as np
import os

from problem import Problem
from ant import Ant


class AntcolonyTSP:
    
    def __init__(self, problemname, ro = 0.5, alpha = 1., beta = 1.5, maxiterations = 100, antnumber = 20, solution = 'False'):
        self.pro = Problem(problemname, ro, alpha, beta)
        self.maxit = maxiterations
        self.pro.antsinit(antnumber)
        if solution:
            self.solutiontour, self.solutionlength = self.getsolution()
        self.bestvalues = np.zeros(self.maxit)
        self.besttour = np.zeros(self.pro.size)
        self.bestsamples = np.zeros(self.maxit)
        print('\nAntcolony TSP problem: ', self.pro.name, ' with ', antnumber, ' ants')
                
    def getsolution(self):
        sol = self.pro.readsol()
        solant = Ant(self.pro.size)
        optlen = solant.solutionwalk(sol, self.pro.distances)
        return sol, optlen
    
    def optimization(self):
        self.pro.currentbest = self.pro.initguess()
        print('initial guess: ', self.pro.currentbest)
        for iteration in range(self.maxit):
            #print('\n_______________________ iteration:', iteration, '____________________________\n')

            for index, ant in enumerate(self.pro.ants):
                ant.walk(0, self.pro.currentbest, self.pro.distances, self.pro.probabilities)
                #print('ant index: ', index, ';  ant tourlength = ', ant.tourlength, ';  candidate? ', ant.candidate)

            self.pro.decay();
            self.pro.update();
            self.pro.weigh();
            
            self.bestvalues[iteration] = self.pro.currentbest
            self.besttour = np.copy(self.pro.bestant.tour)
            #print('current best: ', self.pro.currentbest)
            #print('best tour by: ', self.pro.bestant)
        
            for ant in self.pro.ants:
                ant.reset()
        
        print('\nsolution found: ', self.pro.currentbest)
        print('found best tour: ', self.besttour)
        print('\nknown solution: ' , self.solutionlength)
        print('known best tour: ', self.solutiontour)
        
                
    def optsamples(self, samples = 500):
        self.bestsamples = np.zeros((self.maxit, samples))
        for s in range(samples):
            self.optimization()
            self.bestsamples[:,s] = np.copy(self.bestvalues)
            self.pro.reset()           
            
        return np.mean(self.bestsamples, axis = 1)