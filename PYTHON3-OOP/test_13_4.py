"""
The many problems with threads:
Multiprocessing pools:
In general, there is no reason to have more processes than there are processors on the computer. There are few reason for 
this:
    * only cpu_count() processes can run simultaneously 
    * each process consumes resources with a full copy of the Python interpreter 
    * Communication between processes is expensive 
    * Creating processes takes a non-zero amount of time 

Given these contstaints, it makes sense to create at most cpu_count() processes when the program starts and then have them 
execute tasks as needed. THis has much less overhead than starting a new process for each task. 

Pools abstract away the overhead of figuring out what code is executing in the main process and which code is running in the 
subprocess. The pool abstraction restricts the number of places in which code in different processes interacts, making it 
much easier to keep track of. 
Unlike threads, multiprocessing cannot directly access variables set up by other threads. Multiprocessing provides a few 
different ways to implement interprocess communication. Pools seamlessly hide the process of passing data between processes. 
Using a pool looks much like a function call: you pass data into a function, it is executed in another process or processes, 
and when the work is done, a value is returned. Underhood; objects in one process are being pickled and passed into an os 
process pipe. Then another process retrieves data from the pipe and unpickles it. The requested work is done in the 
subprocess and a result is produced. THe result is pickled and passed back thorugh the pipe. Eventually, the original process 
unpickles and returns it. All this pickling and passing data into pipes takes time and memory. Therefore, it is ideal to 
keep the amount and size of data passed into and returned from the pool to a minimum, and it is only advantageous to use the 
pool if a lot of processing has to be done on the data in question. 

Notes: Pickling is an expensive operation for even medium-sized Python operations. It is frequently more expensive to 
pickle a large object for use in a separate process than it would be to do the work in the original process using threads. 
Make sure you profile your program to ensure the overhead of multiprocessing is actually worth the overhead of implementing
and maintaining it.

Below we calculate all prime factors of a list of randomnumbers. This is common and expensive in crypto. algo. 
It requires years of processing power to crack the extremely large numbers used to secure accoutns. The ff. implementation 
below, while readable, is not at all efficient, but that's okay since we want to see it using lots of CPU time. 

"""
from code_sample import results
import random
from typing import List
from multiprocessing.pool import Pool 

def prime_factor(value: int) -> List:
    factors = []
    for divisor in range(2, value-1):
        quotient, remainder = divmod(value, divisor)
        if not remainder:
            factors.extend(prime_factor(divisor)) #recursive 
            factors.extend(prime_factor(quotient)) #recursive 
            break
    else:
        factors = [value]
    return factors
"""
if __name__ == "__main__":
    pool = Pool() 

    to_factor = [random.randint(100000, 50000000) for i in range(20)]
    results = pool.map(prime_factor, to_factor) 
    for value, factors in zip(to_factor, results):
        print(f"The factors of {value} are {factors}") 
"""

"""
We first construct a multiprocessing pool instance. By default, this pool creates a seperate process for each of the CPU 
cores in the machine it is running on. 
The map method accepts a function and an iterable. The pool pickles each of the value in the iterable and passes it into 
an available process, which executes the function on it. When that process is finished doign its work, it pickles the 
resulting list of factors and passes it back to the pool. Then, if the pool has more work available, it takes on the next 
job. Once all the pools are finished processing work (which cold take some time), the results list is passed back to the 
original process, which has been waiting patiently for all this work to complete. 

Below is using map_async method. Here we return a list of values later by calling results.get() method. This promise 
object also has methods such as ready() and wait(), which allow us to check whether all the results are in yet
"""
"""
if __name__ == "__main__":
    pool = Pool() 

    to_factor = [random.randint(100000, 50000000) for i in range(20)]
    results = pool.map_async(prime_factor, to_factor)
    for value, factors in zip(to_factor, results.get()):
        print(f"The factors of {value} are {factors}") 
"""

"""
Alternatively, if we don't know all the values we want to get results for in advance, we can
use the apply_async method to queue up a single job.  If the pool has a process that isn't
already working, it will start immediately; otherwise, it will hold onto the task until there is
a free process available. Pools can also be closed, which refuses to take any further tasks, but processes everything
currently in the queue, or terminated, which goes one step further and refuses to start any jobs still in the queue, 
although any jobs currently running are still permitted to complete.
Implementation below 
"""
if __name__ == "__main__":
    pool = Pool()
    to_factor = [random.randint(100000, 50000000) for i in range(20)]
    multi_results = [pool.apply_async(prime_factor, (i,)) for i in to_factor]
    for value, factors in zip(to_factor,[result.get() for result in multi_results]):
        print(f"The factors of {value} are {factors}") 
    pool.close()