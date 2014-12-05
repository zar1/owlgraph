class GViewAdapter:
    def __init__(self):
        self.view = None
    def set_view(self, view):
        self.view = view
    def receive_update(self, children_proportions):
        self.view.receive_update(children_proportions)
    def get_child_proportions(self):
        return self.view.get_child_proportions()
    def get_active_children(self):
        return self.view.active_children
    def draw(self, widget):
        self.view.draw(widget)
    def get_geom(self):
        return self.view.get_geom()
    def configure_event(self, draw_refs, pos_vals):
        self.view.configure_event(draw_refs, pos_vals)
    def has_point(self, x, y):
        return self.view.has_point(x,y)
    def gain_node(self, proplen, proportions):
        self.view.gain_node(proplen, proportions)
    def remove(self, proplen, ind):
        self.view.remove(proplen, ind)
    def create_child(self, x, y, rad, left_flag, Adapter_Policy):
        self.view.create_child(x, y, rad, left_flag, Adapter_Policy)
    def context_menu(self, event):
        self.view.context_menu(event)
    def new_graph_dialog(self):
        return self.view.new_graph_dialog()
    def update_child_position(self, x, y, offset, ind):
        self.view.update_child_position(x, y, offset, ind)
    def update_child_size(self, x, y, ind):
        self.view.update_child_size(x, y, ind)
    def in_resize_corner(self, x, y):
        return self.view.in_resize_corner(x, y)
    def reset(self):
        self.view.reset()
    def hide(self, state):
        self.view.hide(state)
    def get_offset(self, x, y):
        return self.view.get_offset(x, y)
    def find_absolute_bounds(self, ind):
        return self.view.find_absolute_bounds(ind)
