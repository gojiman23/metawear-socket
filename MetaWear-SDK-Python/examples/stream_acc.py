# usage: python stream_acc.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import platform
import sys

if sys.version_info[0] == 2:
    range = xrange

def data_handler(ctx, data):
    global samples
    print("%s" % (parse_value(data)))
    samples += 1

samples = 0

callback = FnVoid_VoidP_DataP(data_handler)


device = MetaWear("EA:5F:96:E7:1F:3D")
device.connect()
print("Connected to " + device.address)

print("Configuring device")
libmetawear.mbl_mw_settings_set_connection_parameters(device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)

libmetawear.mbl_mw_acc_set_odr(device.board, 100.0)
libmetawear.mbl_mw_acc_set_range(device.board, 16.0)
libmetawear.mbl_mw_acc_write_acceleration_config(device.board)

signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback)

libmetawear.mbl_mw_acc_enable_acceleration_sampling(device.board)
libmetawear.mbl_mw_acc_start(device.board)

sleep(30.0)

libmetawear.mbl_mw_acc_stop(device.board)
libmetawear.mbl_mw_acc_disable_acceleration_sampling(device.board)

signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(signal)
libmetawear.mbl_mw_debug_disconnect(device.board)

print("Total Samples Received")
print("%s -> %d" % (device.address, samples))
