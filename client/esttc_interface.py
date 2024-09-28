import pmt
import zmq

class ESTTCWrapper:
    def __init__(self, zmq_tx: str = "tcp://localhost:50491", zmq_rx: str = "tcp://localhost:50492"):
        self.context = zmq.Context()
        self.rxsocket = self.context.socket(zmq.PULL)
        self.rxsocket.connect(zmq_rx)

        self.txsocket = self.context.socket(zmq.PUSH)
        self.txsocket.connect(zmq_tx)

    def __del__(self):
        self.rxsocket.close()
        self.txsocket.close()
        self.context.term()
    
    def set_timeout(self, t):
        self.rxsocket.setsockopt(zmq.RCVTIMEO, t)
        self.rxsocket.setsockopt(zmq.LINGER, 0)

    def tx(self, msg: str) -> None:
        message = [ord(c) for c in msg]
        message = pmt.init_u8vector(len(message), message)
        message = pmt.cons(pmt.PMT_NIL, message)
        message = pmt.serialize_str(message)
        self.txsocket.send(message)

    def tx_bytes(self, msg: bytes) -> None:
        message = pmt.init_u8vector(len(msg), msg)
        message = pmt.cons(pmt.PMT_NIL, message)
        message = pmt.serialize_str(message)
        self.txsocket.send(message)

    def rx(self, flags=0) -> str:
        message = self.rxsocket.recv(flags)
        message = pmt.deserialize_str(message)
        message = pmt.cdr(message)
        message = pmt.u8vector_elements(message)
        return "".join(chr(c) for c in message)

    def rx_bytes(self, flags=0) -> bytes:
        message = self.rxsocket.recv(flags)
        message = pmt.deserialize_str(message)
        message = pmt.cdr(message)
        return pmt.u8vector_elements(message)
