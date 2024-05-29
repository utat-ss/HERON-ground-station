#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ESTTC Rx/Tx
# Author: Swarnava Ghosh
# Copyright: University of Toronto Aerospace Team
# GNU Radio version: 3.10.10.0

from gnuradio import UTAT_HERON
from gnuradio import blocks
import math
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import iio
from gnuradio import pdu
import pmt
from gnuradio import zeromq
from math import pi
import gpredict




class esttc_rx_tx(gr.top_block):

    def __init__(self, base_port=52000, iqdump='/dev/null'):
        gr.top_block.__init__(self, "ESTTC Rx/Tx", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.base_port = base_port
        self.iqdump = iqdump

        ##################################################
        # Variables
        ##################################################
        self.gfsk_sps = gfsk_sps = 5
        self.gfsk_bps = gfsk_bps = 9600
        self.gfsk_samp_rate = gfsk_samp_rate = gfsk_sps * gfsk_bps
        self.gfsk_freq_dev = gfsk_freq_dev = 2400
        self.freq = freq = 435e6
        self.tx_vga_gain = tx_vga_gain = 47
        self.tx_freq = tx_freq = freq
        self.tx_amp = tx_amp = True
        self.stream_port = stream_port = base_port+1
        self.samp_rate = samp_rate = 4e6
        self.rx_vga_gain = rx_vga_gain = 50
        self.rx_if_gain = rx_if_gain = 40
        self.rx_freq_offset = rx_freq_offset = 100e3
        self.rx_freq = rx_freq = freq
        self.rx_amp = rx_amp = True
        self.gpredict_port = gpredict_port = base_port+2
        self.gfsk_sensitivity = gfsk_sensitivity = 2*pi*gfsk_freq_dev/gfsk_samp_rate
        self.gfsk_mod_ind = gfsk_mod_ind = 2 * gfsk_freq_dev / gfsk_bps
        self.gfsk_bt = gfsk_bt = 0.5
        self.front_padding_nbytes = front_padding_nbytes = 10
        self.control_port = control_port = base_port

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_msg_sink_0 = zeromq.push_msg_sink('tcp://*:50492', 100, True)
        self.zeromq_pull_msg_source_0_3 = zeromq.pull_msg_source("tcp://*:"+str(control_port), 100, True)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://*:50491', 100, True)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, "tcp://*:"+str(stream_port), 100, False, (-1), '', True, True)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=25,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=250,
                decimation=3,
                taps=[],
                fractional_bw=0)
        self.pdu_pdu_to_tagged_stream_0_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_add_system_time_1_0 = pdu.add_system_time(pmt.intern("Rx CRC FAIL"))
        self.pdu_add_system_time_1 = pdu.add_system_time(pmt.intern("Rx"))
        self.pdu_add_system_time_0 = pdu.add_system_time(pmt.intern("Tx"))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            4,
            firdes.low_pass(
                1,
                (samp_rate/10),
                10e3,
                5e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            10,
            firdes.low_pass(
                1,
                samp_rate,
                75e3,
                25e3,
                window.WIN_HAMMING,
                6.76))
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('' if '' else iio.get_pluto_uri(), [True, True], (2**21))
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency((int(freq + rx_freq_offset + 4e3)))
        self.iio_pluto_source_0.set_samplerate(int(samp_rate))
        self.iio_pluto_source_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0.set_gain(0, 71)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('' if '' else iio.get_pluto_uri(), [True, True], (2**23), False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(20000000)
        self.iio_pluto_sink_0.set_frequency((int(freq - rx_freq_offset+4e3)))
        self.iio_pluto_sink_0.set_samplerate(int(samp_rate))
        self.iio_pluto_sink_0.set_attenuation(0, 10)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.gpredict_doppler_0 = gpredict.doppler('0.0.0.0', gpredict_port, False)
        self.gpredict_MsgPairToVar_0_2 = gpredict.MsgPairToVar(self.set_rx_if_gain)
        self.gpredict_MsgPairToVar_0_1_0_0 = gpredict.MsgPairToVar(self.set_rx_amp)
        self.gpredict_MsgPairToVar_0_1_0 = gpredict.MsgPairToVar(self.set_tx_vga_gain)
        self.gpredict_MsgPairToVar_0_0_0_0 = gpredict.MsgPairToVar(self.set_tx_amp)
        self.gpredict_MsgPairToVar_0_0_0 = gpredict.MsgPairToVar(self.set_rx_vga_gain)
        self.gpredict_MsgPairToVar_0_0 = gpredict.MsgPairToVar(self.set_rx_freq_offset)
        self.gpredict_MsgPairToVar_0 = gpredict.MsgPairToVar(self.set_freq)
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
            samples_per_symbol=int(gfsk_sps),
            sensitivity=gfsk_sensitivity,
            bt=gfsk_bt,
            verbose=False,
            log=False,
            do_unpack=True)
        self.digital_gfsk_demod_0 = digital.gfsk_demod(
            samples_per_symbol=int(gfsk_sps),
            sensitivity=gfsk_sensitivity,
            gain_mu=(175e-3),
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,
            log=False)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((0xAA, 0xAA, 0xAA), True, 1, [])
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, front_padding_nbytes, "packet_len")
        self.blocks_msgpair_to_var_1 = blocks.msg_pair_to_var(self.set_tx_freq)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_rx_freq)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_freqshift_cc_1 = blocks.rotator_cc(2.0*math.pi*(rx_freq_offset + (freq-rx_freq))/samp_rate)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*(tx_freq-freq+rx_freq_offset)/samp_rate)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, iqdump, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.UTAT_HERON_variable_filter_1_2 = UTAT_HERON.variable_filter('tx_amp')
        self.UTAT_HERON_variable_filter_1_1 = UTAT_HERON.variable_filter('tx_vga_gain')
        self.UTAT_HERON_variable_filter_1_0_1 = UTAT_HERON.variable_filter('rx_amp')
        self.UTAT_HERON_variable_filter_1_0 = UTAT_HERON.variable_filter('rx_vga_gain')
        self.UTAT_HERON_variable_filter_1 = UTAT_HERON.variable_filter('rx_if_gain')
        self.UTAT_HERON_variable_filter_0_0 = UTAT_HERON.variable_filter('rx_freq_offset')
        self.UTAT_HERON_variable_filter_0 = UTAT_HERON.variable_filter('freq')
        self.UTAT_HERON_tagged_stream_fixed_length_padder_0 = UTAT_HERON.tagged_stream_fixed_length_padder('packet_len', 8*samp_rate/gfsk_bps, (2**17), 0x01, 5)
        self.UTAT_HERON_esttc_framer_0 = UTAT_HERON.esttc_framer()
        self.UTAT_HERON_esttc_deframer_0 = UTAT_HERON.esttc_deframer(gfsk_samp_rate)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.UTAT_HERON_esttc_deframer_0, 'crc_ok'), (self.pdu_add_system_time_1, 'pdu'))
        self.msg_connect((self.UTAT_HERON_esttc_deframer_0, 'crc_fail'), (self.pdu_add_system_time_1_0, 'pdu'))
        self.msg_connect((self.UTAT_HERON_esttc_deframer_0, 'crc_ok'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.UTAT_HERON_esttc_framer_0, 'pdu_out'), (self.pdu_pdu_to_tagged_stream_0_0_0, 'pdus'))
        self.msg_connect((self.UTAT_HERON_variable_filter_0, 'out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_0, 'out'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_0, 'out'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_0_0, 'out'), (self.gpredict_MsgPairToVar_0_0, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_1, 'out'), (self.gpredict_MsgPairToVar_0_2, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_1_0, 'out'), (self.gpredict_MsgPairToVar_0_0_0, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_1_0_1, 'out'), (self.gpredict_MsgPairToVar_0_1_0_0, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_1_1, 'out'), (self.gpredict_MsgPairToVar_0_1_0, 'inpair'))
        self.msg_connect((self.UTAT_HERON_variable_filter_1_2, 'out'), (self.gpredict_MsgPairToVar_0_0_0_0, 'inpair'))
        self.msg_connect((self.gpredict_doppler_0, 'freq'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.gpredict_doppler_0, 'tx_freq'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.msg_connect((self.pdu_add_system_time_0, 'pdu'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.pdu_add_system_time_1, 'pdu'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.pdu_add_system_time_1_0, 'pdu'), (self.blocks_message_debug_0, 'log'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.UTAT_HERON_esttc_framer_0, 'pdu_in'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.pdu_add_system_time_0, 'pdu'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_0, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_0_0, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_1, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_1_0, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_1_0_1, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_1_1, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_3, 'out'), (self.UTAT_HERON_variable_filter_1_2, 'in'))
        self.connect((self.UTAT_HERON_tagged_stream_fixed_length_padder_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_freqshift_cc_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.UTAT_HERON_tagged_stream_fixed_length_padder_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_gfsk_demod_0, 0), (self.UTAT_HERON_esttc_deframer_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_freqshift_cc_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.digital_gfsk_demod_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.zeromq_pub_sink_0, 0))


    def get_base_port(self):
        return self.base_port

    def set_base_port(self, base_port):
        self.base_port = base_port
        self.set_control_port(self.base_port)
        self.set_gpredict_port(self.base_port+2)
        self.set_stream_port(self.base_port+1)

    def get_iqdump(self):
        return self.iqdump

    def set_iqdump(self, iqdump):
        self.iqdump = iqdump
        self.blocks_file_sink_0.open(self.iqdump)

    def get_gfsk_sps(self):
        return self.gfsk_sps

    def set_gfsk_sps(self, gfsk_sps):
        self.gfsk_sps = gfsk_sps
        self.set_gfsk_samp_rate(self.gfsk_sps * self.gfsk_bps)

    def get_gfsk_bps(self):
        return self.gfsk_bps

    def set_gfsk_bps(self, gfsk_bps):
        self.gfsk_bps = gfsk_bps
        self.set_gfsk_mod_ind(2 * self.gfsk_freq_dev / self.gfsk_bps)
        self.set_gfsk_samp_rate(self.gfsk_sps * self.gfsk_bps)

    def get_gfsk_samp_rate(self):
        return self.gfsk_samp_rate

    def set_gfsk_samp_rate(self, gfsk_samp_rate):
        self.gfsk_samp_rate = gfsk_samp_rate
        self.set_gfsk_sensitivity(2*pi*self.gfsk_freq_dev/self.gfsk_samp_rate)

    def get_gfsk_freq_dev(self):
        return self.gfsk_freq_dev

    def set_gfsk_freq_dev(self, gfsk_freq_dev):
        self.gfsk_freq_dev = gfsk_freq_dev
        self.set_gfsk_mod_ind(2 * self.gfsk_freq_dev / self.gfsk_bps)
        self.set_gfsk_sensitivity(2*pi*self.gfsk_freq_dev/self.gfsk_samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_rx_freq(self.freq)
        self.set_tx_freq(self.freq)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.tx_freq-self.freq+self.rx_freq_offset)/self.samp_rate)
        self.blocks_freqshift_cc_1.set_phase_inc(2.0*math.pi*(self.rx_freq_offset + (self.freq-self.rx_freq))/self.samp_rate)
        self.iio_pluto_sink_0.set_frequency((int(self.freq - self.rx_freq_offset+4e3)))
        self.iio_pluto_source_0.set_frequency((int(self.freq + self.rx_freq_offset + 4e3)))

    def get_tx_vga_gain(self):
        return self.tx_vga_gain

    def set_tx_vga_gain(self, tx_vga_gain):
        self.tx_vga_gain = tx_vga_gain

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.tx_freq-self.freq+self.rx_freq_offset)/self.samp_rate)

    def get_tx_amp(self):
        return self.tx_amp

    def set_tx_amp(self, tx_amp):
        self.tx_amp = tx_amp

    def get_stream_port(self):
        return self.stream_port

    def set_stream_port(self, stream_port):
        self.stream_port = stream_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.tx_freq-self.freq+self.rx_freq_offset)/self.samp_rate)
        self.blocks_freqshift_cc_1.set_phase_inc(2.0*math.pi*(self.rx_freq_offset + (self.freq-self.rx_freq))/self.samp_rate)
        self.iio_pluto_sink_0.set_samplerate(int(self.samp_rate))
        self.iio_pluto_source_0.set_samplerate(int(self.samp_rate))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 75e3, 25e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.samp_rate/10), 10e3, 5e3, window.WIN_HAMMING, 6.76))

    def get_rx_vga_gain(self):
        return self.rx_vga_gain

    def set_rx_vga_gain(self, rx_vga_gain):
        self.rx_vga_gain = rx_vga_gain

    def get_rx_if_gain(self):
        return self.rx_if_gain

    def set_rx_if_gain(self, rx_if_gain):
        self.rx_if_gain = rx_if_gain

    def get_rx_freq_offset(self):
        return self.rx_freq_offset

    def set_rx_freq_offset(self, rx_freq_offset):
        self.rx_freq_offset = rx_freq_offset
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(self.tx_freq-self.freq+self.rx_freq_offset)/self.samp_rate)
        self.blocks_freqshift_cc_1.set_phase_inc(2.0*math.pi*(self.rx_freq_offset + (self.freq-self.rx_freq))/self.samp_rate)
        self.iio_pluto_sink_0.set_frequency((int(self.freq - self.rx_freq_offset+4e3)))
        self.iio_pluto_source_0.set_frequency((int(self.freq + self.rx_freq_offset + 4e3)))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.blocks_freqshift_cc_1.set_phase_inc(2.0*math.pi*(self.rx_freq_offset + (self.freq-self.rx_freq))/self.samp_rate)

    def get_rx_amp(self):
        return self.rx_amp

    def set_rx_amp(self, rx_amp):
        self.rx_amp = rx_amp

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_gfsk_sensitivity(self):
        return self.gfsk_sensitivity

    def set_gfsk_sensitivity(self, gfsk_sensitivity):
        self.gfsk_sensitivity = gfsk_sensitivity

    def get_gfsk_mod_ind(self):
        return self.gfsk_mod_ind

    def set_gfsk_mod_ind(self, gfsk_mod_ind):
        self.gfsk_mod_ind = gfsk_mod_ind

    def get_gfsk_bt(self):
        return self.gfsk_bt

    def set_gfsk_bt(self, gfsk_bt):
        self.gfsk_bt = gfsk_bt

    def get_front_padding_nbytes(self):
        return self.front_padding_nbytes

    def set_front_padding_nbytes(self, front_padding_nbytes):
        self.front_padding_nbytes = front_padding_nbytes
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.front_padding_nbytes)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.front_padding_nbytes)

    def get_control_port(self):
        return self.control_port

    def set_control_port(self, control_port):
        self.control_port = control_port



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--base-port", dest="base_port", type=intx, default=52000,
        help="Set Base Port [default=%(default)r]")
    parser.add_argument(
        "--iqdump", dest="iqdump", type=str, default='/dev/null',
        help="Set iqdump [default=%(default)r]")
    return parser


def main(top_block_cls=esttc_rx_tx, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(base_port=options.base_port, iqdump=options.iqdump)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
