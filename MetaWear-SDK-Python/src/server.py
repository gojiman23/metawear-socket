#!/usr/bin/env python3

# import asyncio
# import websockets

# @asyncio.coroutine
# def hello(websocket, path):
#     name = yield from websocket.recv()
#     print("{}".format(name))
#     websocket.send("{}".format(name))
#     #greeting = "Hello {}!".format(name)

#     #yield from websocket.send(greeting)
#     #print("> {}".format(greeting))

# start_server = websockets.serve(hello, 'localhost', 8764)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

import socket
import json
from multiprocessing import Process

def on_new_client(conn):
    while True:
        data = conn.recv(1024)
        if data:
            if data == "quit":
                break
            else:
                print(json.loads(data))


HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server created, waiting for clients...')

try:
    s.bind((HOST, PORT))
    print('Socket bind successful')
except socket.error as err:
    print('Bind failed. Error code : ' .format(err))

s.listen()

conn, addr = s.accept()
print("%s:%d connected." % addr)

while True:
    data = conn.recv(1024)
    if not data:
        break  
    print(json.loads(data))

s.close()