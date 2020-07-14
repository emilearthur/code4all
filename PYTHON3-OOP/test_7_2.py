"""
Sometime when looping over a for loop, we want to access the index(current position in the list)
of the current item being processed. for loop doesn't provide us with the indexes but 
enumerate function does. It creates a sequence of tuples, where the first object in each 
tuple is the index and second is the orginal item. 

The enumerate function returns a sequence of tuples, our for loop splits each tuple into
two values, and the print statement formats them together. It adds one to the index for
each line number, since enumerate, like all sequences, is zero-based
"""

import sys 

filename = sys.argv[1]  

with open(filename) as file:
    for index, line in enumerate(file):
        print(f"{index+1}: {line}", end="") 
