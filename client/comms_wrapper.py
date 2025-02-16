#!/usr/bin/env python

import argparse
import zmq
import pmt
import time
import signal
import sys
from threading import Thread
from enum import Enum

running = True

class Mode(Enum):
    binary = 'binary'
    text = 'text'
    def __str__(self):
        return self.value

parser = argparse.ArgumentParser(
    prog='Communcations Wrapper',
    description='Open communication channel to GNURadio ZMQ PUSH/PULL Message TCP ports')
parser.add_argument(
    '-i', '--ip',
    type=str,
    default='localhost',
    help='ip address of running transceiver')
parser.add_argument(
    '-t', '--tx_port',
    type=int,
    default=50491,
    help='TCP port specified in ZMQ PULL Message Source')
parser.add_argument(
    '-r', '--rx_port',
    type=int,
    default=50492,
    help='TCP port specified in ZMQ PUSH Message Sink')
parser.add_argument(
    '-m', '--mode',
    type=Mode,
    default=Mode.text,
    choices=list(Mode),
    help='text uses newline characters at the end, and EOF to terminate')

args = parser.parse_args()

context = zmq.Context()
txsocket = context.socket(zmq.PUSH)
txsocket.connect(f"tcp://{args.ip}:{args.tx_port}")
rxsocket = context.socket(zmq.PULL)
rxsocket.connect(f"tcp://{args.ip}:{args.rx_port}")

def receiver():
    global running
    global rxsocket
    while running:
        try:
            rx_msg = rxsocket.recv(zmq.NOBLOCK)
            rx_pdu = pmt.deserialize_str(rx_msg)
            rx_pmt = pmt.cdr(rx_pdu)
            rx_arr = pmt.u8vector_elements(rx_pmt)
            if(args.mode == Mode.binary):
                sys.stdout.buffer.write(bytes(rx_arr))
                sys.stdout.buffer.flush()
            elif(args.mode == Mode.text):
                rx_str = "".join(chr(c) for c in rx_arr)
                print(rx_str)
                sys.stdout.flush()
            else: continue
        except zmq.ZMQError:
            time.sleep(0.01)
        except: pass

t_receiver = Thread(target=receiver)

def end_handler(sig=None, frame=None):
    global running
    running = False
    t_receiver.join()
    sys.exit(0)

signal.signal(signal.SIGINT, end_handler)
signal.signal(signal.SIGTERM, end_handler)
signal.signal(signal.SIGPIPE, end_handler)

t_receiver.start()

while running:
    try:
        tx_arr = None
        if(args.mode == Mode.binary):
            tx_arr = list(sys.stdin.buffer.read1())
        elif(args.mode == Mode.text):
            tx_str = input()
            tx_arr = [ord(c) for c in tx_str]
        else: continue
        if(len(tx_arr) == 0):
            time.sleep(0.01)
            continue
        tx_pmt = pmt.init_u8vector(len(tx_arr), tx_arr);
        tx_pdu = pmt.cons(pmt.PMT_NIL, tx_pmt);
        tx_msg = pmt.serialize_str(tx_pdu)
        txsocket.send(tx_msg)
    except EOFError:
        end_handler()
    except: pass
