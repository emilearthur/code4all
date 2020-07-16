"""
Unpacking arguments 

The function below takes three args.,  we used the *operator inside a function call to unpack it into the three args. 
If we have a dictionary, we use ** operator to unpack it as a collection of key arguments. 

"""

def show_args(arg1, arg2, arg3="THREE"):
    print(arg1, arg2, arg3)

some_args = range(3) 
more_args = {"arg1":"ONE",
            "arg2":"TWO"}

print("Unpacking a sequence:", end=" ")
show_args(*some_args) 

print("Unpacking a dict:", end= " ")
show_args(**more_args)


# the function below 
class Options:
    default_options = {
        'port':21,
        'host':'localhost',
        'username':None, 
        'password':None, 
        'debug': False,
    }
    
    def __init__(self, **kwargs):
        self.options = dict(Options.default_options) # copies the default value from the class, turns to a dictionary 
        self.options.update(kwargs) # updates the with keyword args when called upon

    def __getitem__(self,key):
        return self.options[key]



"""
The function above can be rewritten (unpacking two dictionaires) as:
Because the dictionaries are unpacked in order from left to right, the resulting dictionary
will contain all the default options, with any of the kwarg options replacing some of the
keys
"""
class Options:
    default_options = {
        'port': 21,
        'host': 'localhost',
        'username': None, 
        'password': None, 
        'debug': False,
    }

    def __init__(self, **kwargs):
        self.options = {**Options.default_options, **kwargs}
    
    def __getitem__(self, key):
        return self.options[key]