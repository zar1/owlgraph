class Status_Updater():
        def __init__(self, stack, base_message):
            self.stack = stack
            self.base_message = base_message
            self.message_stack = {}
            self.context_id = stack.get_context_id(base_message)
            self.cur_message_id_recv = -1
            self.last_message_id_sent = self.stack.push(self.context_id, self.base_message)
        def push(self, context, message):
            self.cur_message_id_recv += 1
            self.message_stack[self.cur_message_id_recv] = message
            self.__send()
            return self.cur_message_id_recv
        def remove_message(self, context, message_id):
            del self.message_stack[message_id]
            self.__send()
        def get_context_id(self, context_description):
            return hash(context_description)
        def child(self, base_message):
            return Status_Updater(self, base_message)
        def __send(self):
            to_send = self.base_message
            for k in self.message_stack:
                m = self.message_stack[k]
                if m:
                    to_send = to_send + " " + m
            #print to_send
            self.stack.remove_message(self.context_id, self.last_message_id_sent)
            self.last_message_id_sent = self.stack.push(self.context_id, to_send)
            #self.stack.remove(self.context_id, self.last_message_id_sent)