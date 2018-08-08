# plotting functions
import matplotlib.pyplot as plt

def plotalltours(testit):
    
    greedyx = testit.pro.x[testit.pro.greedytour]
    greedyy = testit.pro.y[testit.pro.greedytour]
    globalsolx = testit.pro.x[testit.globalbesttour]
    globalsoly = testit.pro.y[testit.globalbesttour]
    solx = testit.pro.x[testit.solutiontour]
    soly = testit.pro.y[testit.solutiontour] 
    
    fig, ax = plt.subplots()


    ax.plot(greedyx, greedyy, color = '0.8', label='initial guess')
    ax.plot(solx,soly, label='optimal solution')
    ax.plot(globalsolx,globalsoly, label='global best solution')

    ax.plot(testit.pro.x, testit.pro.y, 'o', color='black')
    
    ax.legend(loc='upper right')

    plt.show()
    
    
def plotconvergence(testit, mean = 'False'):
    fig, ax = plt.subplots()
    # known solution
    ax.plot(np.full(testit.maxit, testit.solutionlength), 'r')
    
    # mean of solutions found
    if mean == 'True':
        ax.plot(testit.samplemean)
        
    # best solutions found
    ax.plot(testit.sampleminimum)

    ax.set_ylim(testit.solutionlength-100, testit.sampleminimum[0])
    plt.show()