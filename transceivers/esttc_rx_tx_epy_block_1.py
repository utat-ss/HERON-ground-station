"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import sys
from gnuradio import gr
import pmt

sys.path.append('/home/heron/toptek-control/python')
from toptek import Toptek

class blk(gr.sync_block):
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, serial_port:str="/dev/ttyAmplifier"):
        gr.sync_block.__init__(
            self,
            name='Toptek Control',
            in_sig=None,
            out_sig=None
        )
        self.amp = Toptek(serial_port)
        self.message_port_register_in(pmt.intern('pa'))
        self.message_port_register_in(pmt.intern('da'))
        self.message_port_register_in(pmt.intern('lna'))
        self.message_port_register_in(pmt.intern('tx_pwr'))
        self.set_msg_handler(pmt.intern('pa'), self.pa_handler)
        self.set_msg_handler(pmt.intern('da'), self.da_handler)
        self.set_msg_handler(pmt.intern('lna'), self.lna_handler)
        self.set_msg_handler(pmt.intern('tx_pwr'), self.tx_pwr_handler)
        self.log = gr.logger(self.alias())
    
    def pa_handler(self, msg):
        try:
            state = pmt.to_bool(pmt.cdr(msg))
            if state:
                self.amp.pa_on()
            else:
                self.amp.pa_off()
        except ValueError:
            pass
    
    def da_handler(self, msg):
        try:
            state = pmt.to_bool(pmt.cdr(msg))
            if state:
                self.amp.da_on()
            else:
                self.amp.da_off()
        except ValueError:
            pass
    
    def lna_handler(self, msg):
        try:
            state = pmt.to_bool(pmt.cdr(msg))
            if state:
                self.amp.lna_on()
            else:
                self.amp.lna_off()
        except ValueError:
            pass
    
    def tx_pwr_handler(self, msg):
        try:
            pwr = pmt.to_long(pmt.cdr(msg))
        except ValueError:
            return
        try:
            self.amp.set_tx_power(pwr)
            self.log.info(f"tx power set: {pwr}")
        except (ValueError,RuntimeError) as e:
            self.log.warn(f"{e}")
    

    def work(self, input_items, output_items):
        return 0
