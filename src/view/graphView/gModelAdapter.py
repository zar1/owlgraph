class GModelAdapter:
    def __init__(self):
        self.model = None
    def set_model(self, model):
        self.model = model
    def get_connections_list(self):
        return self.model.get_connections_list()        
    def rm_node(self, ind):
        self.model.rm_node(ind)
    def new_node(self):
        self.model.new_node()
    def conordisconnect(self, ind1, ind2, state):
        self.model.conordisconnect(ind1, ind2, state)
    def receive_adapter(self, adapter):
        self.model.receive_adapter(adapter)
    def push_to_adapters(self):
        self.model.push_to_adapters()
    def get_adapter_face(self):
        return self.model
    def draw_children(self, widget):
        self.model.draw_children(widget)
    def is_active(self):
        return self.model.active
    def is_child_active(self, ind):
        return self.model.children[ind].active
    def get_active_edges(self):
        return self.model.active_edges
    def is_selected(self):
        return self.model.is_selected
    def get_label(self):
        return self.model.label
    def get_geom_for(self, ind):
        return self.model.get_geom_for(ind)
    def configure_children(self, drawing_refs):
        self.model.configure_children(drawing_refs)
    def find_object(self, x, y, lam):
        self.model.find_object(x, y, lam)
    def select(self, target):
        self.model.select(target)
    def get_rank(self):
        return self.model.rank
    def lose_node(self):
        self.model.lose_node()
    def new_child(self, viewpass, left_flag, Adapter_Policy):
        self.model.create_child(viewpass, left_flag, Adapter_Policy) 
    def get_menu(self):
        return self.model.constructed_menu_items
    def parent_is_leftmost(self):
        return self.model.parent_is_leftmost()
