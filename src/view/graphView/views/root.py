from ..graphView import Graph_View
import gtk

class Root(Graph_View):
    def __init__(self, model, view_pass):
        
        Graph_View.__init__(self, model, view_pass)
        self.zoom = 1
        self.new_child_default_w = .4
        self.new_child_default_h = .4
        #self.new_graph(None, (None, self.Context(0,0)))  
    def draw_help(self, widget, gc):
        widget.queue_draw_area(0, 0, self.width, self.height)
    def new_graph_dialog(self):
        d = gtk.Dialog("New Graph", None, gtk.DIALOG_DESTROY_WITH_PARENT,
                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                        gtk.STOCK_OK, gtk.RESPONSE_OK))
        d.get_action_area().get_children()[0].grab_focus()
        adj1 = gtk.Adjustment(value=0, lower=0, upper = 20, step_incr=1, page_incr = 5)
        spin1 = gtk.SpinButton(adjustment=adj1)
        l1 = gtk.Label('Nodes:')
        adj2 = gtk.Adjustment(value=0., lower=0., upper=1., step_incr=.01, page_incr = .1)
        spin2 = gtk.SpinButton(adjustment=adj2)
        spin2.set_digits(2)
        l2 = gtk.Label('Connection Probability:')
        for w in (l1, spin1, l2, spin2):
            d.vbox.pack_start(w, False, False)
            w.show()
        r = d.run()
        nodes = spin1.get_value_as_int()
        prob = spin2.get_value()
        d.destroy()
        if r == gtk.RESPONSE_OK:
            return (nodes, prob)
        return False
    def reset(self):
        self.new_child_default_w = .4
        self.new_child_default_h = .4
        
