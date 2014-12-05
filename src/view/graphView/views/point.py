from ..graphView import Graph_View

class Point(Graph_View):
    def __init__(self, model, viewpass):
        Graph_View.__init__(self, model, viewpass)
        self.resize_prop = .25
