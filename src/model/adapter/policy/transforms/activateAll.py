from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Activate All"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
    def transform(self, model, active_nodes, active_edges):
        nodelist = range(model.shape[1])
        return (nodelist, self.all_combinations_from_nodes(nodelist))
