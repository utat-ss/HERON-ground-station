"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, baud_rate=9600):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='PTT',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.baud_rate = baud_rate
        self.message_port_register_in(pmt.intern('tx_mag'))
        self.message_port_register_out(pmt.intern('tx_amp'))
        self.message_port_register_out(pmt.intern('tx_vga_gain'))

        self.set_msg_handler(pmt.intern('tx_mag'), self.handle_msg)


    def handle_msg(self, msg):
        msg = pmt.cdr(msg)
        msg = pmt.u8vector_elements(msg)
        length = len(msg)*8 + 72
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
        """example: multiply with constant"""
        return 0
