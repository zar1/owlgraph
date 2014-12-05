from numpy import *
from random import random

class Graph_Model:
    def __init__(self, view, leftmost, parent, label, factory):
        self.view = view
        self.leftmost = leftmost
        self.left_adapter = None
        self.parent = parent
        self.label = label
        self.factory = factory
        self.children = []
        self.is_selected = False
        self.selected_children = []
        self.child_label = 0
        self.active = False
        self.active_children = []
        self.active_edges = []
        self.data = array([[]], dtype = bool)
        self.connections = []
        self.adapters = []
        self.rank = 0
        self.menu_items = []
        self.constructed_menu_items = []
        self.resize = False
        self.hidden = False
    def set_data(self, data):
        self.data = data.copy()
        self.update_connection_list()
    def get_data(self):
        return self.data.copy()
    def new_node(self):
        olddata = self.data
        self.data = zeros((olddata.shape[1] +1, olddata.shape[1] + 1), dtype = bool)
        self.data[0:olddata.shape[1],0:olddata.shape[1]] = olddata
    def rm_node(self, ind):
        self.data = delete(self.data, ind, axis=0)
        self.data = delete(self.data, ind, axis=1)
        self.update_connection_list()
    def conordisconnect(self, source, dest, direction):
        if direction:
            self.connect(source, dest)
        else:
            self.disconnect(source, dest)
        self.update_connection_list()
        self.push_to_adapters(True)
    def connect(self, source, dest):
        if not self.data[source, dest]:
            self.data[source, dest] = True
            self.data[dest, source] = True
    def disconnect(self, source, dest):
        if self.data[source, dest]:
            self.data[source, dest] = False
            self.data[dest, source] = False
    def update_connection_list(self):
        self.connections = []
        for row in xrange(self.data.shape[0]):
            for col in xrange(self.data.shape[1]):
                if self.data[row,col]:
                    self.connections.append((row, col))
    def get_connections_list(self):
        return self.connections    
    def get_size(self):
        return self.shape[1]
    def receive_adapter(self, adapter):
        self.adapters.append(adapter)
        props = self.view.get_child_proportions()
        for i in xrange(len(self.children)):
            adapter.gain_node(self.children[i].label, props[i])  
        self.push_to_adapters(True)        
    def push_to_adapters(self, force):
        for adapter in self.adapters:
            adapter.push(force, self.get_data(), self.view.get_child_proportions(), list(self.active_children), list(self.active_edges))
    def update_active_children(self):
        #TODO slow way of doing this
        for i in xrange(len(self.children)):
            self.children[i].active = i in self.active_children
    def receive_update(self, force, model, props, active_nodes, active_edges):
        self.set_data(model)
        self.active_children = list(active_nodes)
        self.active_edges = list(active_edges)
        self.update_active_children()
        self.view.receive_update(props)
        self.push_to_adapters(force)
    def draw_children(self, widget):
        for child in self.children:
            child.draw(widget)
    def draw(self, widget):
        self.view.draw(widget)
    def get_geom_for(self, ind):
        return self.children[ind].view.get_geom()
    def configure_event_for(self, child_num, pixmap, pl, cx, cy, cwidth, cheight):
        self.children[child_num].view.configure_event(pixmap, pl, cx, cy, cwidth, cheight)
    def configure_children(self, drawing_refs):
        for i in xrange(len(self.children)):
            pos_vals = self.view.find_absolute_bounds(i)
            self.children[i].view.configure_event(drawing_refs, pos_vals)
    class lambda_pass_menu:
        #should not allow modification of leftmost graphs
        def __init__(self):
            self.collect = []
            self.poison = False
        def root(self, this):
            self.run(this)
        def graph(self, this):
            if this.hidden:
                self.collect.append(this.unhide_item)
            else:
                self.collect.append(this.hide_item)
                if this.leftmost:
                    self.collect.append(this.add_point_item)
            if not this.leftmost:
                self.poison = True
            self.run(this)
        def point(self, this):
            if not self.poison:
                self.run(this)
            else:
                this.constructed_menu_items = self.collect
        def run(self, this):
            self.collect.extend(this.menu_items)
            this.constructed_menu_items = self.collect
    
    class lambda_select:
        def run(self, this):
            this.select_me()
        def root(self, this):
            self.run(this)
        def graph(self, this):
            self.run(this)
        def point(self, this):
            self.run(this)
    #def lambda_run(self, lam):
    #    lam.nonroot(self)
    def find_object(self, x, y, lam):
        if lam:
            self.lambda_run(lam)
        if not self.hidden:
            for child in self.children:
                if child.view.has_point(x, y):
                    return child.find_object(x, y, lam)
        return self
    def select(self, x, y):
        target = self.find_object(x, y, self.lambda_pass_menu())
        tparent = target.parent
        if not target.is_selected:
            if not self.get_last_selected_parent() is tparent:
                self.clear_selection()
            target.select_me()
            self.find_object(x, y, self.lambda_select())
        else:
            self.clear_selection()
    def reselect(self, child):
        self.clear_selection()
        x, y, w, h = child.view.get_geom()
        self.select(x, y)
    def select_me(self):
        if not self.is_selected:
            self.rank = self.parent.register_child_selected(self)
            self.is_selected = True
            if self.rank > 3:
                self.rank = 3
    def get_last_selected_parent(self):
        if not self.selected_children:
            return None
        else:
            c = self.children[self.selected_children[0]]
            if c.selected_children:
                return c.get_last_selected_parent()
            else:
                return self
    def clear_selection(self):
        self.selected_children = []
        self.unselect_me()
        for child in self.children:
            child.clear_selection()
    def unselect_me(self):
        self.is_selected = False
    def register_child_selected(self, child):
        self.selected_children.append(self.children.index(child))
        return len(self.selected_children) - 1
    def lose_node(self, ind):
        child = self.children[ind]
        self.remove_child(child)
    def self_destruct(self, start):
        if start and self.left_adapter:
            self.left_adapter.orphan()
        self.parent.remove_child(self)
        for adapter in self.adapters:
            adapter.destroy()
    def remove_child(self, child):
        ind = self.children.index(child)
        for adapter in self.adapters:
            adapter.lose_node(ind)
        self.rm_node(ind)
        if child.is_selected:
            child.clear_selection()
            self.selected_children.remove(ind)
            for i in xrange(len(self.selected_children)):
                if self.selected_children[i] > ind:
                    self.selected_children[i] -= 1
        if child.active:
            print self.label
            self.active_children.remove(ind)
        for con in self.active_edges:
            if ind in con:
                self.active_edges.remove(con)
        self.children.remove(child)
        self.view.remove(len(self.children), ind)
        #self.push_to_adapters(True)
    def create_child(self, view_pass, left, Adapter_Policy):
        label = str(self.child_label)
        if Adapter_Policy:
            label = label + ' (from ' + Adapter_Policy.name + ')'
        self.child_label += 1
        #left = None
        #if left_flag:
        #    left = self.children[self.selected_children[0]]
        c = self.factory.make_child(label, view_pass, left, Adapter_Policy, self)
        self.children.append(c)
        self.new_node()
        if left:
            self.conordisconnect(self.children.index(left), len(self.children)-1, True)
        for adapter in self.adapters:
            adapter.gain_node(label, self.view.get_child_proportions()[-1])
        #self.push_to_adapters(True)
    def set_child_active(self, ind, new_state):
        self.children[ind].active = new_state
        if new_state and not(ind in self.active_children):
            self.active_children.append(ind)
        if not(new_state) and (ind in self.active_children):
            self.active_children.remove(ind)
        self.push_to_adapters(True)
    def get_parent(self):
        return self.parent
    def gain_node(self, label, proportions):
        self.view.gain_node(len(self.children), proportions)
        self.children[-1].label = label
        self.push_to_adapters(True)
    def quit(self):
        for adapter in self.adapters:
            adapter.quit()
    def random_connect(self, prob):
        for row in xrange(self.data.shape[0]):
            for col in xrange(self.data.shape[1]):
                if random() < prob:
                    self.conordisconnect(row, col, True)
                    self.conordisconnect(col, row, True)
    def drag_start(self, x, y):
        self.resize = self.view.in_resize_corner(x, y)
        self.offset = self.view.get_offset(x, y)        
    def drag_to(self, x, y):
        if self.parent.leftmost:
            if self.resize:
                self.parent.update_child_size(x, y, self)
            else:
                self.parent.update_child_position(x, y, self.offset, self)
    def drag_stop(self):
        pass
    def update_child_position(self, x, y, offset, child):
        self.view.update_child_position(x, y, offset, self.children.index(child))
    def update_child_size(self, x, y, child):
        self.view.update_child_size(x, y, self.children.index(child))
    def get_adapter_chain(self):
        chain = []
        for adapter in self.adapters:
            chain.append(adapter.save())
        return chain
    #def save(self):
    #    return (self.view.get_child_proportions(), self.data, self.get_adaper_chain())
    def hide(self, state):
        self.hidden = state
        self.view.hide(state)
    def parent_is_leftmost(self):
        return self.parent.leftmost
    def set_left_adapter(self, ad):
        self.left_adapter = ad
    def lose_adapter(self, adapter):
        self.adapters.remove(adapter)
