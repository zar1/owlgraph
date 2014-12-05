from numpy import *
import cPickle

from owlgraph import VERSION 

class Model:
    def __init__(self, view, graph_model):
        self.transforms = []
        self.view = view
        self.root = graph_model
        self.root.set_transforms(self.get_transforms())
        self.last_filename = None
    def get_transforms(self):
        if not self.transforms:
            self.load_transforms()
        return self.transforms
    def load_transforms(self):
        import adapter.policy.transforms
        for mod in adapter.policy.transforms.__all__:
            t = __import__('adapter.policy.transforms.' + mod, globals(), locals(), ['P'])
            self.transforms.append((t.P.name, t.P))
    def select(self, x, y):
        self.root.select(x, y)
    def context_menu(self, event):
        self.root.get_last_selected().view.context_menu(event)
    def configure_event(self, draw_refs, pos_vals):
        self.root.view.configure_event(draw_refs, pos_vals)
    def draw(self, widget):
        self.root.view.draw(widget)
    def recalc(self):
        self.root.recalc()
    def quit(self):
        self.root.quit()
    def new(self):
        self.root.new()
    def drag_motion_start(self, x, y):
        self.dragged_object = self.root.find_object(x, y, None)
        self.dragged_object.drag_start(x, y)
    def drag_motion_go(self, x, y):
        self.dragged_object.drag_to(x, y)
    def drag_motion_stop(self):
        self.dragged_object.drag_stop()
    def save_picture(self, pixbuf):
        r = self.view.save_dialog('Save as picture', ('save', 'pic'))
        if r:
            filename = r
            ext = filename[-5:]
            ext_short = ext[-4:]
            type = 'png'
            ops = {}
            if (ext_short in ['.jpg', '.jpe']) or (ext == '.jpeg'):
                type = 'jpeg'
            elif ext_short == '.png':
                pass
            else:
                filename = filename + '.png'
            pixbuf.save(filename, type, ops)
            #(fn, "png", {})
    def save(self):
        if self.last_filename:
            self.__save(self.last_filename)
        else:
            self.save_as()
    def save_as(self):
        r = self.view.save_dialog('Save Workspace As', ('save', 'ogr'))
        if r:
            if not r[-4:] == '.ogr':
                r = r + '.ogr'
            self.view.set_title('Owl Graph - ' + r)
            self.__save(r)            
    def __save(self, filename):
        f = open(filename, 'wb')
        cPickle.dump((VERSION, self.root.save()), f)
        f.close()
        self.last_filename = filename
    def load(self):
        r = self.view.save_dialog('Load Workspace', ('load', 'ogr'))
        if r:
            f = open(r, 'rb')
            env = cPickle.load(f)
            f.close()
            version = env[0]
            data = env[1]
            self.new()
            self.root.load(data)
            self.view.set_title('Owl Graph - ' + r)
    def help(self):
        import webbrowser, urllib, os, sys
        # this method for constructing the path works, at least, on Vista and Ubuntu.
        p = urllib.pathname2url(os.path.join(os.getcwd(), 'doc', 'help', 'index.html'))
        
        # There is apparently no way to make sure that webbrowser makes the correct decision for local files, 
        # so let's pray that Mr. Linux User has a properly registered firefox...
        if sys.platform[0:5] == 'linux':
            try:
                b = webbrowser.get('firefox')
            except webbrowser.Error:
                # and if God has not so favored us, we can at least pray that the platform won't choose a text editor
                # (which it probably will)
                b = webbrowser.get()
        elif sys.platform[0:3] == 'win':
            # apparently a necessary correction for urllib in windows
            p = 'file:' + p
        else:
            # Other platforms are not governed by my own deity. They can do whatever the heck they want.
            b = webbrowser.get()
        # I hope the user can render html in his/her head...    
        b.open(p)
        


