import subprocess 
import socket 
import time 
import pytest 

@pytest.fixture(scope="session") 
def echoserver():
    print("loading server") 
    p = subprocess.Popen(["python3", "echo_server.py"]) 
    time.sleep(1) 
    yield p 
    p.terminate() 
    
@pytest.fixture 
def clientsocket(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('localhost', 1028)) 
    yield s 
    s.close() 

def test_echo(echoserver, clientsocket):
    clientsocket.send(b"abc")
    assert clientsocket.recv(3) == b"abc" 

def test_echo2(echoserver, clientsocket):
    clientsocket.send(b"def") 
    assert clientsocket.recv(3) == b"def"


"""
echo server in a seperate process, and yields the process object, cleaning it up when it's finished. 
The second instantiates a new socket object for each test, and closes the socket when the test has completed.  

From the scope="session" keyword arg. passed into the decorator's constructor, pytest knows that we only want this
fixture to be initialized and terminated once for the duration of the unit test session. 

The scope can be one o the strings class, module, package or session. It determines just how long the argument will be 
cached. We set it to session in this example, so it is cached for the duration of the entire pytest run. The process will 
not be terminated or restarted until all tests have run. 

The module scope caches it only for tests in that module and the class scope treats the object more like a normal class 
setup and teardown. 
"""