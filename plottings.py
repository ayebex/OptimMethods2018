# plotting functions
import matplotlib.pyplot as plt

def plottours(testit):
    
    greedyx = testit.pro.x[testit.pro.greedytour]
    greedyy = testit.pro.y[testit.pro.greedytour]
    if testit.statistics == 'True':
        globalsolx = testit.pro.x[testit.globalbesttour]
        globalsoly = testit.pro.y[testit.globalbesttour]
    else:
        globalsolx = testit.pro.x[testit.besttour]
        globalsoly = testit.pro.y[testit.besttour]
    solx = testit.pro.x[testit.solutiontour]
    soly = testit.pro.y[testit.solutiontour] 
    
    fig, ax = plt.subplots()


    ax.plot(greedyx, greedyy, color = '0.8', label='initial guess')
    ax.plot(solx,soly, label='optimal solution')
    ax.plot(globalsolx,globalsoly, label='best found solution')

    ax.plot(testit.pro.x, testit.pro.y, 'o', color='black')
    
    ax.legend(loc='upper right')

    plt.show()
    
    
def plotconvergence(testit, mean = 'False', notes = 'best run'):
    
    fig, ax = plt.subplots()
    # known solution
    ax.plot(np.full(testit.maxit, testit.solutionlength), 'r', label='known optimum')
    
    # mean of solutions found
    if mean == 'True':
        ax.plot(testit.samplemean, label='mean of all runs')
        
    # best solutions found
    ax.plot(testit.sampleminimum, label=notes)
    
    ax.legend(loc='upper right')

    ax.set_ylim(testit.solutionlength-100, testit.sampleminimum[0])
    plt.show()