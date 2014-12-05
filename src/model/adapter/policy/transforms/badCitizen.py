from ..adapterPolicy import Adapter_Policy
from numpy import *

class P(Adapter_Policy):
    name = "Bad Citizen"
    def __init__(self, selected):
        Adapter_Policy.__init__(self, selected)
    def transform(self, model, active_nodes, active_edges):
        while True:
            pass
        return ([1, 7, 3,5, 12], [(1000000, 2000000)])
