
import pmt
import zmq
from subprocess import Popen

class _ESTTC_TX_Wrapper:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.connect('tcp://10.0.7.38:50491')
    
    def __del__(self):
        # self.tx_flowgraph.terminate()
        self.socket.close()
        self.context.term()
    
    def __call__(self, message):
        if isinstance(message, str):
            message = [ord(c) for c in message]
        message = pmt.init_u8vector(len(message), message)
        message = pmt.cons(pmt.PMT_NIL, message)
        message = pmt.serialize_str(message)
        self.socket.send(message)

class _ESTTC_RX_Wrapper:
    def __init__(self):
        self.interpret_as_string = True
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://10.0.7.38:50492')
    
    def __del__(self):
        self.socket.close()
        self.context.term()
    
    def __call__(self):
        message = self.socket.recv()
        message = pmt.deserialize_str(message)
        message = pmt.cdr(message)
        message = pmt.u8vector_elements(message)
        if(self.interpret_as_string):
            message = ''.join(chr(c) for c in message)
        return message

    def set_interpret_as_string(val):
        self.interpret_as_string = val

esttc_tx = _ESTTC_TX_Wrapper()
esttc_rx = _ESTTC_RX_Wrapper()
