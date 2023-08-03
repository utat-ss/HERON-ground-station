#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.9.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class rx_debug(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "rx_debug")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.rx_rf_gain = rx_rf_gain = 14
        self.rx_if_gain = rx_if_gain = 8
        self.rx_bb_gain = rx_bb_gain = 4
        self.ppm = ppm = 14
        self.freq = freq = 435e6
        self.baud_rate = baud_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self._freq_range = Range(435e6, 438e6, 500e0, 435e6, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, 'freq', "counter", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_win)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, 'hackrf=0000000000000000a06063c8242f915f',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, freq)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(16, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(16, 0.0), 62.0))
        # Create the options list
        self._rx_rf_gain_options = [14, 0]
        # Create the labels list
        self._rx_rf_gain_labels = ['RF Gain ON', 'RF Gain OFF']
        # Create the combo box
        self._rx_rf_gain_tool_bar = Qt.QToolBar(self)
        self._rx_rf_gain_tool_bar.addWidget(Qt.QLabel("rx_rf_gain: "))
        self._rx_rf_gain_combo_box = Qt.QComboBox()
        self._rx_rf_gain_tool_bar.addWidget(self._rx_rf_gain_combo_box)
        for _label in self._rx_rf_gain_labels: self._rx_rf_gain_combo_box.addItem(_label)
        self._rx_rf_gain_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_rf_gain_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._rx_rf_gain_options.index(i)))
        self._rx_rf_gain_callback(self.rx_rf_gain)
        self._rx_rf_gain_combo_box.currentIndexChanged.connect(
            lambda i: self.set_rx_rf_gain(self._rx_rf_gain_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._rx_rf_gain_tool_bar)
        self._rx_if_gain_range = Range(0, 40, 8, 8, 200)
        self._rx_if_gain_win = RangeWidget(self._rx_if_gain_range, self.set_rx_if_gain, 'rx_if_gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_if_gain_win)
        self._rx_bb_gain_range = Range(0, 62, 2, 4, 200)
        self._rx_bb_gain_win = RangeWidget(self._rx_bb_gain_range, self.set_rx_bb_gain, 'rx_bb_gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_bb_gain_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self._ppm_range = Range(-20, 20, 0.1, 14, 200)
        self._ppm_win = RangeWidget(self._ppm_range, self.set_ppm, 'ppm', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._ppm_win)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, samp_rate, 3*baud_rate, 3.3333e3, window.WIN_HANN, 6.76), 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'home/adyn/ground-station/recordings/packets_path_packed', False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rx_debug")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 3*self.baud_rate, 3.3333e3, window.WIN_HANN, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)

    def get_rx_rf_gain(self):
        return self.rx_rf_gain

    def set_rx_rf_gain(self, rx_rf_gain):
        self.rx_rf_gain = rx_rf_gain
        self._rx_rf_gain_callback(self.rx_rf_gain)

    def get_rx_if_gain(self):
        return self.rx_if_gain

    def set_rx_if_gain(self, rx_if_gain):
        self.rx_if_gain = rx_if_gain

    def get_rx_bb_gain(self):
        return self.rx_bb_gain

    def set_rx_bb_gain(self, rx_bb_gain):
        self.rx_bb_gain = rx_bb_gain

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_hackrf_source_0.set_frequency(0, self.freq)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 3*self.baud_rate, 3.3333e3, window.WIN_HANN, 6.76))




def main(top_block_cls=rx_debug, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
