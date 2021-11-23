"""
A simple client that connects to the same port and outputs the response before existing 
"""

import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(("localhost",2401)) 
print("Recieved: {0}".format(client.recv(1024)))
client.close() 

