
import numpy as np
from gnuradio import gr
import pmt
import time
import sys

# sys.path.append('/home/heron/toptek-control/python')
# from toptek import Toptek


SLEEPY_TIME = 0.05

class blk(gr.sync_block):
    """Emulates push-to-talk by switching Tx HackRF gain on when Tx message is registered"""

    def __init__(self, baud_rate=9600, padding_nbytes=10, delay_s=0, extra_s=0):
        gr.sync_block.__init__(
            self,
            name='PTT',
            in_sig=None,
            out_sig=None
        )
        self.baud_rate = baud_rate
        self.padding_nbytes = padding_nbytes
        self.delay = delay_s
        self.extra = extra_s
        self.message_port_register_in(pmt.intern('tx_mag'))
        self.message_port_register_out(pmt.intern('tx_amp'))
        self.message_port_register_out(pmt.intern('tx_vga_gain'))
        self.message_port_register_out(pmt.intern('pa'))
        self.message_port_register_out(pmt.intern('da'))
        self.message_port_register_out(pmt.intern('lna'))
        self.set_msg_handler(pmt.intern('tx_mag'), self.handle_msg)
        self.message_port_pub(
            pmt.intern('pa'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_T))
        self.message_port_pub(
            pmt.intern('lna'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_T))

    def handle_msg(self, msg):
        msg = pmt.cdr(msg)
        msg = pmt.u8vector_elements(msg)
        length = (len(msg)+self.padding_nbytes)*8
        tx_time = length/self.baud_rate + self.extra
        time.sleep(self.delay)
        # self.amp.da_on()
        self.message_port_pub(
            pmt.intern('da'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_T))
        # self.message_port_pub(
        #    pmt.intern("tx_amp"),
        #    pmt.cons(pmt.intern("tx_amp"), pmt.PMT_T))
        # self.message_port_pub(
        #    pmt.intern("tx_vga_gain"),
        #    pmt.cons(pmt.intern("tx_vga_gain"), pmt.to_pmt(47)))
        time.sleep(tx_time)
        self.message_port_pub(
            pmt.intern('da'),
            pmt.cons(pmt.PMT_NIL, pmt.PMT_F))
        # self.amp.da_off()
        #self.message_port_pub(
        #    pmt.intern("tx_amp"),
        #    pmt.cons(pmt.intern("tx_amp"), pmt.PMT_F))
        #self.message_port_pub(
        #    pmt.intern("tx_vga_gain"),
        #    pmt.cons(pmt.intern("tx_vga_gain"), pmt.to_pmt(0)))

    def work(self, input_items, output_items):
        return 0
