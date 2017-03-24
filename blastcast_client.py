# Author: Alex Char
# Date: 2017-03-11
# Title: Hackathon BlastCast Client script
#
# To invoke this script, go to the containing folder and type:
#   python blastcast_client.py
#
# This is a basic client to contact the BlastCast server. It sends a simple message, waits for a 
# response from the server, then closes the connection.
#
# If the text is appended by "ADMIN_", then the message will go to the server then get 
# re-broadcast to all known clients.
#
# For more info on UDP sockets, see this guide:
# https://pymotw.com/2/socket/udp.html

import socket
import sys

# Connection info
host = 'localhost'
port = 10001

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (host, port)
message = b'Hi, I am a client!'
# Sample admin message
# message = b'admin_Hi, I am an admin client!'

try:
    # Send data
    print(message)
    sent = sock.sendto(message, server_address)

    # Receive response
    print('Waiting for a response from the server...')
    data, server = sock.recvfrom(4096)
    print(data)

finally:
    print('Transmission complete, closing socket.')
    sock.close()