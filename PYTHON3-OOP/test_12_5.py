"""
Skipping test with pytest:zne

As with the unittest module, it is frequently neccessary to skip test in pytest, for some reasons: the code being tested 
hasn't be implemented yet, the test only runs on certain interpreters or os or the test is time-consuming and should only 
be run under certain circumstances. 

We skip tests at any point in our code using pytest.skip func. It accepts a single arg: a sting describing why it has 
been skipped. This function can be called anywhere.  If we call it inside a test function, the test will be skipped. 
if we call it at the module level, all the test in that module will be skipped. If we call it inside a fixture, all
test that call the funcarg will be skipped. 

We can also execute the skip function in an if statement.  

Eg. below 

import sys 
import pytest 

def test_simple_skip():
    if sys.platform != "fakeos":
        pytest.skip("Test works only on fakeos") 
    fakeos.do_something_fakes() 
    assert fackeos.did_not_happen
    

pytest provides a convenience decorator that allow us to do skippping of individual test method or function based on
certain conditions. 
The decorator accepts a single string, which can contain any executable python code that evalutes to a Boolean value. 
Eg. below 
"""
import sys 
import pytest 

@pytest.mark.skipif("sys.version_info <= (3,0)")
def test_python3():
    assert b"hello".decode() == "hello" 

"""
THe pytest.mark.xfail decorator behaves similarly, except that it marks a test as expected to fail, similar to 
unittest.expectFailure(). If the test is successful, it will be recorded as a failure. If it fails, it will be reported 
as expected behavior. In the case of xfail, the conditional arg is optional. If its not supplied, the test will be marked 
as expected to fail under all conditions. 
"""

"""
Imitating expensive objects:
Sometimes, we want to test code that requires an object be supplied that is either expensive or difficult to construct. 
Sometimes we find ourselves writing test code that has a ton of boilerplate to setup objects that are only incidentally 
related to the code under test. 

For eg, imagine we have some code that keeps track of flight status in an external key-value store(eg. redis or memcache)
such that we can store the timestamp and the most recent status. 
A basic version of the code below. 
"""
import datetime 
import redis 

class FlightStatusTracker:
    ALLOWED_STATUSES = {"CANCELLED","DELAYED","ON TIME"} 

    def __init__(self): 
        self.redis =  redis.StrictRedis() 

    def change_status(self, flight, status):
        status = status.upper() 
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"{status} is not a valid status") 

        key = f"flightno:{flight}"
        value = f"{datetime.datetime.now().isoformat()}|{status}"
        self.redis.set(key, value) # set method called on the redis object

"""
Here we don't have to check in our unit tests if the redis data is properly storing the data as it is done in integration 
or application testing. Here we assume that py-redis devs have tested their codes and that this method does what we want 
it to do. As the a rule, unit test should be self-contained and shouldn't rely on the existance of outside resources, such 
as a running Redis instance. 
Instead, we only need to test that the set() method was called the appropraite number of times and with the appropriate 
args. We can use Mock() obkect in our test to replace the troublesome method with an object we can introspect. 
Eg of Mock() below.
"""

# move the code above to code_sample.py . Thus will be import code from there 
from code_sample import FlightStatusTracker
from unittest.mock import Mock 
import pytest 
from unittest.mock import patch

@pytest.fixture
def tracker():
    return FlightStatusTracker() 

def test_mock_method(tracker):
    """
    Written using pytest syntax, asserts that the correct exception is raised when an inappropriate arg is passed in. 
    Additionally it creates a Mock object for the set method and makes sure that its never called. It i was, it means 
    there is a bug in our exception handling code. 
    """
    tracker.redis.set = Mock()
    fake_now = datetime.datetime(2015, 4 , 1) 
    with pytest.raises(ValueError) as ex:
        tracker.change_status("AC101", "lost")
    assert ex.value.args[0] == "LOST is not a valid status"
    assert tracker.redis.set.call_count == 0

"""
Temporarily setting a library func. to a specific value is one of the few valid use cases for monkey-patching. The mock 
library provides a patch context managerr that allows us to replace attributes on existing libraries with mock objects. 
When the context manager exits, the original attributes is automatically restored so as not to impact other test cases. 
eg below. 
"""
def test_patch_1(tracker):
    tracker.redis.set = Mock() 
    fake_now = datetime.datetime(2015, 4, 1) 
    with patch("datetime.datetime") as dt:
        dt.now.return_value = fake_now
        tracker.change_status("AC102", "on time") 
    dt.now.assert_called_once_with()
    tracker.redis.set.assert_called_once_with("flightno:AC102", "2015-04-01T00:00:00|ON TIME")

"""
In the code above, we first construct a value fake_now which set as the return value of the datetime.datetime.now func. 
We have to constuct this object before patch datetime.datetime, because otherwise we'd be calling the patched now 
func. before we constructed. 
The with statement invites the patch to replace the datetime.datetime module with a mock object, which is returned as the 
dt value. The neat thing about mock object is that any time you access an attribute or mtehod on that object, it returns 
another mock object.
Thus, when access dt.now, it gives us a new mock object. We set the return_value of that object to our fake_now object. 
Now, whenever the datetime.datetime.now function is called, it will retrun our object instead of a new mock object. But 
when the interpreter exists the context manager, the orginal datetime.datetime.now() functionality is restored.

After calling our change_status method with know values, we use the assert_called_once_with function of the Mock class to 
ensure that the now function was indeed called exactly once with no args.  We the call it a second time to prove that the 
redis.set method was called with args that were formatted as we expected them to be.

We also mock out the redis.StrictRedis class to return a mock in a setUp method. Also, an alternative implementation, 
is to construct the redis instance inside __init__ as below. 
def __init__(self, redis_instance=None):
    self.redis = redis_instance if redis_instance else redis.StrictRedis()

This implemtation above, allows us to pass a mocj in when testing so the StrictRedis method never gets constructed. 
Additionally, it allows any client code that talks to FlightStatusTracker to pass in their own redis instance. 

In general, we should be quite stingy with mocks. If we find ourselves mocking out
multiple elements in a given unit test, we may end up testing the mock framework rather
than our real code. This serves no useful purpose whatsoever; after all, mocks are well-
tested already! If our code is doing a lot of this, it's probably another sign that the API we
are testing is poorly designed. Mocks should exist at the boundaries between the code
under test and the libraries they interface with. If this isn't happening, we may need to
change the API so that the boundaries are redrawn in a different place.


How  much testing is enough?
Code coverage is an estimate of the number of lines of code that are executed by a program. If we know that number and the
number of lines of code that are executed by a program, we can get an estimate of what percentage of the code was really 
tested or covered. If we adittionally have an indicator as to which  line was not tested, we can more easily write new 
testes to ensure thos lines are less broken. 

We use coverage for the task stated above. 

We don't have space to cover all the details of the coverage API, so we'll just look at a few typical examples.
If we have a Python script that runs all our unit tests for us (for example, using unittest.main, discover, pytest, or a
custom test runner), we can use the following command to perform a coverage analysis:

$coverage run test_code_sample.py # performing coverage analysis
$coverage report # get analysis of the code coverage. 
$coverage report -m # add a column that includes stats module that were not executed during the test run.4

Also we can install pytest-coverage, a plugin which adds cmd options to pytest  eg pytest test_test.py --cover-report 
which can be set to html, report or annotate 
"""

