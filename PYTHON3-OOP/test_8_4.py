"""
Getting information from regular expressions:

So far, our regular expressions have answered questions such as, does this string match this
pattern? Matching patterns is useful, but in many cases, a more interesting question is, if this
string matches this pattern, what is the value of a relevant substring? If you use groups to
identify parts of the pattern that you want to reference later, you can get them out of the
match return value. 
"""
import re 


pattern = "^[a-zA-Z.]+@([a-z.]*\.[a-z]+)$"
search_string = "some.user@example.com"
match = re.match(pattern, search_string) 

if match:
    domain = match.groups()[0]
    print(domain)


"""
Code above, Explaination:
the point is that we want to access the domain name (after the @ sign) so we can connect to that
address. This is done easily by wrapping that part of the pattern in parentheses and calling
the groups() method on the object returned by match. 
The groups method returns a tuple of all the groups matched inside the pattern, which you
can index to access a specific value.

The groups are ordered from left to right. However,
bear in mind that groups can be nested, meaning you can have one or more groups inside
another group. In this case, the groups are returned in the order of their leftmost brackets,
so the outermost group will be returned before its inner matching groups.

If there are no groups in the pattern, re.findall will return a list of strings,
where each value is a complete substring from the source string that matches the
pattern
If there is exactly one group in the pattern, re.findall will return a list of
strings where each value is the contents of that group
If there are multiple groups in the pattern, re.findall will return a list of tuples
where each tuple contains a value from a matching group, in order


The type of the return value depends on the number of bracketed groups inside the regular
expression:
If there are no groups in the pattern, re.findall will return a list of strings,
where each value is a complete substring from the source string that matches the
pattern
If there is exactly one group in the pattern, re.findall will return a list of
strings where each value is the contents of that group
If there are multiple groups in the pattern, re.findall will return a list of tuples
where each tuple contains a value from a matching group, in order

run:
re.findall('a.', 'abacadefagah')
re.findall("a(.)","abacadefagah")
re.findall("(a)(.)","abacadefagah")
re.findall("((a)(.))","abacadefagah")
"""


"""
Making repeated regular expressions efficient:

Whenever you call one of the regular expression methods, the engine has to convert the
pattern string into an internal structure that makes searching strings fast. This conversion
takes a non-trivial amount of time. If a regular expression pattern is going to be reused
multiple times (for example, inside a for or while loop), it would be better if this
conversion step could be done only once.

This is possible with the re.compile method. It returns an object-oriented version of the
regular expression that has been compiled down and has the methods we've explored
(match, search, and findall) already, among others

"""

"""
Filesystems paths:
They have a clunky interface with integer file handles and buffered reads and
writes, and that interface is different depending on which operating system you are using.
Python provides an OS-independent abstraction over these system calls in the os.path
module. It's a little easier to work with than accessing the operating system directly, but it's
not very intuitive. It requires a lot of string concatenation and you have to be conscious of
whether to use a forward slash or a backslash between directories, depending on the
operating system. There is a os.sep file representing the path separator, but using it
requires code that looks like this:

run:
path = os.path.abspath(os.sep.join(['.','subdir','subsubdir','file.ext']))
print(path)

pathlib in the standard library. 
It's an object-oriented representation of paths and files that is much more pleasant
to work with. The preceding path, using pathlib, would look like this:

run:
path = (pathlib.Path(".")/"subdir"/"subsubdir"/"file.ext").absolute()
print(path)

"""

"""
Below is a real-world example. 
A code that counts the number of lines of code excluding whitespace and comment in all 
python files in current directory and subdirectors 
"""
print("\n")
import pathlib 

def count_sloc(dir_path):
    sloc = 0 
    for path in dir_path.iterdir():
        if path.name.startswith("."):
            continue 
        if path.is_dir():
            sloc += count_sloc(path) # if path is a directory run count_sloc .i.e. child package
            continue
        if path.suffix != ".py":
            continue 
        with path.open() as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    sloc += 1 
    return sloc

root_path = pathlib.Path(".") 
print(f"{count_sloc(root_path)} lines of python code")


"""
Most standard library modules that accept a string path can also accept a pathlib.Path
object. For example, you can open a ZIP file by passing a path into it:
run:
zipfile.ZipFile(Path('nothing.zip'), 'w').writestr('filename','contents')

This doesn't always work, especially if you are using a third-party library that is
implemented as a C extension. In those cases, you'll have to cast the path to a string using
str(pathname).



"""