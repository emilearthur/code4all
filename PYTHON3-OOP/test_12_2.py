"""
Assertion methods:
The general layout of a test case is to set certain variables to know values, run one or more funcs, methods or processes,
and then prove that correct expected results were return or calculate by using TestCase assertion methods 

We use assertEqual test failure if the two parameters do not pass an equality check. The inverse assertNotEqual fails if 
the two parameters compared as equal. The assertTrue and assertFalse methods each accept a single expression and fails if 
the expression does not pass an if test. These tests do not check for the Boolean values True or False, rather they test
the same condition as though an if statement were used: False, None, 0  or an empty list, dict, str, set or tuple would 
pass a call to the assertFalse method. Nonzero numbers, containers with values in them, or the value True would succeed 
when calling the assertTrue method. 
There is an assertRaises method that can be used to ensure that a specific function call raises a specific exception or 
optionally, it can used as a context manager to wrap inline code. The test passes if the code inside the with statement 
raises the proper exception; otherwise it fails. 

Eg. below 
"""
from typing import List
import unittest 

def average(seq):
    return sum(seq) / len(seq) 

class TestAverage(unittest.TestCase):
    def test_zero(self):
        self.assertRaises(ZeroDivisionError, average, [])
    
    def testwith_zeros(self):
        with self.assertRaises(ZeroDivisionError):
            average([]) 

if __name__ == "__main__":
    unittest.main()

"""
The context manager allows us to wirte the code the way we would normally write it(by calling functions or excuting code
directly), rather than having to wrap the function call in another function call. 

Other assertion methods below. 

methods: 
* assertGreater, assertGreaterEqual, assertLess, assertLessEqual => Accept two comparable objects and ensure the 
named inequality holds. 
* assertIn, assertNotIn => Ensure an element is (or is not) an elemetn in a container object. 
* assertIsNone, assertIsNotNone => Ensure an element is (or is not) the exact None value (but not another falsey value) 
* assertSameElements => Ensure tow container objects have the same elements, ignoring the order. 
* assertSequnceEqualassertDictEqual, assertSetEqual, assertListEqual, assertTupleEqual => Ensure two containers have the
same order. If there's a failure, show a code difference comparing the two lists to see where they differ. The last four 
methods also test the type of the list. 

Each of the assertion methods accepts an optional arg named msg. If supplied, it is included in the error message if the 
assertion fails. This can be useful for clarifying what was expected or explaining where a bug may have occured to cause
the assertion to fail. 

"""

"""
Reducing boilerplate and cleaning up:
After writing a few small tests, we often find that we have to write the same setup code for several related tests.  

Eg below: the list subclass has three methods for statistical cal. 
"""

from collections import defaultdict 

class StatsList(list):
    def mean(self:List) -> float:
        return sum(self) / len(self) 
    
    def median(self:List) -> float:
        if len(self) % 2:
            return float(self[int(len(self) / 2)])
        else:
            idx = int(len(self) / 2) 
            return float((self[idx] + self[idx-1]) / 2)

    def mode(self:List) -> List:
        freqs = defaultdict(int) 
        for item in self:
            freqs[item] += 1 
        mode_freq = max(freqs.values())
        modes = [] 
        for item, value in freqs.items():
            if value == mode_freq:
                modes.append(item) 
        return modes



import unittest 
class TestValidInputs(unittest):
    def setUp(self):
        self.stats = StatsList([1,2,2,3,3,4])

    def test_mean(self):
        self.assertEqual(self.stats.mean(), 2.5) 
    
    def test_median(self):
        self.assertEqual(self.stats.median(), 2.5) 
        self.stats.append(4) 
        self.assertEqual(self.stats.median(), 3.0)
    
    def test_mode(self):
        self.assertEqual(self.stats.mode(), [2,3])
        self.stats.remove(2)
        self.assertEqual(self.stats.mode(), [3]) 



""""
Organizing and running tests:
Most Python programmers choose to put their tests in a separate package (usually named tests/ alongside their source 
directory). This is not required, however. Sometimes it makes sense to put the test modules for different packages in a 
subpackage next to that package, for example.

Ignoring broken tests:
Sometimes test is knonwn to fail, but we don't want the test suite to report the failure. This may be because a broken or 
unfinished feature has tests written, but we aren't currently focusing on improving it. More often, it happens because a 
feature is only available on certain platforms, python version, of for advanced versions of a specific library. 
Python provides a few decorators to mark tests as expected to fail or to be skipped under know conditions. 
These decorators are as follows:
* expectedFailure()   => Accepts no args. and tells the test runner not to record the test as failure when it fails. 
* skip (reason)  => It expects a single string arg describing why the test was skipped. 
* skipIf(condition, reason) => this accepts one Boolean expression that indicating whether or not the test should be run
  and a similar description. 
* skipUnless(condition, reason) => same as explained above. 

These are applied using the python decorator syntax. 

its used as below
"""

import unittest 
import sys 

class SkipTests(unittest.TestCase):
    @unittest.expectedFailure
    def test_fails(self):
        self.assertEqual(False, True) 
    
    @unittest.skip("Test is useless")
    def test_skip(self):
        self.assertEqual(False, True)
    
    @unittest.skipIf(sys.version_info.minor == 7, "broken on 3.4")
    def test_skipif(self):
        self.assertEqual(False, True) 
    
    @unittest.skipUnless(sys.platform.startswith("linux"), "broken on linux") 
    def test_skipunless(self):
        self.assertEqual(False, True) 
    


if __name__ == "__main__":
    unittest.main()