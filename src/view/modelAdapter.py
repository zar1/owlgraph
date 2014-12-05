class ModelAdapter:
    def __init__(self):
        self.model = None
    def set_model(self, model):
        self.model = model
    def select(self, x, y):
        self.model.select(x, y)
    def context_menu(self, event):
        self.model.context_menu(event)
    def configure_event(self, drawing, pos):
        self.model.configure_event(drawing, pos)
    def draw(self, widget):
        self.model.draw(widget)
    def save_picture(self, pixbuf):
        self.model.save_picture(pixbuf)
    def recalc(self):
        self.model.recalc()
    def quit(self):
        self.model.quit()
    def drag_motion_start(self, x, y):
        self.model.drag_motion_start(x, y)
    def drag_motion_go(self, x, y):
        self.model.drag_motion_go(x, y)
    def drag_motion_stop(self):
        self.model.drag_motion_stop()
    def save(self):
        self.model.save()
    def save_as(self):
        self.model.save_as()
    def load(self):
        self.model.load()
    def new(self):
        self.model.new()
    def help(self):
        self.model.help()
