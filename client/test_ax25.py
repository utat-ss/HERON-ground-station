import esttc_interface
import ax25
import time

digi = esttc_interface.ESTTCWrapper()
msg = ax25.str2pkt('=4339.60N/07923.85W-Hello from the University of Toronto Aerospace Team', 'CQ', 'VE3SGH', 'WIDE1-1')

try:
    while True:
        digi.tx_bytes(msg)
        # print(ax25.pkt2str(digi.rx_bytes()))
        time.sleep(1)
except KeyboardInterrupt:
    print('done')