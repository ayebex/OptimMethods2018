import numpy as np


from problem import Problem
from ant import Ant
from antcolonyTSP import AntcolonyTSP

np.set_printoptions(precision=2)

#ulysses16 = AntcolonyTSP('ulysses16', solution = True, antnumber = 15)
#ulysses16.optimization()

st70 = AntcolonyTSP('st70', ro = 0.6, alpha = 1., beta = 2., solution = True, antnumber = 25)
st70.optimization()

