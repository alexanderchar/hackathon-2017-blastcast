# Author: Alex Char
# Date: 2017-03-11
# Title: Hackathon BlastCast Server script
#
# To invoke this script, go to the containing folder and type:
#   python blastcast_server.py
#
# To add debugging statements, append 'debug':
#   python blastcast_server.py debug
#
# This is a basic server which listens for incoming UDP connections and reprints whatever 
# message was sent. In addition, it will broadcast a global message to all known clients at a 
# set time interval.
# 
# If the client sends a message with the text "ADMIN_" appended to the beginning, the server 
# will re-broadcast the ADMIN message to all known clients.
#
# TODO: Add AT&T M2X messaging capability to record all messages sent and received, along with 
# other additional metadata such as timestamps and some kind of client ID.

import threading
import socket
import sys
from datetime import datetime
# from m2x.client import M2XClient

# M2X info
# API_KEY = '07fbc6b4f4d3ced32e164a6abdc7e866'
# DEVICE_ID = 'e8e35c4a37ae2104007fe38424be8885'

# Symbolic name meaning all available interfaces
HOST = ''

# Port number can be changed at-will
PORT = 10001

# Messages to be broadcasted to clients
globalBroadcast = b'Hello EVERYONE from the server!'

# List of clients who have connected so far
connectedClients = []

# Code for M2X connection
# m2xclient = M2XClient(key=API_KEY)
# m2xdevice = m2xclient.device(DEVICE_ID)
# msgstream = m2xdevice.stream('message')

# Debug variable (0 = off, 1 = on)
debug = 0
if (len(sys.argv) > 1):
    if (sys.argv[1] == 'debug'):
        debug = 1

# Print generic message every X intervals; broadcast to all known available clients
# 5 seconds for testing purposes, but will realistically be increased to 15 min
def broadcastGenericMessage():
    threading.Timer(5.0, broadcastGenericMessage).start()
    print('Broadcasting global message from the SERVER (every 5 seconds)')

    if debug:
        print('List of all known clients so far:')
        print(connectedClients)

    for address in connectedClients:
        sent = mySocket.sendto(globalBroadcast, address)

broadcastGenericMessage()

# Bind socket to port
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (HOST, PORT)
serverStartMsg = 'Server started on %s, port %s' % server_address
print(serverStartMsg)
mySocket.bind(server_address)

# TODO: During testing, only one of 3-5 clients we used would throw a ConnectionResetError 
# when the connection was forcibly closed. A try/catch should be added for cleaner error 
# handling.
# try:
#   <code goes here>
# except ConnectionResetError:
#   <exception code goes here>
#   connectedClients.remove(address)

# Server loop
while True:
    print('Waiting for a CLIENT to send a message...')
    data, address = mySocket.recvfrom(4096)

    print('Incoming CLIENT message from:')
    # Convert input from raw byte stream to ASCII
    data_string = data.decode('ascii')
    print(address)
    print('The CLIENT said:')
    print(data_string)
    print()

    if data:
        # Check if client is already known
        if address not in connectedClients:
            connectedClients.append(address)

        # Add message to M2X
        # msgstream.add_value(data_string, datetime.now())

        # Send ACK to single client
        response = b'Message received! The SERVER thanks you.'
        sent = mySocket.sendto(response, address)

        # Send message to ALL known clients if ADMIN message
        if data_string.split('_')[0] == 'admin':
            print('ADMIN CLIENT message received!')
            byteString = data_string.split('_')[1].encode()
            for address in connectedClients:
                sent = mySocket.sendto(byteString, address)
