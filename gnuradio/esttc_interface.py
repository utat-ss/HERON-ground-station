import pmt
import zmq


class ESTTCWrapper:
    TX_PORT: int = 50491
    RX_PORT: int = 50492

    def __init__(self, ip: str):
        self.ip = ip

        self.context = zmq.Context()
        self.rxsocket = self.context.socket(zmq.PULL)
        self.rxsocket.connect(f"tcp://{self.ip}:{self.RX_PORT}")

        self.txsocket = self.context.socket(zmq.PUSH)
        self.txsocket.connect(f"tcp://{self.ip}:{self.TX_PORT}")

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
