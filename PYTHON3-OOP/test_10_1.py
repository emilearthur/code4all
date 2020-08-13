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
import gzip
from io import BytesIO

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


# Creating a pair of decorators that customize the socket behavior without having to extend or modify the soscket itself. 
class LogSocket:
    """A class which decorates a socket object and presents the send and close interface to client sockets. 
    """
    def __init__(self, socket):
        self.socket = socket 
    
    def send(self, data):
        print("Sending {0} to {1}".format(data, self.socket.getpeername()[0]))
        self.socket.send(data)
    
    def close(self):
        self.socket.close()

# creating a decorator that compresses data using gzip compression whenever send method is called. 
class GzipSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self,data):
        buf = BytesIO() 
        zipfile = gzip.GzipFile(fileobj=buf, mode="w") 
        zipfile.write(data) 
        zipfile.close() 
        self.socket.send(buf.getvalue())
    
    def close(self):
        self.socket.close()

try:
    while True:
        client, addr = server.accept() 
        respond(LogSocket(client))
        """
        modified version of code above
        
        client, addr = server.accept()
        if log_send:
            client = LogSocket(client)
        if client.getpeername()[0] in compress_hosts:
            client = GzipSocket(client)
        respond(client)

        Notes of code above:
        This code checks a hypothetical configuration variable named log_send. If it's enabled, it
        wraps the socket in a LogSocket decorator. Similarly, it checks whether the client that has
        connected is in a list of addresses known to accept compressed content. If so, it wraps the
        client in a GzipSocket decorator.

        """
finally:
    server.close()

# run socket_client.py in another terminal to make this code work. 

"""
Notes. 
respond function accepts a socket parameter and prompts for data to be sent as reply, then sends it. 
To use it, we construct a server socket and tell it to listen on port 2401
(I picked the port randomly) on the local computer. When a client connects, it calls the
respond function, which requests data interactively and responds appropriately. The
important thing to notice is that the respond function only cares about two methods of the
socket interface: send and close.

Creating a pair of decorators that customize the socket behavior without having to extend or modify the soscket itself. 
above. 

When faced with a choice between decorators and inheritance, we should only use
decorators if we need to modify the object dynamically, according to some condition. For
example, we may only want to enable the logging decorator if the server is currently in
debugging mode. Decorators also beat multiple inheritance when we have more than one
optional behavior.

"""
