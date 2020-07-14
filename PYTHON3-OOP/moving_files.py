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


