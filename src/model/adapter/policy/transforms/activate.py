from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Activate"
    def transform(self, model, active_nodes, active_edges):
        return (self.selected, active_edges)
