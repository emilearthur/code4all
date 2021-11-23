"""
Set and dictionary comprehensions:
Comprehensions aren't only restricted to lists. We can use similar syntax braces to create a dictionaries as well. 

One way to create a set comprehension is wrap a list comprehension in the set() constructor, which converts it to 
sets.  
Eg below  we use a named tuple to model author/title/genre traid and then retrieves a set of all the authors 
that wirte a specifi genre. 
"""
from collections import namedtuple
from sys import warnoptions 

Book = namedtuple("Book","author title genre")

books = [Book("Pratchett", "Nightwatch", "fantasy"),
        Book("Pratchett","Thief of Time","fantasy"),
        Book("Le Guin","The Dispossessed","scifi"),
        Book("Le Guin","A Wizard of Earthsea","fantasy"),
        Book("Turner","The Thief","fantasy"),
        Book("Phillips","Preston Diamond","western"),
        Book("Phillips","Twice Upon A Time","scifi"),]

fantasy_authors = {b.author for b in books if b.genre == "fantasy"}
fantasy_titles = {b.title for b in books if b.genre == "fantasy"}


"""
Generator expressions : 

To avoid use of misuse of memory on large files which might be as a results of list comprehension or foor loops
generator expressions are best touse. 
They use the same syntax as comprehensions, but they don't create a final container object. 
To create a generator expression, wrap the comprehension in () instead of [] or {}.

Eg below

This program takes the two filenames on the command line, uses a generator expression to
filter out the warnings (in this case, it uses the if syntax and leaves the line unmodified),
and then outputs the warnings to another file. If we run it on our sample file, the output
"""
import sys 

inname = sys.argv[1] 
outname = sys.argv[2] 

with open(inname) as infile:
    with open(outname, "w") as outfile:
        warnings = (l for l in infile if "WARNING" in l )
        for l in warnings:
            outfile.write(l)




class WarningFilter:
    def __init__(self, insequence):
        self.insequence = insequence 

    def __iter__(self):
        return self 
    
    def __next__(self):
        l = self.insequence.readline() 
        while l and "WARNING" not in l:
            l = self.insequence.readline() 
        if not l:
            raise StopIteration
        return l.replace("\tWARNING", "") 
        
#with open(inname) as infile:
#    with open(outname, "w") as outfile:
#        filter = WarningFilter(infile) 
#        for l in filter:
#            outfile.write(l) 

"""
When python sees yield i a function, it takes that function and wraps it up in an object. 
yeild is like a return function however when the function is called again via next, it will start from 
where it left off. 
"""
def warnings_filter(insequence):
    for l in insequence:
        if "WARNING" in l:
            yield l.replace("\tWARNING", "")  # yield is a key to generators.

with open(inname) as infile:
    with open(outname,"w") as outfile:
        filter = warnings_filter(infile) 
        for l in filter:
            outfile.write(l) 