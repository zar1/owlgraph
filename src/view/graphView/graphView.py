import gtk
import math

from ...model.graphModel.graphModel import Graph_Model
from ...model.adapter.adapter import Adapter
from ...model.adapter.policy import adapterPolicy

class Graph_View:
    selected_colors = (gtk.gdk.Color(0x0000, 0x3333, 0x6666),
                       gtk.gdk.Color(0x9595, 0xcaca, 0xffff),
                       gtk.gdk.Color(0x0000, 0x5252, 0xa4a4),
                       gtk.gdk.Color(0xc9c9, 0xe4e4, 0xffff))
    unselected_color = gtk.gdk.Color(0x0000, 0x0000, 0x0000)
    activated_color = gtk.gdk.Color(0xffff, 0xffff, 0x0000)
    def __init__(self, model, view_pass):
        (x, y, width, height, pixmap, pl) = view_pass
        self.model = model
        self.pixmap = pixmap
        self.pl = pl
        self.children_proportions = [] # a list
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = Graph_View.unselected_color
        self.menu_items = []
        self.constructed_menu_items = []
        self.new_child_default_w = .1
        self.new_child_default_h = .1
        self.resize_prop = .1
        self.hidden = False
    def receive_update(self, children_proportions):
        nnodes = len(children_proportions)
        self.children_proportions = children_proportions[:nnodes]
        self.reconfigure()
    def find_absolute_bounds(self, child_index):
        propx, propy, propwidth, propheight = self.children_proportions[child_index]
        thiswidth = self.width*propwidth
        thisheight = self.height*propheight
        thisx = propx*self.width + self.x
        thisy = propy*self.height + self.y
        return (thisx, thisy, thiswidth, thisheight)
    def draw(self, widget):
        if not self.pixmap:
            return
        x, y, width, height = self.get_geom()
        if not self.model.is_selected():
            self.color = Graph_View.unselected_color
        else:
            self.color = Graph_View.selected_colors[self.model.get_rank()]
        color = widget.get_colormap().alloc_color(self.color)
        gc = widget.window.new_gc()
        gc.foreground = color
        if self.hidden:
            x, y, width, height = self.get_geom()
            w, h = self.__round((self.new_child_default_w * width,  self.new_child_default_h * height))
            self.pixmap.draw_rectangle(gc, False, x, y, w, h)
        else:
            self.draw_help(widget, gc)
            self.model.draw_children(widget)
            self.draw_connections(gc)            
    def draw_help(self, widget, gc):
        x, y, width, height = self.get_geom()
        if self.model.is_active():
            color = gc.foreground
            gc.foreground = widget.get_colormap().alloc_color(self.activated_color)
            self.pixmap.draw_rectangle(gc, True, x, y, width, height)
            gc.foreground = color
        self.pixmap.draw_rectangle(gc, False, x, y, width, height)
        if self.model.is_selected():
            self.pixmap.draw_rectangle(gc, False, x+1, y+1, width, height)
        self.pl.set_text(self.model.get_label())
        self.pixmap.draw_layout(gc, x, y, self.pl)
        if self.model.parent_is_leftmost():
            xcorner = x + width*(1-self.resize_prop)
            ycorner = y + height*(1-self.resize_prop)
            wcorner = width*(self.resize_prop)
            hcorner = height*(self.resize_prop)
            rounded = self.__round((xcorner, ycorner, wcorner, hcorner))
            self.pixmap.draw_rectangle(gc, True, rounded[0], rounded[1], rounded[2], rounded[3])
    def draw_connections(self, gc):
        connections = self.model.get_connections_list()
        active = self.model.get_active_edges()
        for connection in connections:
            c1 = connection[0]
            c2 = connection[1]
            x1, y1, w, h = self.model.get_geom_for(c1)
            x2, y2, w, h = self.model.get_geom_for(c2)
            if connection in active:
                lw = gc.line_width
                gc.line_width = 3
                self.pixmap.draw_line(gc, x1, y1, x2, y2)
                gc.line_width = lw
            else:
                self.pixmap.draw_line(gc, x1, y1, x2, y2)
    class Context:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def get_x(self):
            return self.x
        def get_y(self):
            return self.y
    def context_menu(self, event):
        self.make_menu(self.Context(event.x, event.y))
        self.menu.popup(None, None, None, event.button, event.time, None)
    def reconfigure(self):
        self.model.configure_children((self.pixmap, self.pl))
    def configure_event(self, drawing_references, place_references):
        rounded_pos = self.__round(place_references)
        self.x = rounded_pos[0]
        self.y = rounded_pos[1]
        self.width = rounded_pos[2]
        self.height = rounded_pos[3]
        self.pixmap = drawing_references[0]
        self.pl = drawing_references[1]
        self.reconfigure()
    def get_geom(self):
        return self.x, self.y, self.width, self.height
    def has_point(self, x, y):
        cx, cy, cwidth, cheight = self.get_geom()
        if self.hidden:
            cwidth = int(self.new_child_default_w*cwidth)
            cheight = int(self.new_child_default_h*cheight)
        return ((cx <= x) and (x <= cx + cwidth)) and ((cy<= y) and (y <= cy + cheight ))
    def select(self, x, y):   
        self.model.select(x, y)
    def lose_node(self, ind):
        #child = self.children[ind]
        #self.remove_child(child)
        self.model.lose_node(ind)
        del self.children_proportions[ind]
    
    def create_child(self, x, y, rad, left, Adapter_Policy):
        absx, absy, abswidth, absheight = self.get_geom()
        if rad > -1:
            x = math.cos(rad) * (abswidth-abswidth*self.new_child_default_w) * .5 + absx + (abswidth * .5) - abswidth*self.new_child_default_w* .5
            y = math.sin(rad) * (absheight-absheight*self.new_child_default_h-20) * .5 + absy + (absheight * .5) - absheight*self.new_child_default_h * .5 + 10
            #TODO use actual font size instead of "20"
        relx, rely = self.get_relative_geom(x, y)
        relwidth = self.new_child_default_w
        relheight = self.new_child_default_h
        self.children_proportions.append([relx, rely, relwidth, relheight])
        self.model.new_child((x, y, abswidth*relwidth, absheight*relheight, self.pixmap, self.pl), left, Adapter_Policy)
        self.fix_proportions()
    def get_relative_geom(self, x, y):
        absx, absy, abswidth, absheight = self.get_geom()
        relx = (x-absx)/abswidth
        rely = (y-absy)/absheight
        return (relx, rely)    
    def gain_node(self, proplen, proportions):
        absx, absy, abswidth, absheight = self.get_geom()
        relx, rely, relwidth, relheight = proportions
        self.create_child(absx + relx*abswidth, absy + rely*absheight, -1, False, None)
        if proplen > len(self.children_proportions):
            self.children_proportions.pop()
    def make_menu(self, context):
        self.menu = gtk.Menu()
        for item in self.model.get_menu():
            anitem = gtk.MenuItem(item[0])
            self.menu.append(anitem)
            anitem.connect("activate", item[1], (item[2], context))
            anitem.show()
    def fix_proportions(self):
        xpropmax = 1
        ypropmax = 1
        xmin = 0
        ymin = 0
        for p in self.children_proportions:
            xpropmax = max(xpropmax, p[0]+p[2])
            ypropmax = max(ypropmax, p[1]+p[3])
            xmin = min(xmin, p[0])
            ymin = min(ymin, p[1])
        #normalize
        xsize = xpropmax - xmin
        ysize = ypropmax - ymin
        for p in self.children_proportions:
            p[0] = p[0]/xsize - xmin/xsize
            p[2] = p[2]/xsize
            p[1] = p[1]/ysize - ymin/ysize
            p[3] = p[3]/ysize
        #self.new_child_default_w /= xsize
        #self.new_child_default_h /= ysize
        self.reconfigure()
    def conordisconnect(self, ind1, ind2, new_state):
        self.model.conordisconnect(ind1, ind2, new_state)
        #self.model.push_to_adapters()
    def get_child_proportions(self):
        return self.children_proportions
    def remove(self, proplen, ind):
        if proplen < len(self.children_proportions):
            del self.children_proportions[ind]
    def update_child_position(self, x, y, offset, ind):
        relx, rely = self.get_relative_geom(x-offset[0], y-offset[1])
        relw = self.children_proportions[ind][2]
        relh = self.children_proportions[ind][3]
        if relx + relw > 1:
            relx = 1-relw
        elif relx < 0:
            relx = 0
        if rely + relh > 1:
            rely = 1 - relh
        elif rely < 0:
            rely = 0
        self.children_proportions[ind][0] = relx
        self.children_proportions[ind][1] = rely
        self.reconfigure()
    def update_child_size(self, x, y, ind):
        point_relx, point_rely = self.get_relative_geom(x, y)
        c_relx, c_rely, c_relw, c_relh = self.children_proportions[ind]
        new_relw = point_relx - c_relx
        new_relh = point_rely - c_rely
        if new_relw < .01:
            new_relw = .01
        if new_relh < .01:
            new_relh = .01
        if c_relx + new_relw > 1:
            new_relw = 1 - c_relx
        if c_rely + new_relh > 1:
            new_relh = 1 - c_rely
        self.children_proportions[ind][2] = new_relw
        self.children_proportions[ind][3] = new_relh
        self.reconfigure()
    def in_resize_corner(self, x, y):
        if not self.hidden:
            relx, rely = self.get_relative_geom(x, y)
            if relx > (1-self.resize_prop) and rely > (1-self.resize_prop):
                return True
        return False
    def hide(self, state):
        self.hidden = state
    def get_offset(self, x, y):
        return (x - self.x, y - self.y)
    def __round(self, iterable):
        return map(lambda x: int(round(x)), iterable)
