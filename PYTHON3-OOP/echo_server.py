"""
Based on test_12_4.py

Eg below : We we test the following echo server, we may want to run only one instance of the server in a sperate process
and then hve multiple tests connect to that instance. 
"""
import socket

"""
Code below listen on a specific o
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 1028)) 
s.listen(1) 
while True:
    client, address = s.accept() 
    data = client.recv(1024) 
    client.send(data) 
    client.close()
    