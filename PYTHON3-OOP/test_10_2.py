"""
Decorators in Python 

Notes code below:
A function, log_calls, that accepts another function
This function defines (internally) a new function, named wrapper, that does
some extra work before calling the original function
The inner function is returned from the outer function

"""
import time 

def log_calls(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        print("Calling {0} with {1} and {2}".format(func.__name__, args, kwargs))

        return_value = func(*args, **kwargs) 
        print("Executed {0} in {1}ms".format(func.__name__, time.time()- now))
        
        return return_value

    return wrapper 

def test1(a, b, c):
    print("\ttest1 called") 

def test2(a, b):
    print("\ttest2 called") 

def test3(a, b):
    print("\ttest3 called")
    time.sleep(1) 

test1 = log_calls(test1) 
test2 = log_calls(test2) 
test3 = log_calls(test3) 

test1(1,2,3)
test2(4, b=5) 
test3(6,7)


"""
Instead of applying the decorator functoin after method definintion we can use th @decorator syntax to do all at one. 
Eg. below 
"""
@log_calls
def test4(a, b, c):
    print("\ttest4 called")

test4(5,6,7)