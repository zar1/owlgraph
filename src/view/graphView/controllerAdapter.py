class ControllerAdapter:
    def __init__(self, controller):
        self.controller = controller
    def get_model(self, view):
        return self.controller.get_model(view)
