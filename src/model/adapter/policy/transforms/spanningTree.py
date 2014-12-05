from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Spanning Tree"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
    def transform(self, model, active_nodes, active_edges):
        current = 0
        if self.selected:
            current = self.selected[0]
        fresh = range(model.shape[1])
        (t, fresh) = self.tree_help(model, current, fresh)
        return ([], t)
    def tree_help(self, model, current, fresh):
        myt = []
        fresh.remove(current)
        n = self.N(model, current)
        avail = intersect1d(n, fresh)
        while avail.shape[0] > 0:
            next = avail[0]
            myt.append(self.mk_con(current, next))
            (t, fresh) = self.tree_help(model, next, fresh)
            myt.extend(t)
            avail = intersect1d(n, fresh)
        return (myt, fresh)
