from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
from websocket import create_connection

import platform
import sys
import json
import socket

if sys.version_info[0] == 2:
    range = xrange

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def data_handler(ctx, data):
    global samples
 
    #ws = create_connection("ws://localhost:65432")
    #ws.send("%s" % (parse_value(data)))
    var = json.dumps("%s" % (parse_value(data))).encode()
    s.sendall(var)
    samples+= 1

callback = FnVoid_VoidP_DataP(data_handler)
samples = 0

device = MetaWear("EA:5F:96:E7:1F:3D")
device.connect()
print("Connected to " + device.address)

print("Configuring device")
libmetawear.mbl_mw_settings_set_connection_parameters(device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)

libmetawear.mbl_mw_acc_set_odr(device.board, 100.0)         #sets output data range in Hz
libmetawear.mbl_mw_acc_set_range(device.board, 16.0)        #sets full scale range in g's
libmetawear.mbl_mw_acc_write_acceleration_config(device.board)

#retrieves and returns pointer to data signal representing acceleration data
signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback)     #subscribes to data stream, processes msgs with given handler

libmetawear.mbl_mw_acc_enable_acceleration_sampling(device.board)   #enables acceleration sampling
libmetawear.mbl_mw_acc_start(device.board)                          #switches accelerometer to active mode  

sleep(5.0)

libmetawear.mbl_mw_acc_stop(device.board)
libmetawear.mbl_mw_acc_disable_acceleration_sampling(device.board)

signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
#use rss to compress data signal?    
libmetawear.mbl_mw_datasignal_unsubscribe(signal)
libmetawear.mbl_mw_debug_disconnect(device.board)

print("Total Samples Received")
print("%s -> %d" % (device.address, samples))
