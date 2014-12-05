from ..adapterPolicy import Adapter_Policy
from numpy import *
from math import sqrt

class P(Adapter_Policy):
    name = "Slow Citizen"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
    def transform(self, model, active_nodes, active_edges):
        x = 2
        for i in xrange(99999999/2):
            x = sqrt(x)
        print 'slow citizen done'
        return (model, [0], [])
