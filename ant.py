#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import os


class Ant:
    
    def __init__(self, problemsize):
        self.size = problemsize
        self.cities = np.arange(problemsize)
        self.tour = np.zeros(problemsize, 'i4')
        self.tourlength = 0
        self.choices = np.zeros(problemsize, 'f8')
        self.candidate = False
        
    def choosenext(self, position, probmatrix):
        self.choices = np.copy(probmatrix[position, :])
        #print(self.choices)
        self.choices[self.tour] = 0.
        #print(self.choices)
        #print("sum", self.choices.sum())
        #DO WITH MASK, COPY WHEN DIVIDING
        s = self.choices.sum()
        self.choices /= s
        #return np.random.choice(self.cities, size=None, replace=True, p = self.choices)
        return np.random.multinomial(1,self.choices).argmax()
    
    def walk(self, start, currentbest, distmatrix, probmatrix):
        self.tourlength = 0
        self.tour = np.zeros(self.size, 'i4')
        i = start
        self.tour[0] = i
        for k in range(1, self.size):
            #print('i', i, 'j', j)
            #print("i =", i)
            j = self.choosenext(i, probmatrix)
            self.tour[k] = j
            self.tourlength += distmatrix[i,j]
            i = j
            #print("i==j =", i)
            #print("length =", self.tourlength)
            #print("tour:", self.tour)
            if (self.tourlength > currentbest):
                return
        self.tourlength += distmatrix[j,start]
        if (self.tourlength >= currentbest):
                return self.tourlength
        self.candidate = True
        return self.tourlength
    
    def solutionwalk(self, solution, distmatrix):
        self.tour = np.zeros(self.size, 'i4')
        self.tourlength = 0
        i = solution[0]
        for j in solution[1:]:
            self.tourlength += distmatrix[i,j]
            i=j
        self.tourlength += distmatrix[solution[-1], solution[0]]
        return self.tourlength
    
    def naivewalk(self, distmatrix):
        randsol = np.random.permutation(self.size)
        self.tour = np.zeros(self.size, 'i4')
        self.tourlength = 0
        i = randsol[0]
        self.tour[0] = 0
        for j in randsol[1:]:
            self.tourlength += distmatrix[i,j]
            i=j
        self.tourlength += distmatrix[randsol[-1], randsol[0]]
        return self.tourlength
    
    def reset(self):
        self.tour = np.zeros(self.size, 'i4')
        self.tourlength = 0
        self.choices = np.zeros(self.size, 'f8')
        self.candidate = False
        