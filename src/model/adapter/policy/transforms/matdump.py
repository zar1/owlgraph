from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Dump to MATLAB"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
        self.rev = 0
    def transform(self, model, active_nodes, active_edges):
        print "revision " + str(self.rev)
        n = model.shape[0]
        toprint = '['
        for row in xrange(n):
            for col in xrange(n):
                toprint = toprint + str(int(model[row,col])) + ' '
            if row < n-1:
                toprint = toprint + '\n'
        toprint = toprint + ']'
        print toprint
        self.rev += 1
        return (active_nodes, active_edges)
