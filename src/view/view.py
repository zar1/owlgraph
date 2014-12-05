import pygtk
import gtk
import gobject

from graphView.views.root import Root

from statusUpdater import Status_Updater
from owlgraph import VERSION

class View:
    dialog_modes = {'save':gtk.FILE_CHOOSER_ACTION_SAVE, 'load':gtk.FILE_CHOOSER_ACTION_OPEN}
    filter_instructions = {'ogr': ('Owl Graph Files', (), ('*.ogr',)),
                            'pic': ('Images', ('image/png', 'image/jpeg'), ('*.png', '*.jpe', '*.jpeg', '*.jpg')),
                            'all': ('All Files', (), ('*'))}
    def __init__(self, model):
        self.model = model
    def init_gui(self):
        
        self.left_clicked = False
        self.in_motion = False
        #clock
        self.draw_rate = 1.0/13.0
        self.recalc_rate = .05
        self.tick = min(self.draw_rate, self.recalc_rate)
        self.draw_ticks = int(round(self.draw_rate/self.tick))
        self.recalc_ticks = int(round(self.recalc_rate/self.tick))
        self.draw_cycle = 0
        self.recalc_cycle = 0
        
        gtk.window_set_default_icon_from_file('logo/logo.png')
        
        self.w = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.w.connect("destroy", self.quit)
        self.w.set_default_size(800, 640)
        self.w.set_title("Owl Graph")
        #self.w.set_icon_from_file("logo/logosm.png")
        
        self.vBox = gtk.VBox(False, 0)
        self.w.add(self.vBox)
        self.vBox.show()
        
        self.uim = gtk.UIManager()
        accel = self.uim.get_accel_group()
        self.w.add_accel_group(accel)
        menugrp = gtk.ActionGroup('menu')
        menugrp.add_actions([('File', None, '_File'),
                             ('New', None, '_New', '<Control>N', None, self.new),
                             ('Save', None, '_Save Workspace', '<Control>S', None, self.save),
                             ('SaveAs', None, 'Save Workspace _As', None, None, self.save_as),
                             ('Load', None, '_Open Workspace', '<Control>O', None, self.load),
                             ('SavePicture', None, 'Export As _Picture', None, None, self.save_picture),
                             ('Quit', None, '_Quit', '<Control>Q', None, self.quit),
                             ('Help', None, '_Help'),
                             ('OHelp', None, 'Owlgraph _Help', None, None, self.help),
                             ('About', None, '_About Owl Graph', None, None, self.about)])
        self.uim.insert_action_group(menugrp, 0)
        self.uim.add_ui_from_file('src/view/ui.xml')
        self.uim.ensure_update()
        self.menu_bar = self.uim.get_toplevels('menubar')[0]
        self.vBox.pack_start(self.menu_bar, False, False)
        self.menu_bar.show()
        
        self.d = gtk.DrawingArea()
        self.d.set_events(gtk.gdk.BUTTON_PRESS_MASK
                            |gtk.gdk.EXPOSURE_MASK)
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.add_with_viewport(self.d)
        self.vBox.pack_start(self.sw, True, True)
        self.sw.show()
        self.d.show()
        self.d.connect("button_press_event", self.button_press_event)
        self.d.connect("expose_event", self.expose_event)
        self.d.connect("configure_event", self.configure_event)
        self.d.connect("motion_notify_event", self.motion_notify_event)
        self.d.connect("button_release_event", self.button_release_event)
        self.d.set_events(gtk.gdk.EXPOSURE_MASK
                            | gtk.gdk.LEAVE_NOTIFY_MASK
                            | gtk.gdk.BUTTON_PRESS_MASK
                            | gtk.gdk.BUTTON_RELEASE_MASK
                            | gtk.gdk.POINTER_MOTION_MASK
                            | gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.status = gtk.Statusbar()
        self.vBox.pack_end(self.status, False, False)
        #self.status_updater = self.Status_Updater(self.status, "Waiting on:")
        self.status.show()
        
        self.pixmap = None
        self.pl = None
        #self.box.set_transforms(self.model.get_transforms()) 
        #self.w.show()
    
    def get_status_updater(self):
        return Status_Updater(self.status, "Waiting on:")
    def main(self):
        gobject.timeout_add(int(round(self.tick*1000)), self.do_tick)
        self.w.show()
        gtk.main()
        return 0
    def button_press_event(self, widget, event):
        x, y, width, height = widget.get_allocation()
        if event.button == 1:
            self.left_clicked=True
            self.model.drag_motion_start(event.x, event.y)
        elif event.button == 3:
            self.model.context_menu(event)
    def button_release_event(self, widget, event):
        if event.button==1:
            if not self.in_motion:
                self.model.select(event.x, event.y)
            self.in_motion=False
            self.left_clicked = False
            self.model.drag_motion_stop()
        return True
    def motion_notify_event(self, widget, event):
        if self.left_clicked:
            self.model.drag_motion_go(event.x, event.y)
            self.in_motion = True
        return True
    def do_tick(self):
        if self.draw_cycle > self.draw_ticks:
            self.all_redraw()
            self.draw_cycle = 0
        if self.recalc_cycle > self.recalc_ticks:
            self.model.recalc()
            self.recalc_cycle = 0
        self.draw_cycle += 1
        self.recalc_cycle += 1
        return True
    def all_redraw(self):
        x, y, width, height = self.d.get_allocation()
        self.redraw(self.d, 0, 0, width, height)
    def configure_event(self, widget, event):
        x, y, width, height = widget.get_allocation()
        self.pixmap = gtk.gdk.Pixmap(widget.window, width, height)
        self.pl = widget.create_pango_layout("")        
        self.model.configure_event((self.pixmap, self.pl), (x, y, width, height))
        self.redraw(widget, x, y, width, height)
        return True        
    def redraw(self, widget, x, y, width, height):
        self.pixmap.draw_rectangle(widget.get_style().white_gc, True, 0, 0, width, height)
        self.model.draw(widget)
        self.d.window.invalidate_rect((x, y, width, height), True)
    def expose_event(self, widget, event):
        x, y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                self.pixmap, x, y, x, y, width, height)
        return False
    def save_picture(self, action):
        size = self.pixmap.get_size()
        width, height = size
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, size[0], size[1])
        pb.get_from_drawable(self.pixmap, self.pixmap.get_colormap(), 0, 0, 0, 0, width, height)
        self.model.save_picture(pb)
    def __add_filters(self, dialog, instructions):
        filter = gtk.FileFilter()
        filter.set_name(instructions[0])
        for mime in instructions[1]:
            filter.add_mime_type(mime)
        for pattern in instructions[2]:
            filter.add_pattern(pattern)
        dialog.add_filter(filter)
    def save_dialog(self, dialog_title, mode):
        import os, sys
        d = gtk.FileChooserDialog(title=dialog_title, action = self.dialog_modes[mode[0]], buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        d.set_default_response(gtk.RESPONSE_OK)
        self.__add_filters(d, self.filter_instructions[mode[1]])
        self.__add_filters(d, self.filter_instructions['all'])
        d.set_filename(os.path.expanduser('~' + ('user' * (sys.platform[0:3] == 'win'))))
        r = d.run()
        fn = d.get_filename()
        d.destroy()
        if r == gtk.RESPONSE_OK:
            return fn
        return False 
    def save(self, action):
        self.model.save()
    def save_as(self, action):
        self.model.save_as()
    def load(self, action):
        self.model.load()
    def new(self, action):
        self.model.new()
    def quit(self, action):
        self.model.quit()
        gtk.main_quit()
    def help(self, action):
        self.model.help()
    def about(self, action):
        global VERSION
        d = gtk.AboutDialog()
        d.set_name('Owl Graph')
        d.set_authors(('Zachary Rubenstein',))
        d.set_version(str(VERSION[0]) + '.' + str(VERSION[1]) + '.' + str(VERSION[2]) + ('dev' + str(VERSION[3])) * (VERSION[3]>0))
        d.set_logo(None)
        d.run()
        d.destroy()
    def set_title(self, title):
        self.w.set_title(title)
    
    
