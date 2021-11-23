"""
Coroutines:

They are extemely powerful contructs that are confused with generators. 

"""

# a programe that allow one to keep running tally that can be increased by arbitrary values. 
def tally():
    score = 0 
    while True:
        increment = yield score 
        score += increment  

"""
The thing that is really confusing for many people is the order in which this happens:
1. yield occurs and the generator pauses
2. send() occurs from outside the function and the generator wakes up
3. The value sent in is assigned to the left side of the yield statement
4. The generator continues processing until it encounters another yield statement

This is how we define the difference
between a generator and a coroutine: a generator only produces values, while a coroutine
can also consume them.
+


"""

"""
Problem: Now, given the preceding log file, the problem we need to solve is how to obtain the serial
number of any drives that have XFS errors on them. This serial number might later be used by a data center 
technician to identify and replace the drive.

using regular expression to identify individual lines. 


"""
import re

def match_regex(filename, regex):
    "loops over all the lines and spit out any line that matches a given regular expression"
    with open(filename) as file:
        lines = file.readlines() 
    for line in reversed(lines):
        match = re.match(regex, line) 
        if match:
            regex = yield match.groups()[0]



def get_serials(filename): 
    "interact with match_regex on what regular expression to be searched for at a given time."
    ERROR_RE = "XFS ERROR (\[sd[a-z]\])"
    matcher = match_regex(filename, ERROR_RE) 
    device = next(matcher) 
    while True:
        try:
            bus = matcher.send("(sd \S+) {}.*".format(re.escape(device)))
            serial = matcher.send("{} \(SERIAL=([^)]*)\)".format(bus))
            yield serial 
            device = matcher.send(ERROR_RE) 
        except StopIteration:
            matcher.close() 
            return 


for serial_number in get_serials("system_log.log"):
    print(serial_number)

"""
Notes:
Look at the match_regex coroutine first. Remember, it doesn't execute any code when it is
constructed; rather, it just creates a coroutine object. Once constructed, someone outside the
coroutine will eventually call next() to start the code running. Then it stores the state of
two variables filename and regex. It then reads all the lines in the file and iterates over
them in reverse. Each line is compared to the regular expression that was passed in until it
finds a match. When the match is found, the coroutine yields the first group from the
regular expression and waits.

At some point in the future, other code will send in a new regular expression to search for.
Note that the coroutine never cares what regular expression it is trying to match; it's just
looping over lines and comparing them to a regular expression. It's somebody else's
responsibility to decide what regular expression to supply.

"""


"""
Closing coroutines and throwing exceptions:
Normal generators signal their exit from inside by raising StopIteration. If we chain multiple genereators 
together (eg. by iterating over one generator from inside another), the StopIteration exception will be 
propagated outward. Eventually, it will hit a for loop that will see the exception and nkow that its time 
to exit the loop. 

Even though they use a similar syntax, coroutines don't normally follow the iteration
mechanism. Instead of pulling data through one until an exception is encountered, data is
usually pushed into it (using send). The entity doing the pushing is normally the one in
charge of telling the coroutine when it's finished. It does this by calling the close()
method on the coroutine in question.

When called, the close() method will raise a GeneratorExit exception at the point the
coroutine was waiting for a value to be sent in. It is normally good policy for coroutines to
wrap their yield statements in a try...finally block so that any cleanup tasks (such as
closing associated files or sockets) can be performed.

If we need to raise an exception iside a coroutine, we can use the throw() method in a similar way. 
It accepts an exception type with optional value and traceback args. 

"""

"""
Relationship between coroutines, generators and functions:

A coroutine is a routine that can have data passed in at one or more points and get it out at
one or more points. In Python, the point where data is passed in and out is the yield
statement.
A function, or subroutine, is the simplest type of coroutine. You can pass data in at one
point, and get data out at one other point when the function returns. While a function can
have multiple return statements, only one of them can be called for any given invocation
of the function.
A generator is a type of coroutine that can have data passed in at one point, but can
pass data out at multiple points. In Python, the data would be passed out at a yield
statement, but you can't pass data back in. If you called send, the data would be silently
discarded.

So, in theory, generators are types of coroutines, functions are types of coroutines, and
there are coroutines that are neither functions nor generators. That's simple enough, eh? So,
why does it feel more complicated in Python?

Functions are callable and return values, generators have data pulled out using
next(), and coroutines have data pushed in using send.



"""
