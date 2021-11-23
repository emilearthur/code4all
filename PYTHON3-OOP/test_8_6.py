"""
Serializing web objects:

It is not a good idea to load a pickled object from an unknown or untrusted source. It is
possible to inject arbitrary code into a pickled file to maliciously attack a computer via the
pickle. Another disadvantage of pickles is that they can only be loaded by other Python
programs, and cannot be easily shared with services written in other languages.

Format that can be used in clude XML, YAML and CSV for tablular data. 
Python has solid standard or third-party libraries for all of them.

XML and YAML, for example, both have obscure features that, used maliciously, can allow arbitrary commands
to be executed on the host machine. These features may not be turned off by default. Do your research.

JSON (javascript object notation) is a human-readable format for exchanging primitive data. 
JSON is a standard format that can be interpreted by a wide array of heterogeneous client systems. 
Hence, JSON is extremely useful for transmitting data between completely decoupled systems.
Further, JSON does not have any support for executable code, only data can be serialized; thus, it is 
more difficult to inject malicious statements into it.

Because JSON can be easily interpreted by JavaScript engines, it is often used for transmitting data from 
a web server to a JavaScript-capable web browser. 
If the web application serving the data is written in Python, it needs a way to convert internal data
into the JSON format.

The module to work with on json file is called json. 
This module provides a similar interface to the pickle module, with dump, load, dumps, and loads functions. 
The default calls to these functions are nearly identical to those in pickle, so let's not repeat the details.
There are a couple of differences; obviously, the output of these calls is valid JSON notation, rather than 
a pickled object. In addition, the json functions operate on str objects, rather than bytes. 
Therefore, when dumping to or loading from a file, we need to create text files rather than binary ones.

The JSON serializer is not as robust as the pickle module; it can only serialize basic types such as integers, 
floats, and strings, and simple containers such as dictionaries and lists. 

In the json module, both the object storing and loading functions accept optional
arguments to customize the behavior. The dump and dumps methods accept a poorly named
cls (short for class, which is a reserved keyword) keyword argument. If passed, this
should be a subclass of the JSONEncoder class, with the default method overridden. This
method accepts an arbitrary object and converts it to a dictionary that json can digest. If it
doesn't know how to process the object, we should call the super() method, so that it can
take care of serializing basic types in the normal way.
The load and loads methods also accept such a cls argument that can be a subclass of the
inverse class, JSONDecoder. However, it is normally sufficient to pass a function into these
methods using the object_hook keyword argument. This function accepts a dictionary
and returns an object; if it doesn't know what to do with the input dictionary, it can return
it unmodified.

"""

"""
A simple contact class that we want to serialize

run:
c = Contact("John", "Smith")
json.dumps(c.__dict__)

"""

class Contact:
    def __init__(self, first, last):
        self.first = first 
        self.last = last
        self.__full_namex = str(self.first) + " " + str(self.last)

    def full_namex(self):
        return(self.__full_namex)

    @property 
    def full_name(self):
        return("{} {}".format(self.first, self.last)) 
    
    @full_name.setter
    def full_name(self, value):
        value = value.split()
        self.first = value[0] 
        self.last = value[-1] 
        self.__full_namex = str(self.first) + " " + str(self.last)


"""
But accessing special (double-underscore) attributes in this fashion is kind of crude. Also,
what if the receiving code (perhaps some JavaScript on a web page) wanted that
full_name property to be supplied? Of course, we could construct the dictionary by hand,
but let's create a custom encoder instead:

The default method basically checks to see what kind of object we trying to serialize. 
If it's a contact, we convert it to a dictionary manually, else we let the parent class 
hadnle serialization(by assuming that it is a basic type, which json knows how to handle) 

Notice that we pass an extra attribute to identify this object as a contact, since there would
be no way to tell upon loading it. This is just a convention; for a more generic serialization
mechanism, it might make more sense to store a string type in the dictionary, or possibly
even the full class name, including package and module. Remember that the format of the
dictionary depends on the code at the receiving end; there has to be an agreement as to how
the data is going to be specified


run:
c = Contact("John","May")
json.dumps(c, cls=ContactEncoder)
"""
import json

class ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Contact):
            return{
                "is_contact":True,
                "first":obj.first,
                "last":obj.last,
                "full":obj.full_name,
                "full_x": obj.full_namex(), # this is because its a method 
            }
        return super().default(obj)



"""
For decoding, we can write a function that accepts a dictionary checks the existance of 
the is_contact variable to decide whether to convert it to a contact. 

run:
c = Contact("James","Main")
data = json.dumps(c, cls=ContactEncoder)
c = json.loads(data, object_hook=decode_contact 

"""
def  decode_contact(dic):
    if dic.get("is_contact"):
        return Contact(dic["first"], dic["last"])
    else:
        return dic

