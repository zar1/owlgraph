from ..graphModel import Graph_Model

class Graph(Graph_Model):
    def __init__(self, view, leftmost, parent, label, factory):
        Graph_Model.__init__(self, view, leftmost, parent, label, factory)
        self.menu_items = [("Delete Graph", self.__self_destruct, None)]
        #self.olen = len(self.menu_items) + 1
        self.hide_item = ('Hide', self.hide_from_menu, True)
        self.unhide_item = ('Unhide', self.hide_from_menu, False)
        self.add_point_item = ("Add Point", self.add_point, None)
        self.transforms_dict = {}
    def hide_from_menu(self, widget, data):
        state = data[0]
        self.hide(state)
        self.parent.reselect(self)
    def __self_destruct(self, widget, data):
        self.self_destruct(True)
    def add_point(self, widget, ops):
        context = ops[1]
        x = context.get_x()
        y = context.get_y()
        self.view.create_child(x, y, -1, False, None)
    def set_transforms(self, transforms):
        m = []
        for t in transforms:
            m.append((t[0], self.__make_transform_from_context, t[1]))
            self.transforms_dict[t[0]] = t[1]
        m.extend(self.menu_items)
        self.menu_items = m
    def __make_transform_from_context(self, widget, ops):
        Policy = ops[0]
        context = ops[1]
        x = context.get_x()
        y = context.get_y()
        self.__make_transform(x, y, Policy)
    def __make_transform(self, x, y, Policy):   
        left = self 
        self.parent.view.create_child(x, y, -1, left, Policy)
    def lambda_run(self, lam):
        lam.graph(self)
    def save(self):
        return [self.view.get_child_proportions(), self.data, self.active_children, self.active_edges, self.hidden, self.get_adapter_chain()]
    def load(self, env):
        if env:
            if self.leftmost:
                for i in xrange(env[1].shape[1]):
                    self.view.create_child(0, 0, -1, None, None)
                self.set_data(env[1])
                self.active_children =(env[2])
                self.update_active_children()
                self.active_edges = env[3]
                self.view.receive_update(env[0])
            self.hide(env[4]) 
            for data in env[5]:
                Policy = self.transforms_dict[data[0][0]]
                selected = data[0][1]
                for index in selected:
                    self.children[index].select_me()
                self.__make_transform(0, 0, Policy)
                self.clear_selection()
                self.adapters[-1].load(data[1], selected)
