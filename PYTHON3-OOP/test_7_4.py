"""
 Let's create a simple context manager that allows us to construct a
sequence of characters and automatically convert it to a string upon exit

This code adds two special methods required of a context manager to the list class it 
inherits from. 
"""

class StringJoiner(list):
    def __enter__(self):
        return self 

    def __exit__(self, type, value, tb):
        self.result = "".join(self)
        


"""
Testing context manager if it does work with a with statement 
"""
import random, string 

with StringJoiner() as joiner:
    for i in range(15):
        joiner.append(random.choice(string.ascii_letters))
print(joiner.result)



"""
Method Overloading 
Method overloading refers to having multiple methods with the same name that accept
different sets of arguments. 
"""

def no_args():
    pass 

# to call the function above  
no_args()

def mandatory_args(x, y, z):
    pass

# to call the function above 
a_variable = set()
mandatory_args("a string", a_variable, 5)


"""
Default args:
If we want to make an argument optional, rather than creating a second method with a
different set of arguments, we can specify a default value in a single method, using an
equals sign.
"""
def default_args(x, y, z, a="Some string", b=False):
    pass 

# to call the function above 
default_args("a string", a_variable, 8, "", True)
default_args("a long string", a_variable, 14)

default_args("a string", a_variable, 14, b=True)

default_args(y=1,z=2,x=3,a="hi")


"""
Its sometimes useful to use keyword-only arg. It's an arg that must be supplied as a
keyword argument. You can do that by placing a * before the keyword-only args. 

This function below has one positional argument, x, and three keyword arguments, y, a, and b. 
x and y are both mandatory, but a can only be passed as a keyword argument. y and b are
both optional with default values, but if b is supplied, it can only be a keyword argument.

"""

def kw_only(x, y="defaultkw", *, a, b="only"):
    print(x,y,a,b)

#since its a keyword args the following code runs successful and the code: kw_only("x","y","a") fails
kw_only("x",a="a",b="b")

"""
One thing to take note of with keyword arguments is that anything we provide as a default
argument is evaluated when the function is first interpreted, not when it is called. 
This means we can't have dynamically generated default values. For example, the following
code won't behave quite as expected. 
Eg. Below
"""
number = 5 
def funky_function(number=number):
    print(number)

def hello(b=[]):
    b.append('a')
    print(b)

"""
The function above create multiple elements in the list container whenever its called. 
To fix the issue, we use the code below
"""

def hello(b=None):
	if b is None:
		b = [] 
	 	b.append("a")
 	print(b) 


