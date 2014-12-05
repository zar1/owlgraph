from ..graphModel import Graph_Model

class Point(Graph_Model):
    def __init__(self, view, leftmost, parent, label, factory):
        Graph_Model.__init__(self, view, leftmost, parent, label, factory)
        self.menu_items = [("Remove Point", self.remove_point, None),
                           ("Connect", self.connect_nodes, True),
                           ("Disconnect", self.connect_nodes, False),
                           ("Toggle Active", self.toggle_active, None),]
    def remove_point(self, widget, ops):
        # safe from renumbering
        cs = []
        for i in self.parent.selected_children:
            cs.append(self.parent.children[i])
        for c in cs:
            self.parent.remove_child(c)    
    def connect_nodes(self, widget, ops):
        new_state = ops[0]
        selected = self.parent.selected_children
        #if new_state:
        #    if len(selected) > 1:
        #       for i in xrange(len(selected) - 1):
        #            self.parent.conordisconnect(selected[i], selected[i+1], new_state)
        #else:
        if True:
            for ind1 in self.parent.selected_children:
                for ind2 in self.parent.selected_children:
                    if ind1 != ind2:
                       self.parent.conordisconnect(ind1, ind2, new_state)
    def toggle_active(self, widget, ops):
        for i in self.parent.selected_children:
            self.parent.set_child_active(i, not self.parent.children[i].active)
    def lambda_run(self, lam):
        lam.point(self)
    
