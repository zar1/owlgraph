from ..view.view import View
from ..view.modelAdapter import ModelAdapter
from ..model.model import Model
from ..model.viewAdapter import ViewAdapter
from ..model.graphModel.graphModel import Graph_Model
from ..view.graphView.controllerAdapter import ControllerAdapter
from childFactory import ChildFactory

class Controller:
    def __init__(self):
        ma = ModelAdapter()
        va = ViewAdapter()
        self.v = View(ma)
        self.v.init_gui()
        self.fact = ChildFactory(self.v.get_status_updater())
        root = self.fact.make_child("", (0, 0, 640, 480, None, None), None, None, None)
        self.m = Model(va, root)
        va.set_view(self.v)
        ma.set_model(self.m)
        root.select(0,0)
        self.v.main()


