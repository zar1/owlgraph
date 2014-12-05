from ..graphModel import Graph_Model
from math import pi

class Root(Graph_Model):
    def __init__(self, view, leftmost, parent, label, factory):
        Graph_Model.__init__(self, view, leftmost, parent, label, factory)
        self.menu_items = [("New Graph", self.new_graph, None)]
        self.graph_menu_items = []
    def lambda_run(self, lam):
        lam.root(self)
    def set_transforms(self, transforms):
        self.graph_menu_items = transforms        
    def new_graph(self, widget, ops):
        Policy = ops[0]
        context = ops[1]
        x = context.get_x()
        y = context.get_y()
        r = self.view.new_graph_dialog()
        if r:
            nodes, prob = r
            self.view.create_child(x, y, -1, False, None)
            c = self.children[-1]
            for i in xrange(nodes):
                rad = (float(i)/nodes) * (2*pi)
                c.view.create_child(x, y, rad, False, None)
            if prob:
                c.random_connect(prob)
        self.view.reset()
    def select_me(self):
        if not self.is_selected:
            self.is_selected = True    
    def recalc(self):
        for child in self.children:
            if child.leftmost:
                #child.push_to_adapters(False)
                child.push_to_adapters(True)
    def quit(self):
        for child in self.children:
            if child.leftmost:
                child.quit()
    def create_child(self, view_pass, left, Adapter_Policy):
        Graph_Model.create_child(self, view_pass, left, Adapter_Policy)
        self.children[-1].set_transforms(self.graph_menu_items)
    def get_last_selected(self):
        p = self.get_last_selected_parent()
        if p is None:
            return self
        return p.children[p.selected_children[0]]
    def drag_to(self, x, y):
        pass
    def new(self):
        for c in list(self.children):
            if c.leftmost:
                c.self_destruct(True)
        self.child_label = 0
    def save(self):
        children_save = []
        for child in self.children:
            if child.leftmost:
                children_save.append(child.save())
        return (self.view.get_child_proportions(), self.data, children_save)
    def load(self, env):
        distributed = env[2]
        for data in distributed:
            self.view.create_child(0, 0, -1, None, None)
            #TODO: load for graphs
            self.children[-1].load(data)
        self.set_data(env[1])
        self.view.receive_update(env[0])
