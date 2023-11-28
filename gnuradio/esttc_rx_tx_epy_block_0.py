
import numpy as np
from gnuradio import gr
import pmt
import time

class blk(gr.sync_block):
    """Emulates push-to-talk by switching Tx HackRF gain on when Tx message is registered"""

    def __init__(self, baud_rate=9600, padding_nbytes=10):
        gr.sync_block.__init__(
            self,
            name='PTT',
            in_sig=None,
            out_sig=None
        )
        self.baud_rate = baud_rate
        self.padding_nbytes = padding_nbytes
        self.message_port_register_in(pmt.intern('tx_mag'))
        self.message_port_register_out(pmt.intern('tx_amp'))
        self.message_port_register_out(pmt.intern('tx_vga_gain'))
        self.set_msg_handler(pmt.intern('tx_mag'), self.handle_msg)

    def handle_msg(self, msg):
        msg = pmt.cdr(msg)
        msg = pmt.u8vector_elements(msg)
        length = (len(msg)+self.padding_nbytes)*8 + 72
        tx_time = length/baud_rate
        self.message_port_pub(
            pmt.intern("tx_amp"),
            pmt.cons(pmt.intern("tx_amp"), True))
        self.message_port_pub(
            pmt.intern("tx_vga_gain"),
            pmt.cons(pmt.intern("tx_vga_gain"), 47))
        time.sleep(tx_time)
        self.message_port_pub(
            pmt.intern("tx_amp"),
            pmt.cons(pmt.intern("tx_amp"), False))
        self.message_port_pub(
            pmt.intern("tx_vga_gain"),
            pmt.cons(pmt.intern("tx_vga_gain"), 0))

    def work(self, input_items, output_items):
        return 0
