"""
The problem with multiprocessing:
As Threads do, multiprocessing also has problems. There is no best way to do concurrency; this is especially true in Python. 
In multiprocessing, the primary drawback is that sharing data between processes is costly. As discussed, all communication 
between processes, whether queue, pipes or a more implicit mechanism requires pickling the objects. 
Excessive pickling quickly dominates processing time. Multiprocessing works best when relatively small objects are passed 
between processes and tremendous amount of work need to be done on each time. ON the other hand, if no communication 
between process is required, there may not be any point using the module at all; we can sip up four seperate Python 
process (by running each in a seperate terminal) and use them independently. 
The major problem with multiprocessing is that like threads, it can be hard to tell which process a variable or method 
is being accessed in. In multiprocessing, if you access a variable from another process it will usually overwrite the 
variable in the currently running process while the other process keeps the old value. This is really confusing to maintain 
thus don't do it. 


Features:
Futures wrap either multiprocessing or threading depending on what kind of concurrency we need. They don't completely solve 
of accidentally altering shared state but they allow us to structure our code such that it is easier to track down when 
we do so. Futures provider distinct boundaries between the different threads or processes. Similar to the multprocessing 
poll, they are useful for call and answer type interactions, in which processing can happen in another thread and then at 
some point in the future you can ask it for the result. NB: Its just a wrapper around the multiprocessing pools and thread 
pools and thread pools but it provides a cleaner APU and encourages nicer code. 

A future is an object that wraps a function call. That function call is run in the background, in a thread or process. 
The future object has methods the main thread can use to check whether the future has comlpleted and to get the results 
after it has completed. 
Below we are writing another file search example. Here we are creating a simple version of the find command. This code 
will search the entire filesystem for paths that contains a given a string of characters. 

"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path 
from os.path import sep as pathsep 
from collections import deque 

def find_files(path, query_string):
    subdirs = [] 
    for p in path.iterdir():
        full_path = str(p.absolute()) 
        if p.is_dir() and not p.is_symlink():
            subdirs.append(p)
        if query_string in full_path:
            print(full_path)

    return subdirs

query = '.py'
futures = deque() 
basedir = Path(pathsep).absolute() 

with ThreadPoolExecutor(max_workers=10) as executor:
    futures.append(executor.submit(find_files, basedir, query))
    while futures:
        future = futures.popleft() 
        if future.exception():
            continue
        elif future.done():
            subdirs = future.result() 
            for subdir in subdirs:
                futures.append(executor.submit(find_files, subdir, query)) 
        else:
            futures.append(future)

"""
Notes: The code above consists of a function named find_files, which runs on a seperate thread. All interaction with the
external environment is passed into the functin or returned from it. Note that it does not access any global variable. 

Accessing outside variable without proper synchronization results into race condition. 

We search for all files that constain the character '.py' for this eg.  WE have a queue of features. The basedir variable 
points to the root of the filesystem. 

Search theory: The algo implements breadth-first seach in parallel. Rather than recursively searching every directory 
using depth-first seach, it adds all the subdirectories in the current folder to the queue, then all the subdirectories 
in the current folder to the queue, then all the subdirectories of each of those folders, and so on. 

The meat of the program is known as an event loop. We can construct a ThreadPoolExecutor as a context manager so that it 
is automatically clearn up and closes it threads when it is done. It requires a max_workers arg to indicate the number of 
threads running at a time. If more than this many jobs is submitted, it queues up the rest until a worker thread becomes 
available. When using ProcessPoolExecutor, this is normally constrained to the number of CPUs on the machine, but with 
threads, it can be much higher, depending how many are waiting on I/O at a time. Each thread takes up a certain amount 
of memory, so it shouldn't be too high. It doesn't take all that many threads before the speed of the disk, rather than 
the number of parallel requests, is the bottleneck. 
Once the executor has been constructed, we submit a job to it using the root direcotry by the submit() method which 
immediately returns a Future object. The future is place in the queue. The loop then repeatedly removes the first future 
from the queue and inspects it. If its  running  it added back to the end of the queue, otherwise, we check whether 
the function raised an exception with a call to future.exception(). If it did we just ingore it.
If we didn't check this exception here, it would be raised when we called result() and could be handled through the 
normal try...except mechanism.
If no exception occurs , we can call reuslts() to get the return value. The function retruns a list of subdirs that 
are not symbolic links. The new subdirs are submitted to the executor and the resulting futures are tossed onto the queue 
to have thier contents seached in a later iteration.

And that's all that is required to develop a future-based I/O-bound application. Under the
hood, it's using the same thread or process APIs we've already discussed, but it provides a
more understandable interface and makes it easier to see the boundaries between
concurrently running functions (just don't try to access global variables from inside the
future!).

"""


        