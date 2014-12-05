class ViewAdapter:
    def __init__(self):
        self.view = None
    def set_view(self, view):
        self.view = view
    def context_menu(self, event):
        self.view.context_menu(event)
    def save_dialog(self, title, mode):
        return self.view.save_dialog(title, mode)
    def set_title(self, title):
        self.view.set_title(title)
