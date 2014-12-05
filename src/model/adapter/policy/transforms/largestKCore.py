from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Largest K Core"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
    def transform(self, model, active_nodes, active_edges):
        k = len(self.selected)
        f = []
        fnew = array(active_nodes)
        #fnew = array(range(model.shape[0]))
        while not self.same(f, fnew):
            f = fnew.copy()
            d = model.take(f, axis=0).take(f, axis=1).sum(axis=0)
            x = nonzero(d < k)[0]
            y = f[x]
            fnew = setdiff1d(f, y)
        nodelist = fnew.tolist()
        return (nodelist, self.all_combinations_from_nodes(nodelist))
    def same(self, v1, v2):
        if shape(v1) == shape(v2):
            if (v1 == v2).all():
                return True
        return False
