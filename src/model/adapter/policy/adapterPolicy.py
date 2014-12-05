from numpy import *

class Adapter_Policy:
    name = ""
    def __init__(self, selected):
        self.selected = selected
    def transform(self, model, active_nodes, active_connections):
        return ([], [])
    def lose_node(self, ind):
        for i in xrange(len(self.selected)):
            if self.selected[i] > ind:
                self.selected[i] -= 1
    def mk_con(self, ind1, ind2):
        return (min(ind1, ind2), max(ind1, ind2))
    def path_from_nodes(self, nodelist):
        c = []
        for i in xrange(len(nodelist)-1):
            c.append(self.mk_con(nodelist[i], nodelist[i+1]))
        return c
    def all_combinations_from_nodes(self, nodelist):
        c = []
        s = list(nodelist)
        s.sort()
        for i in xrange(len(s)):
            for j in xrange(i+1,len(s)):
                c.append((s[i], s[j]))
        return c
    def N(self, model, ind):
        return nonzero(model[ind])[0]
