"""
Python Design Patterns I:

The decorator pattern:
The decorator pattern alows us to wrap an object that provides core functionality with other objects that 
alter this functionality. Any object that uses the decorated object will interact with it in exactly the 
same way as if it were undecorated(ie. the interface of the decoreated object is identical to that of the 
core object.)

Uses of decorator pattern:
* Enhancing the response of a component as it send data to a second component 
* Supporting multiple optional behaviours. 
"""


"""
Eg. of a decorator below
We create a TCP socket. The socket.send() method takes a string of input bytes and output them to the 
receiving sockt at another end. 
We create such an object; it will be an interactive shell
that waits for a connection from a client and then prompts the user for a string response
"""
import socket 

def respond(client):
    """
    sends data into a socket object
    """
    response = input("Enter a value: ") 
    client.send(bytes(response, "utf8"))
    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(("localhost", 2401)) 
server.listen(1) 

try:
    while True:
        client, addr = server.accept() 
        respond(client)
finally:
    server.close()



"""

respond function accepts a socket parameter and prompts for data to be sent as reply, then sends it. 
To use it, we construct a server socket and tell it to listen on port 2401
(I picked the port randomly) on the local computer. When a client connects, it calls the
respond function, which requests data interactively and responds appropriately. The
important thing to notice is that the respond function only cares about two methods of the
socket interface: send and close.

Creating a pair of decorators that customize the socket behavior without having to extend or modify the soscket itself. 

"""
class LogSocket:
    def __init__(self, socket):
        self.socket = socket 
    
    def send(self, data):
        print("Sending {0} to {1}".format(data, self.socket.getpeername()[0]))
        self.socket.send(data)