from ..model.graphModel.models.graph import Graph as GraphM
from ..model.graphModel.models.point import Point as PointM
from ..model.graphModel.models.root import Root as RootM

from ..view.graphView.views.graph import Graph as GraphV
from ..view.graphView.views.point import Point as PointV
from ..view.graphView.views.root import Root as RootV 

from ..view.graphView.gModelAdapter import GModelAdapter
from ..model.graphModel.gViewAdapter import GViewAdapter

from ..model.adapter.adapter import Adapter

class ChildFactory:
    child_models = {None:RootM, RootM:GraphM, GraphM:PointM, PointM:None}
    child_views = {None:RootV, RootM:GraphV, GraphM:PointV, PointM:None} 
    def __init__(self, status_updater):
        self.status_updater = status_updater    
    def make_child(self, label, view_pass, left, Adapter_Policy, parent):
        #viewpass = (x, y, width, height, pixmap, pl)
        #burden of the parent to figure out proportions and the like
        #model has burden of labels and such
        va = GViewAdapter()
        ma = GModelAdapter()
        if parent:
            key = parent.__class__
        else:
            key = parent
        leftmost = True
        if left:
            leftmost = False
        m = ChildFactory.child_models[key](va, leftmost, parent, label, self)
        v = ChildFactory.child_views[key](ma, view_pass)
        va.set_view(v)
        ma.set_model(m)
        if left:
            ad = Adapter(Adapter_Policy(left.selected_children), m, left, self.status_updater.child(""))
            left.receive_adapter(ad)
            m.set_left_adapter(ad)
        return m

