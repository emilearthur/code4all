"""
Yield items from another iterable 

Often, when we build a generator function, we end up in a situation where we want to
yield data from another iterable object, possibly a list comprehension or generator
expression we constructed inside the generator, or perhaps some external items that were
passed into the function. This has always been possible by looping over the iterable and
individually yielding each item.

Eg. below; 
"""

import sys
from test_9_2 import infile 

inname = sys.argv[1] 
outname = sys.argv[2] 

# the generator can do some basic setup before yielding information from another iterable (as a generator expression) 
def warnings_filter(infilename):
    with open(infilename) as infile:
        yield from (l.replace("\tWARNING", "") for l in infile if "WARNING" in l)

filter = warnings_filter(inname)
with open(outname,"w") as outfile:
    for l in filter:
        outfile.write(l) 


def warnings_filter_(infilename):
    with open(infilename) as infile:
        warning  = (l for l in infile if "WARNING" in l)
