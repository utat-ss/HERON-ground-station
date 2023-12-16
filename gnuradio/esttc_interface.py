import pmt
import zmq


class ESTTCWrapper:
    def __init__(self, ip: str, tx_port: int = 50491, rx_port: int = 50492):
        self.ip = ip
        self.tx_port = tx_port
        self.rx_port = rx_port

        self.context = zmq.Context()
        self.rxsocket = self.context.socket(zmq.PULL)
        self.rxsocket.connect(f"tcp://{self.ip}:{self.rx_port}")

        self.txsocket = self.context.socket(zmq.PUSH)
        self.txsocket.connect(f"tcp://{self.ip}:{self.tx_port}")

    def __del__(self):
        self.rxsocket.close()
        self.txsocket.close()
        self.context.term()

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

    def rx(self) -> str:
        message = self.rxsocket.recv()
        message = pmt.deserialize_str(message)
        message = pmt.cdr(message)
        message = pmt.u8vector_elements(message)
        return "".join(chr(c) for c in message)

    def rx_bytes(self) -> bytes:
        message = self.rxsocket.recv()
        message = pmt.deserialize_str(message)
        message = pmt.cdr(message)
        return pmt.u8vector_elements(message)
