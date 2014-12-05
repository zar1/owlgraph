from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Deactivate Nth"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
    def transform(self, model, active_nodes, active_edges):
        N = len(self.selected)
        if len(active) > N:
            newactive = list(active)
            del newactive[N]
        else:
            newactive = []
        return (newactive, active_edges)
