from ..adapterPolicy import Adapter_Policy
from numpy import *

# Dijkstra's algorithm
class P(Adapter_Policy):
    name = "Shortest Path"
    def transform(self, model, active_nodes, active_edges):
        #prelim
        A = model
        start = self.selected[0]
        end = self.selected[1]
        #start = 0
        #end = 4
        
        #find path
        n = A.shape[0]
        val = Inf*ones((n,1))
        val[start] = 0
        parent = -1*ones((n,1), dtype = int)
        visit = zeros((n,1), dtype = bool)
        current = start
        while not visit.all():
            vc = val[current]
            if vc == inf:
                break
            unvisited = nonzero(visit==False)[0]
            neighbors = nonzero(A[current])[0] 
            for neighbor in intersect1d(neighbors, unvisited):
                vn = val[neighbor]
                dist = A[current][neighbor]
                if vc+dist <= vn:
                    val[neighbor] = vc + dist
                    parent[neighbor] = current
            visit[current] = True
            vsort = sort(val, axis=0)
            guess = 0
            current = -1
            for guess in xrange(n):
                candidates = intersect1d(nonzero(val == vsort[guess])[0], nonzero(visit==False)[0])
                if candidates.size > 0:
                    current = candidates[0]
                    break
        r = [end]
        p = parent[end][0]
        while not(p == start):
            if p == -1:
                break
            r.append(p)
            plast = p
            p = parent[p][0]
        r.append(start)
        r.reverse()
        return (r, self.path_from_nodes(r))

        ##construct an adjacency matrix of the path
        #new = zeros(model.shape, dtype=model.dtype)    
        #for ind in xrange(len(r)-1):
        #    first = r[ind]
        #    next = r[ind + 1]
        #    new[first][next] = model[first][next]
        #    new[next][first] = model[next][first]
        #return new
