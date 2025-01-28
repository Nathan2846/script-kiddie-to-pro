"""
The first exercise from Black Hat Python - a simple TCP Client
"""

import socket

target_host = '127.0.0.1'
target_port = 9998

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect
client.connect((target_host, target_port))

# Send data
client.send(b'ABCDEF')

# Recieve data
response = client.recv(4096)

print (response.decode())

client.close()