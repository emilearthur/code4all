"""
A completely different way to setup variable:
One of the most common uses for the various setup and teardown functions is to ensure certain class or module variables 
are available with a known value before each test method is run. 

pytest offers a completely diferrent way of doing this using what are known as fixtures. Fixtures are named variables 
that are predefined in a test configuration file. This allows us to seperate conf. from execution of tests and allows 
fixtures to be used acrosss multiple classes and modules. 

To use them, we add parameters to our test function. The names of the parameters are used to lookup specific args in 
specially named functions. 

Eg. below
"""
import pytest 
from code_sample import StatsList 

@pytest.fixture 
def valid_stats():
    return StatsList([1,2,2,3,3,4]) 

def test_mean(valid_stats):
    assert valid_stats.mean() == 2.5

def test_median(valid_stats):
    assert valid_stats.median() == 2.5
    valid_stats.append(4) 
    assert valid_stats.median() == 3 

def test_mode(valid_stats):
    assert valid_stats.mode() == [2,3] 
    valid_stats.remove(2) 
    assert valid_stats.mode() == [3]


"""
Fixtures can do more than return basic variables. A request object can be passed into the 
factory to provide extremely useful methods and attributes to modify the funcarg's
behaviour. The module, cls and func. attribute allow us to see what exactly which test 
is requesting the fixture. The config attribute allows us to check cmd args and a great 
deal of other config data. 

If we implement the fixture as a generator, we can run cleanu code after each test is run. This provides an equivalent 
of a teardown method, except on a per-fixture basis. We can use it to clean up files, close connnections, empty list or 
reset queues. 

Eg. below: code test os.mkdir functionality by creating a temporary directory fixture. 
"""
import pytest
import tempfile 
import shutil 
import os.path 

@pytest.fixture 
def temp_dir(request):
    """
    Fixture creates a new empty temp direcotry for files to be created in. It yields this for use in the test, but removes 
    that direcotry (using shutil.rmtree, which recursively removes a direcotry and anythin inside it) after the test has 
    completed. The filesys is then left in the same state in which it started. 

    """
    dir = tempfile.mkdtemp() 
    print(dir) 
    yield dir 
    shutil.rmtree(dir)

def test_osfiles(temp_dir):
    os.mkdir(os.path.join(temp_dir, "a")) 
    os.mkdir(os.path.join(temp_dir, "b")) 
    dir_contents = os.listdir(temp_dir) 
    assert len(dir_contents) == 2
    assert "a" in dir_contents 
    assert "b" in dir_contents

"""
we can pass a scope parameter to create a fixture that lasts longer than one test. This is useful when setting up an 
expensive operatino that can be reused by multiple tests, as long as the resource reuse doesn't break the atomic or unit 
nature of the tests.  

CHECK echo_server.py and test_echo_server.py
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