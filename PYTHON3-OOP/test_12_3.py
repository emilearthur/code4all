"""Using pytest.

By default pytest suppress output from print statement if the test is successful. 
"""
"""
class TestNumbers:
    def test_int_float(self):
        assert 1 == 1.0
    
    def test_int_str(self):
        assert 1 == "1" 
"""

"""
One way to do setup and cleanup:
pytest suppports setup and teardown methods similar to those used in unittest, but provides more flexibility. 
If we are writing class-based tests, we can use two methods called setup_method and teardown_metod in the same way 
that setUp and tearDown are called in unittest. They are called before and after each test method in the class to perform 
setup and cleanup an argument: the func. object representing the method being called. 

Also, pytest provides other setup and cleanup code is executed. The setup_class and teardown_class methods are expected to
be class methods; they accept a single args(there is no self arg) representing the class in question. These methods are 
only run when the class is initiated rather than on each test run.
Finally, we ahve the setup_module and teardown_module funcs, which are run immediately before and after all tests(in funcs
and classses) in that module. These can be useful for one time setup such as creating a socket or db connection that will 
be used by all test in the module. 

Eg below 
"""
def setup_module(module):
    print(f"setting up MODULE {module.__name__}")

def teardown_module(module):
    print(f"tearing down MODULE {module.__name__}") 

def test_a_function():
    print("Running Test Function") 


class BaseTest:
    """Sole purpose of the BaseTest class is to extract four methods that are otherwise identical to the test classes 
    and use inheritance to reduce the amount of duplicate code.
    """
    def setup_class(cls):
        print(f"setting up class {cls.__name__}") 
    
    def teardown_class(cls):
        print(f"tearing down CLASS {cls.__name__}") 
    
    def setup_method(self, method):
        print(f"setting up METHOD {method.__name__}") 
    
    def teardown_method(self, method):
        print(f"tearing down METHOD {method.__name__}") 


class TestClass1(BaseTest):
    def test_method_1(self):
        print(f"RUNNING METHOD 1-1") 

    def test_method_2(self):
        print(f"RUNNING METHOD 1-2")
    

class TestClass2(BaseTest):
    def test_method_1(self):
        print(f"RUNNING METHOD 2-1") 
    
    def test_method_2(self):
        print(f"RUNNING METHOD 2-2")

"""
From pytest POV the two subclass above have not only two test methods each but have two step and two teardown methods
(one at the class level, one at the method level). 
"""