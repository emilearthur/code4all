"""
Testing OO Programs: 
Testing is one of the most important aspect of software dev. 
Python test tests rarely check types as compared to C++ and Java. Python's interactive interpreter and near-zero compile 
times makes it easy to write a few lines of code and run the program to make sure those lines are doing what is expected. 
But changing a few lines of code affect parts we have not realized yet. Also, as the program grows it is difficult to 
manually test all of them. To handle such issue we write automated tests. These programs that automatically run certain 
inputs through the other programs or parts of programs. 

Four main reasons to write test: 
* To ensure that code is working the way the developer thinks it should 
* To ensure that code continues working when we make changes 
* To ensure that the developer understodd the requirement 
* To ensure that the code we are writing has a maintainable interface 

In fact, it is often beneficial to write the tests before we write the code we are testing.

Test-driven development:
Write tests first is the mantra of test-driven development.Test-driven development takes the untested code is broken code 
concept one step further and suggests that only unwritten code should be untested.  We don't write any code until we have 
written the tests that will prove it works. The first time we run a test it should fail, since the code hasn't been
written. The we write the code that ensures the test passes, then write antoher test for the next segment of code. 

Goals of test-driven development:
* Ensure that tests really get written. 
* Writing tests first forces us to consider exactly how the code will be used. It tells us what methods object need to have 
and how attributes will be accessed. It helps us break up the initial problem into smaller, testable problems and then to 
recombine the tested solution into larger and also test solutions. Often, when we're writing a test for a new object, we 
discover anomalies in the design that force us to consider new aspects of the software.

Unit testing:
Python's built-in test library is unittest. It provides serveral tools for creating and running unit tests, the most
important being the TestCase class. This class provides a set of methods that allow us to compare values, set up tests, 
and clean up when have finished. 
When we want to write a set of unit tests for a specific task, we create a subclasss of TestCase and write individual
methods to do the actual testing. These methods must all start with the name test. When the convention is followed, the 
tests automatically run as part of the test process. Normally, the tests set some values on an object and then run a
method and use the built-in comparison methods to ensure that the right results were calculated. 

Eg below
"""
import unittest 

class CheckNumbers(unittest.TestCase):
    def test_int_float(self):
        self.assertEqual(1, 1.0) 
    
    def test_str_float(self):
        self.assertEqual(1,"1")
    
if __name__ == "__main__":
    unittest.main()

"""
We can have many test methods on one TestCase class as we like. As long as the method name begins with test, the test runner 
will execute each one as a seperate, isolated test. Each test should be completelu independent of other tests. Results or 
calculations from previous test should have no impact on the current test. The key to writing good unit tests is keeping 
each test method as short as possible, testing a small unit of ode with each tes case. 
If our code does not seem to naturally break up into such testable units, it's probably a sign that the code needs to be 
redesigned.

"""