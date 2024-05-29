#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: HackRF Remote Control
# Author: Swarnava Ghosh
# Copyright: University of Toronto Aerospace Team
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import sip



class hackrf_remote_control(gr.top_block, Qt.QWidget):

    def __init__(self, base_port=52000, ip='10.0.7.91'):
        gr.top_block.__init__(self, "HackRF Remote Control", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("HackRF Remote Control")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "hackrf_remote_control")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.base_port = base_port
        self.ip = ip

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1
        self.tx_vga_gain = tx_vga_gain = 47
        self.tx_pwr = tx_pwr = 20
        self.tx_amp = tx_amp = True
        self.stream_port = stream_port = base_port+1
        self.squelch_threshold = squelch_threshold = -50
        self.samp_rate = samp_rate = 4e6
        self.rx_vga_gain = rx_vga_gain = 50
        self.rx_if_gain = rx_if_gain = 40
        self.rx_freq_offset = rx_freq_offset = 100e3
        self.rx_amp = rx_amp = True
        self.pa = pa = False
        self.lna = lna = False
        self.freq = freq = 435e6
        self.da = da = False
        self.control_port = control_port = base_port

        ##################################################
        # Blocks
        ##################################################

        self.control_tab = Qt.QTabWidget()
        self.control_tab_widget_0 = Qt.QWidget()
        self.control_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tab_widget_0)
        self.control_tab_grid_layout_0 = Qt.QGridLayout()
        self.control_tab_layout_0.addLayout(self.control_tab_grid_layout_0)
        self.control_tab.addTab(self.control_tab_widget_0, 'Control')
        self.control_tab_widget_1 = Qt.QWidget()
        self.control_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tab_widget_1)
        self.control_tab_grid_layout_1 = Qt.QGridLayout()
        self.control_tab_layout_1.addLayout(self.control_tab_grid_layout_1)
        self.control_tab.addTab(self.control_tab_widget_1, 'SDR Amps')
        self.control_tab_widget_2 = Qt.QWidget()
        self.control_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tab_widget_2)
        self.control_tab_grid_layout_2 = Qt.QGridLayout()
        self.control_tab_layout_2.addLayout(self.control_tab_grid_layout_2)
        self.control_tab.addTab(self.control_tab_widget_2, 'Toptek')
        self.control_tab_widget_3 = Qt.QWidget()
        self.control_tab_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.control_tab_widget_3)
        self.control_tab_grid_layout_3 = Qt.QGridLayout()
        self.control_tab_layout_3.addLayout(self.control_tab_grid_layout_3)
        self.control_tab.addTab(self.control_tab_widget_3, 'Misc')
        self.top_grid_layout.addWidget(self.control_tab, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, "tcp://"+ip+":52001", 100, False, (-1), '', False)
        self.zeromq_push_msg_sink_0 = zeromq.push_msg_sink("tcp://"+ip+":"+str(control_port), 100, False)
        self._volume_range = qtgui.Range(0, 10, 0.1, 1, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_3.addWidget(self._volume_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.control_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_3.setColumnStretch(c, 1)
        self._tx_vga_gain_range = qtgui.Range(0, 47, 1, 47, 200)
        self._tx_vga_gain_win = qtgui.RangeWidget(self._tx_vga_gain_range, self.set_tx_vga_gain, "TX VGA Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_1.addWidget(self._tx_vga_gain_win, 0, 2, 1, 2)
        for r in range(0, 1):
            self.control_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 4):
            self.control_tab_grid_layout_1.setColumnStretch(c, 1)
        # Create the options list
        self._tx_pwr_options = [20, 40, 60, 80]
        # Create the labels list
        self._tx_pwr_labels = ['20', '40', '60', '80']
        # Create the combo box
        # Create the radio buttons
        self._tx_pwr_group_box = Qt.QGroupBox("TX Power" + ": ")
        self._tx_pwr_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._tx_pwr_button_group = variable_chooser_button_group()
        self._tx_pwr_group_box.setLayout(self._tx_pwr_box)
        for i, _label in enumerate(self._tx_pwr_labels):
            radio_button = Qt.QRadioButton(_label)
            self._tx_pwr_box.addWidget(radio_button)
            self._tx_pwr_button_group.addButton(radio_button, i)
        self._tx_pwr_callback = lambda i: Qt.QMetaObject.invokeMethod(self._tx_pwr_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._tx_pwr_options.index(i)))
        self._tx_pwr_callback(self.tx_pwr)
        self._tx_pwr_button_group.buttonClicked[int].connect(
            lambda i: self.set_tx_pwr(self._tx_pwr_options[i]))
        self.control_tab_grid_layout_2.addWidget(self._tx_pwr_group_box, 0, 1, 3, 1)
        for r in range(0, 3):
            self.control_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.control_tab_grid_layout_2.setColumnStretch(c, 1)
        _tx_amp_check_box = Qt.QCheckBox("TX RF Amplifier")
        self._tx_amp_choices = {True: True, False: False}
        self._tx_amp_choices_inv = dict((v,k) for k,v in self._tx_amp_choices.items())
        self._tx_amp_callback = lambda i: Qt.QMetaObject.invokeMethod(_tx_amp_check_box, "setChecked", Qt.Q_ARG("bool", self._tx_amp_choices_inv[i]))
        self._tx_amp_callback(self.tx_amp)
        _tx_amp_check_box.stateChanged.connect(lambda i: self.set_tx_amp(self._tx_amp_choices[bool(i)]))
        self.control_tab_grid_layout_1.addWidget(_tx_amp_check_box, 1, 2, 1, 1)
        for r in range(1, 2):
            self.control_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.control_tab_grid_layout_1.setColumnStretch(c, 1)
        self._squelch_threshold_range = qtgui.Range(-100, 0, 1, -50, 200)
        self._squelch_threshold_win = qtgui.RangeWidget(self._squelch_threshold_range, self.set_squelch_threshold, "Squelch Threshold (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_3.addWidget(self._squelch_threshold_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.control_tab_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_3.setColumnStretch(c, 1)
        self._rx_vga_gain_range = qtgui.Range(0, 62, 1, 50, 200)
        self._rx_vga_gain_win = qtgui.RangeWidget(self._rx_vga_gain_range, self.set_rx_vga_gain, "RX VGA Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_1.addWidget(self._rx_vga_gain_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.control_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.control_tab_grid_layout_1.setColumnStretch(c, 1)
        self._rx_if_gain_range = qtgui.Range(0, 40, 1, 40, 200)
        self._rx_if_gain_win = qtgui.RangeWidget(self._rx_if_gain_range, self.set_rx_if_gain, "RX IF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_1.addWidget(self._rx_if_gain_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.control_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 2):
            self.control_tab_grid_layout_1.setColumnStretch(c, 1)
        self._rx_freq_offset_range = qtgui.Range(-samp_rate/2, samp_rate/2, samp_rate/200, 100e3, 200)
        self._rx_freq_offset_win = qtgui.RangeWidget(self._rx_freq_offset_range, self.set_rx_freq_offset, "RX Offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_0.addWidget(self._rx_freq_offset_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.control_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_0.setColumnStretch(c, 1)
        _rx_amp_check_box = Qt.QCheckBox("RX RF Amplifier")
        self._rx_amp_choices = {True: True, False: False}
        self._rx_amp_choices_inv = dict((v,k) for k,v in self._rx_amp_choices.items())
        self._rx_amp_callback = lambda i: Qt.QMetaObject.invokeMethod(_rx_amp_check_box, "setChecked", Qt.Q_ARG("bool", self._rx_amp_choices_inv[i]))
        self._rx_amp_callback(self.rx_amp)
        _rx_amp_check_box.stateChanged.connect(lambda i: self.set_rx_amp(self._rx_amp_choices[bool(i)]))
        self.control_tab_grid_layout_1.addWidget(_rx_amp_check_box, 1, 3, 1, 1)
        for r in range(1, 2):
            self.control_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(3, 4):
            self.control_tab_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            48e3, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 1, 6, 2)
        for r in range(0, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            48e3, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 5, 1)
        for r in range(1, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        _pa_check_box = Qt.QCheckBox("PA")
        self._pa_choices = {True: True, False: False}
        self._pa_choices_inv = dict((v,k) for k,v in self._pa_choices.items())
        self._pa_callback = lambda i: Qt.QMetaObject.invokeMethod(_pa_check_box, "setChecked", Qt.Q_ARG("bool", self._pa_choices_inv[i]))
        self._pa_callback(self.pa)
        _pa_check_box.stateChanged.connect(lambda i: self.set_pa(self._pa_choices[bool(i)]))
        self.control_tab_grid_layout_2.addWidget(_pa_check_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.control_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_2.setColumnStretch(c, 1)
        _lna_check_box = Qt.QCheckBox("LNA")
        self._lna_choices = {True: True, False: False}
        self._lna_choices_inv = dict((v,k) for k,v in self._lna_choices.items())
        self._lna_callback = lambda i: Qt.QMetaObject.invokeMethod(_lna_check_box, "setChecked", Qt.Q_ARG("bool", self._lna_choices_inv[i]))
        self._lna_callback(self.lna)
        _lna_check_box.stateChanged.connect(lambda i: self.set_lna(self._lna_choices[bool(i)]))
        self.control_tab_grid_layout_2.addWidget(_lna_check_box, 1, 0, 1, 1)
        for r in range(1, 2):
            self.control_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_2.setColumnStretch(c, 1)
        self._freq_range = qtgui.Range(420e6, 450e6, 250e3, 435e6, 200)
        self._freq_win = qtgui.RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter", float, QtCore.Qt.Horizontal)
        self.control_tab_grid_layout_0.addWidget(self._freq_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.control_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_0.setColumnStretch(c, 1)
        _da_check_box = Qt.QCheckBox("DA")
        self._da_choices = {True: True, False: False}
        self._da_choices_inv = dict((v,k) for k,v in self._da_choices.items())
        self._da_callback = lambda i: Qt.QMetaObject.invokeMethod(_da_check_box, "setChecked", Qt.Q_ARG("bool", self._da_choices_inv[i]))
        self._da_callback(self.da)
        _da_check_box.stateChanged.connect(lambda i: self.set_da(self._da_choices[bool(i)]))
        self.control_tab_grid_layout_2.addWidget(_da_check_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.control_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.control_tab_grid_layout_2.setColumnStretch(c, 1)
        self.blocks_var_to_msg_0_3_1_0_1_0 = blocks.var_to_msg_pair('tx_pwr')
        self.blocks_var_to_msg_0_3_1_0_1 = blocks.var_to_msg_pair('da')
        self.blocks_var_to_msg_0_3_1_0_0 = blocks.var_to_msg_pair('lna')
        self.blocks_var_to_msg_0_3_1_0 = blocks.var_to_msg_pair('pa')
        self.blocks_var_to_msg_0_3_1 = blocks.var_to_msg_pair('rx_amp')
        self.blocks_var_to_msg_0_3_0 = blocks.var_to_msg_pair('tx_amp')
        self.blocks_var_to_msg_0_3 = blocks.var_to_msg_pair('volume')
        self.blocks_var_to_msg_0_2 = blocks.var_to_msg_pair('rx_if_gain')
        self.blocks_var_to_msg_0_1_0 = blocks.var_to_msg_pair('tx_vga_gain')
        self.blocks_var_to_msg_0_1 = blocks.var_to_msg_pair('squelch_threshold')
        self.blocks_var_to_msg_0_0_0 = blocks.var_to_msg_pair('rx_vga_gain')
        self.blocks_var_to_msg_0_0 = blocks.var_to_msg_pair('rx_freq_offset')
        self.blocks_var_to_msg_0 = blocks.var_to_msg_pair('freq')


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_var_to_msg_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_0_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_1, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_1_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_2, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3_1, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3_1_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3_1_0_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3_1_0_1, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.blocks_var_to_msg_0_3_1_0_1_0, 'msgout'), (self.zeromq_push_msg_sink_0, 'in'))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "hackrf_remote_control")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_base_port(self):
        return self.base_port

    def set_base_port(self, base_port):
        self.base_port = base_port
        self.set_control_port(self.base_port)
        self.set_stream_port(self.base_port+1)

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_var_to_msg_0_3.variable_changed(self.volume)

    def get_tx_vga_gain(self):
        return self.tx_vga_gain

    def set_tx_vga_gain(self, tx_vga_gain):
        self.tx_vga_gain = tx_vga_gain
        self.blocks_var_to_msg_0_1_0.variable_changed(self.tx_vga_gain)

    def get_tx_pwr(self):
        return self.tx_pwr

    def set_tx_pwr(self, tx_pwr):
        self.tx_pwr = tx_pwr
        self._tx_pwr_callback(self.tx_pwr)
        self.blocks_var_to_msg_0_3_1_0_1_0.variable_changed(self.tx_pwr)

    def get_tx_amp(self):
        return self.tx_amp

    def set_tx_amp(self, tx_amp):
        self.tx_amp = tx_amp
        self._tx_amp_callback(self.tx_amp)
        self.blocks_var_to_msg_0_3_0.variable_changed(self.tx_amp)

    def get_stream_port(self):
        return self.stream_port

    def set_stream_port(self, stream_port):
        self.stream_port = stream_port

    def get_squelch_threshold(self):
        return self.squelch_threshold

    def set_squelch_threshold(self, squelch_threshold):
        self.squelch_threshold = squelch_threshold
        self.blocks_var_to_msg_0_1.variable_changed(self.squelch_threshold)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_vga_gain(self):
        return self.rx_vga_gain

    def set_rx_vga_gain(self, rx_vga_gain):
        self.rx_vga_gain = rx_vga_gain
        self.blocks_var_to_msg_0_0_0.variable_changed(self.rx_vga_gain)

    def get_rx_if_gain(self):
        return self.rx_if_gain

    def set_rx_if_gain(self, rx_if_gain):
        self.rx_if_gain = rx_if_gain
        self.blocks_var_to_msg_0_2.variable_changed(self.rx_if_gain)

    def get_rx_freq_offset(self):
        return self.rx_freq_offset

    def set_rx_freq_offset(self, rx_freq_offset):
        self.rx_freq_offset = rx_freq_offset
        self.blocks_var_to_msg_0_0.variable_changed(self.rx_freq_offset)

    def get_rx_amp(self):
        return self.rx_amp

    def set_rx_amp(self, rx_amp):
        self.rx_amp = rx_amp
        self._rx_amp_callback(self.rx_amp)
        self.blocks_var_to_msg_0_3_1.variable_changed(self.rx_amp)

    def get_pa(self):
        return self.pa

    def set_pa(self, pa):
        self.pa = pa
        self._pa_callback(self.pa)
        self.blocks_var_to_msg_0_3_1_0.variable_changed(self.pa)

    def get_lna(self):
        return self.lna

    def set_lna(self, lna):
        self.lna = lna
        self._lna_callback(self.lna)
        self.blocks_var_to_msg_0_3_1_0_0.variable_changed(self.lna)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.blocks_var_to_msg_0.variable_changed(self.freq)

    def get_da(self):
        return self.da

    def set_da(self, da):
        self.da = da
        self._da_callback(self.da)
        self.blocks_var_to_msg_0_3_1_0_1.variable_changed(self.da)

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
        "--ip", dest="ip", type=str, default='10.0.7.91',
        help="Set IP Address [default=%(default)r]")
    return parser


def main(top_block_cls=hackrf_remote_control, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(base_port=options.base_port, ip=options.ip)

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
