"""

*variable_name = list 
**variable_name = dict 

Default values alone do not allow us all the flexible benefits of method overloading. One
thing that makes Python really slick is the ability to write methods that accept an arbitrary
number of positional or keyword arguments without explicitly naming them. We can also
pass arbitrary lists and dictionaries into such functions.

For example, a function to accept a link or list of links and download the web pages could
use such variadic arguments, or varargs. Instead of accepting a single value that is expected
to be a list of links, we can accept an arbitrary number of arguments, where each argument
is a different link. We do this by specifying the * operator in the function definition, as
follows
"""
def get_pages(*links):
    for link in links:
        print(link)

# *links parameter accepts a number of arguments and put them all in a list named links. 


"""
We can also accept arbitrary keyword arguments. These arrive in the function as a
dictionary. They are specified with two asterisks (as in **kwargs) in the function
declaration. This tool is commonly used in configuration setups. The following class allows
us to specify a set of options with default values:
"""
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


#running the function above 
options = Options(username="dusty", password="mainpwd", debug=True)

print(options['debug'], options['port'])



"""
This example processes an arbitrary list of files. The first argument is a target folder, and
the default behavior is to move all remaining non-keyword argument files into that folder.
Then there is a keyword-only argument, verbose, which tells us whether to print
information on each file processed. Finally, we can supply a dictionary containing actions
to perform on specific filenames; the default behavior is to move the file, but if a valid
string action has been specified in the keyword arguments, it can be ignored or copied
instead. Notice the ordering of the parameters in the function; first, the positional argument
is specified, then the *filenames list, then any specific keyword-only arguments, and
finally, a **specific dictionary to hold remaining keyword arguments.

"""

import shutil 
import os.path

def augmented_move(target_folder, *filenames, verbose=False, **specific):
    """
    Move all filenames into the target_folder, allowing specific treatment of certain files.
    """
    def print_verbose(message, filename):
        """print the message only if verbose is enabled"""
        if verbose:
            print(message.format(filename))

    for filename in filenames:
        target_path = os.path.join(target_folder, filename)
        if filename in specific:
            if specific[filename] == "ignore":
                print_verbose("Ignoring {0}", filename)
            elif specific[filename] == "copy":
                print_verbose("Copying {0}", filename)
                shutil.copyfile(filename, target_path)
        else:
            print_verbose("Moving {0}", filename)
            shutil.move(filename, target_path)


