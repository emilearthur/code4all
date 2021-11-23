"""
Serializing objects:

The Python pickle module is an object-oriented way to store objects directly in a special
storage format. It essentially converts an object (and all the objects it holds as attributes)
into a sequence of bytes that can be stored or transported however we see fit.

For basic tasks, the pickle module has an extremely simple interface. It comprises four
basic functions for storing and loading data: two for manipulating file-like objects, and two
for manipulating bytes objects (the latter are just shortcuts to the file-like interface, so we
don't have to create a BytesIO file-like object ourselves).

The dump method accepts an object to be written and a file-like object to write the serialized
bytes to. This object must have a write method (or it wouldn't be file-like), and that
method must know how to handle a bytes argument (so, a file opened for text output
wouldn't work).


The load method does exactly the opposite; it reads a serialized object from a file-like
object. This object must have the proper file-like read and readline arguments, each of
which must, of course, return bytes. The pickle module will load the object from these
bytes and the load method will return the fully reconstructed object. 

"""
from datetime import time
import pickle 

some_data = ["a list","containing",5,"values including another list",["inner","list"]] 

with open("pickled_list","wb") as file:
    pickle.dump(some_data, file)

with open("pickled_list", "rb") as file:
    loaded_data = pickle.load(file) 

print(loaded_data)
assert loaded_data == some_data

"""
It is possible to call dump or load on a single open file more than once. Each call to dump
will store a single object (plus any objects it is composed of or contains), while a call to load
will load and return just one object. So, for a single file, each separate call to dump when
storing the object should have an associated call to load when restoring at a later date.

"""

"""
Customizing pickles:
Basic primitives such as integers,
floats, and strings can be pickled, as can any container objects, such as lists or dictionaries,
provided the contents of those containers are also picklable. Further, and importantly, any
object can be pickled, so long as all of its attributes are also picklable.

"""

"""
Eg: Here's a class that loads the contents of a web page every hour to ensure that they stay up
to date. It uses the threading.Timer class to schedule the next update:

"""
from threading import Timer 
import datetime 
from urllib.request import urlopen 

class UpdatedURL:
    def __init__(self, url):
        self.url = url 
        self.contents = ""
        self.last_updated = None 
        self.update() 
    

    def update(self):
        self.contents = urlopen(self.url).read() 
        self.last_updated = datetime.datetime.now() 
        self.schedule() 
    
    def schedule(self):
        self.timer = Timer(3600, self.update) 
        self.timer.setDaemon(True)
        self.timer.start()

    def __getstate__(self):
        new_state = self.__dict__.copy() 
        if 'timer' in new_state:
            del new_state['timer']
        return new_state

    
    def __setstate__(self, data):
        self.__dict__ = data
        self.schedule()

"""
The code above is not pickleable because self.timer instance. 

That's not a very useful error, but it looks like we're trying to pickle something we
shouldn't be. That would be the Timer instance; we're storing a reference to self.timer in
the schedule method, and that attribute cannot be serialized.

When pickle tries to serialize an object, it simply tries to store the object's __dict__
attribute; __dict__ is a dictionary mapping all the attribute names on the object to their values. 

Luckily, before checking __dict__, pickle checks to see whether a __getstate__ method exists. If it does, 
it will store the return value of that method instead of the __dict__.

Adding a __getstate__ method to our UpdatedURL class that simply returns a copy of
the __dict__ without a timer. 

As we might expect, there is a complementary __setstate__ method that can be implemented to customize unpickling. 
This method accepts a single argument, which is the object returned by __getstate__. 
If we implement both methods, __getstate__ is not required to return a dictionary, since __setstate__ will 
know what to do with whatever object __getstate__ chooses to return. In our case, we simply want to restore the
__dict__, and then create a new timer:

"""