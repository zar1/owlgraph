from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Closure"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
        self.k = len(selected)
    def transform(self, model, active_nodes, active_edges):
        n = model.shape[0]
        x = zeros((n,1))
        x[active_nodes] = 1
        A0 = model
        k = self.k
        y = dot(A0,x)
        y[y<k] = 0
        y[y>=k] = 1
        ncnt = 1;
        while linalg.norm(y-x) > .5 and ncnt < n:
            x = y.copy()
            y = dot(A0,x)
            y[y<k] = 0
            y[y>=k] = 1
            ncnt += 1
        nodelist = nonzero(y)[0].tolist()
        return (nodelist, self.all_combinations_from_nodes(nodelist))
