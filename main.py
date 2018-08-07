import numpy as np


from problem import Problem
from ant import Ant
from antoptimizer import AntOptimizer

np.set_printoptions(precision=2)

ulysses16 = AntOptimizer('ulysses16', solution = True, antnumber = 20)
ulysses16.optimization()

st70 = AntOptimizer('st70', ro = 0.6, alpha = 1., beta = 2., solution = True, antnumber = 25)
st70.optimization()

