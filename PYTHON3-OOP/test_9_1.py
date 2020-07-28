"""
Iterators:

An iterator is a object with a next() method and a done() methond; the latter returns True if there are no items 
left in the sequence.  

In a programming langauage without built-in suppport for iterators, the iterator would be looped over as below 

while not iterator.done():
    item = iterator.next()
    # do something with the item. 

In python iteration is a special feature, so the method gets a special name, __next__. This method can be accessed 
using the next(interator) built-in.  Rather than done method, python iterator protocol raises StopIteration to 
notify the loop that it has completed. 

"""

"""
The iterator protocol:
The Iterator abstract base class, in the collection.abc module, defines the iterator protocl in Python. As mentioned
it must have a __next__ method that the foor loop( and other features that support iteration) can call to get a new 
element from the sequence. In addition, every iterator must also fulfill the Iterable interface. 
Any class that provides an __iter__ method is iterable. 
This method must return an Iterator instance that will cover all the elements in that class. 

Eg. below
"""

class CapitalIterable:
    """
    This is class which loops over each of the words i a string and output them with the first letter 
    capitalized. 

    """
    def __init__(self, string):
        self.string = string 
    

    def __iter__(self): 
        return CapitalIterator(self.string) 

class CapitalIterator:
    def __init__(self, string):
        self.words = [w.capitalize() for w in string.split()]
        self.index = 0 

    def __next__(self):
        if self.index == len(self.words):
            raise StopIteration
        
        word = self.words[self.index]
        self.index += 1 
        return word 

    def __iter__(self):
        return self

"""
run:
iterable = CapitalIterable('the quick brown fox jumps over the lazydog')
iterator = iter(iterable)

while True:
    try:
        print(next(iterator))
    except StopIteration:
        break

Explaination:
The iterable is an object with elements that can be looped over. 
By default these elements can be looped over multiple times, however the iterator, represents a specific location 
in that iterablel; some of the items have been consumed and some have not.   

Each time next() is called on the iterator, it returns another token from the iterable, in order. Eventually, the 
iterator will be exhausted  in which case StopIteration is raised and we break out of the loop. 
simple form is 
for i in iterable:
    print(i)
"""


"""
Comprehension:
Comprehensions are simple, but powerful, syntaxes that allow us to transform or filter an iterable object in as 
little as one line of code. The resultant object can be a perfectly normal list, set, or dictionary, or it can be 
a generator expression that can be efficiently consumed while keeping just one element in memory at a time.

"""

"""
List Comprehensions:
They are fast to run and clean code. 
List comprehensions are used to map input values to output values, applying a filter along the way to include or 
exclude any values that meet a specific condition.


Eg. below
"""

# converting list of string to list of intergers. NB: without list comprehsion 
input_string = ["1","5","28","131","3"]
output_integers = [] 
for num in input_string:
    output_integers.append(int(num))

# with list comprehsion 
input_string_ = ["1","5","28","131","3"]
output_integers_ = [int(num) for num in input_string_]

# using if statement in list comprehsion 
filtered_output_ingeters = [int(num) for num in input_string_ if len(num) < 3]

filtered_output_ingeters_ = [int(num) for num in input_string_ if int(num) <40]

"""
Any iterable can be the input to a list comprehsion. In other words, anything we can wrap in a for loop can also 
be place inside a comprehension. 

For eg, text files are iterable; each call to __next__ on the file's iterator will return one line of the file. 
We could load a tab-deliminted file where the first line is a header row into a dictionary using the zip func. 

"""
import sys
filename = sys.argv[1] 

with open(filename) as file:
    header = file.readline().strip().split("\t") 
    contacts = [dict(zip(header, line.strip().split("\t")) for line in file)]

    for contact in contacts:
        print("email : {email} -- {last}, {first}".format(**contact))