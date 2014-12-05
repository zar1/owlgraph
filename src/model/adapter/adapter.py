from numpy import resize, intersect1d
import sys
if (sys.platform[0:3] == 'win') or (sys.version_info[1]<6):
	from threading import Thread as Process
	from Queue import Queue
else:
    from multiprocessing import Process, Queue
from Queue import Empty, Full
from numpy import array


class Adapter:
    def __init__(self, policy, child_box, left, status_updater):
        self.policy = policy
        self.box = child_box
        self.left = left
        self.expected_size = 0
        self.available_nodes = []
        self.available_edges = []
        self.status_updater = status_updater
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.proc = Process(target=self.__push, args=(self.in_queue, self.out_queue))
        self.proc.start()
        self.last_out = ([], [])
        self.last_in = (array([]), [], [])
        self.retry = False
        self.status_context = status_updater.get_context_id("666")
        self.last_status_message_id = None
    def array_eq(self, a1, a2):
        if a1.shape == a2.shape:
            if (a1==a2).all():
                return True
        return False
    def push(self, force, model_data, proportions, active_nodes, active_edges):
        tactive_nodes, tactive_edges = self.last_out
        if not(self.array_eq(self.last_in[0], model_data)) or not(self.last_in[1] == active_nodes) or not(self.last_in[2]==active_edges) or self.retry:
        #TODO there is something wrong here
        #if True:
            if not self.retry:
                self.in_queue.put((model_data, active_nodes, active_edges))
                self.last_status_message_id = self.status_updater.push(self.status_context, self.policy.name + '->' + self.box.label)
                self.last_in = (model_data.copy(), list(active_nodes), list(active_edges))
            try:
                tactive_nodes, tactive_edges = self.out_queue.get(False)
                self.retry = False
                self.status_updater.remove_message(self.status_context, self.last_status_message_id)
            except Empty:
                self.retry = True
        ex = (self.expected_size, self.expected_size)
        if model_data.size != ex:
            model_data = resize(model_data, ex) 
        tactive_nodes = intersect1d(tactive_nodes, self.available_nodes).tolist()
        #tactive_edges = intersect1d(tactive_edges, self.available_edges).tolist()
        self.last_out = (list(tactive_nodes), list(tactive_edges))
        self.box.receive_update(force, model_data, proportions, tactive_nodes, tactive_edges)
    def __push(self, in_queue, out_queue):
        while True:
            gotten = in_queue.get(block=True, timeout=None)
            if gotten == 'quit':
                break
            model_data, active_nodes, active_edges = gotten
            tactive_nodes, tactive_edges = self.policy.transform(model_data, active_nodes, active_edges)
            out_queue.put((tactive_nodes, tactive_edges), block=False)
    def lose_node(self, ind):
        self.policy.lose_node(ind)
        self.box.lose_node(ind)
        self.available_nodes.pop()
        if self.expected_size > 1:
            self.available_edges.pop()
        self.expected_size -= 1
    def gain_node(self, label, proportions):
        self.box.gain_node(label, proportions)
        self.available_nodes.append(self.expected_size)
        if self.expected_size > 0:
            self.available_edges.append((self.expected_size-1, self.expected_size))
        self.expected_size += 1
    def quit(self):
        self.__cleanup()
        self.box.quit()
    def destroy(self):
        self.__cleanup()
        self.box.self_destruct(False)
    def orphan(self):
        self.__cleanup()
        self.left.lose_adapter(self)
    def save(self):
        return ((self.policy.name, self.policy.selected), self.box.save())
    def load(self, data, selected):
        self.policy.selected = selected
        self.box.load(data)
    def __cleanup(self):
        if self.proc.is_alive():
            self.in_queue.put('quit')
            #self.proc.join()
        if self.retry:
            self.status_updater.remove_message(self.status_context, self.last_status_message_id)
        
