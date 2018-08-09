def vary_antnumber(problemname, maxiter, samples, str = 'minim'):

    opt_antnumber = []
    antno = [5, 10, 20, 50, 100]
    for an in antno:
        opt_antnumber.append(AntOptimizer(problemname, maxiterations = maxiter, antnumber = an, solution = 'True'))

    for opt in opt_antnumber:
        print(len(opt.pro.ants), 'ants; ', )
        opt.optsamples(samples)

    if str == 'mean':
        plotconvergence(opt_antnumber, mean='True', minim='False', noteslist = antno, title='shortest path found for different number of ants')
    else:
        plotconvergence(opt_antnumber, noteslist = antno)
        
#
#vary parameter alpha
def vary_alpha(problemname, maxiter, samples, str = 'minim'):

    opt_alpha = []
    alpha = [0.5, 0.75, 1.0, 1.25, 1.5]
    for a in alpha:
        opt_alpha.append(AntOptimizer(problemname, alpha = a, maxiterations = maxiter, antnumber = 50, solution = 'True'))

    for opt in opt_alpha:
        print('alpha: ', opt.pro.alpha )
        opt.optsamples(samples)

    if str == 'mean':
        plotconvergence(opt_alpha, mean='True', minim='False', noteslist = alpha, title=problemname +'; shortest path found for different values of alpha')
    else:
        plotconvergence(opt_alpha, noteslist = alpha, title=problemname +'; shortest path found for different values of alpha')
        
        ##vary parameter beta


def vary_beta(problemname, maxiter, samples, str = 'minim'):

    opt_alpha = []
    alpha = [1, 1.75, 2.5, 3.5, 5]
    for a in alpha:
        opt_alpha.append(AntOptimizer(problemname, beta = a, maxiterations = maxiter, antnumber = 50, solution = 'True'))

    for opt in opt_alpha:
        print('beta: ', opt.pro.beta )
        opt.optsamples(samples)

    if str == 'mean':
        plotconvergence(opt_alpha, mean='True', minim='False', noteslist = alpha, title=problemname +'; shortest path found for different values of beta')
    else:
        plotconvergence(opt_alpha, noteslist = alpha, title=problemname +'; shortest path found for different values of beta')
        
        #

#vary parameter ro


def vary_ro(problemname, maxiter, samples, str = 'minim'):

    opt_alpha = []
    alpha = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ]
    for a in alpha:
        opt_alpha.append(AntOptimizer(problemname, ro = a, maxiterations = maxiter, antnumber = 50, solution = 'True'))

    for opt in opt_alpha:
        print('ro: ', opt.pro.ro )
        opt.optsamples(samples)

    if str == 'mean':
        plotconvergence(opt_alpha, mean='True', minim='False', noteslist = alpha, title=problemname +'; shortest path found for different values of ro')
    else:
        plotconvergence(opt_alpha, noteslist = alpha, title=problemname +'; shortest path found for different values of ro')
        
    #