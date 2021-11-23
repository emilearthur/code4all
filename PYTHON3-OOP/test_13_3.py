"""
The many problems with threads:
Some pitfalls of threads. 

Shared memory:
The main advantage is having access to all the program's memory and all variable. However, this advantage is it main 
proble as it can easily cause inconsistencies in th program state. 

The solution to problem in threaded programming is to synchronize access to any code that reads or(especially) writes 
a shared variable. Synchronize solution works but its easy to forget and bugs due to inapproprate use of sync are hard 
to track down because the order in which threads perform operations is inconsistent. We can easily reproduce the error. 
Usually, it is safest to force communication between threads to happen using a lightweight data structure that already 
uses locks appropriately. Python offers the queue.Queue class to do this; it functionality is basically the same as 
multprocessing.Queue. 
In some cases, these disadvantages might be outweighed by the one advantage of allowing shared memory; it's fast. 
If multiple threads need access to a huge data structure, shared memory can provide that access quickly. 


The global interpreter lock:
In order to efficiently manage memory, garbage collection and calls to machine code in native libararies, Python has a 
utility called the global interpreter lock or GIL. It's impossible to turn off and it means that threads are useless in 
Python for one thing that they ecvel at in order langauges; parallel processing. The GIL's primary effect, for our purpose,
is to prevent any two threads from doing work (using CPU)  at the exact same time, even if they have work to do. Thus it's 
okay for multiple threads to access the disk or netowrk but GIL is released as soon as the thread start to wait for 
something. 


Thread overhead:
One limitation of threads is maintaining each thread. Each thread take up cetain amount of memory (both in python process
and the os kernal) to record the state of that thread. Switching between threads also uses a (small) amount of CPU time. 
This work happens seamlessly without extra coding (we just have to call start() and the rest is take care of), but the work 
still has to happen somewhere. 
Python provides Threadpool feature which handles structing workload so that threads can be reused to perform multiple jobs. 
Threadpool is part of multiprocessing library and behaves identically to ProcessPool. 


Multiprocessing:
Multiprocessing API was designed to mimic the Thread API. However, it has envolved in python3 and supports more features. 
The multiprocessing library is desinged for when CPU-intensive jobs need to happen in parallel and multiple cores are
avialable. Multiprocessing is not useful when processes  spend a majority of their time waiting on I/O(for eg; network, 
disk, db or keyboard) but it is the way to go for parallel computation. The multiprocessing module spins up new OS process 
to do the work. This means there is entirely seperate copy of the python interpreter running for each process.  
Eg. for parallize below
"""
from multiprocessing import Process, cpu_count 
from threading import Thread
import time 
import os 

class MuchCPU(Process):
    def run(self):
        print(os.getpid()) 
        for i in range(200000000):
            pass 

class MuchCPU_(Thread):
    def run(self):
        print(os.getpid()) 
        for i in range(200000000):
            pass 

if __name__ == "__main__":
    #procs = [MuchCPU() for f in range(cpu_count())] 
    procs = [MuchCPU_() for f in range(cpu_count())]
    t = time.time() 
    for p in procs:
        p.start() 
    for p in procs:
        p.join() 
    print(f"work took {time.time()-t} seconds")

"""
In the code above, we implemented a subclass of Process(instead of Thread) and implemented a run method. This method prints 
out the process ID (a unique number the os assigns to each process on the machine) before doing some intense (if misguided) 
work. 
In the code above the if __name__ == "__main__" guards around the module level code that prevents it running if the module 
is being imported, rather than run as a program. This is a good practice in general. Behind the scens, multiprocessing may 
have to reimport the module inside the new process in order to execute the run() method.  If we allow the entire module to 
execute at that point, it would start creating new processes recursively until the os ran out of resources, crashing your 
computer. We construct one process for each processor core on our machine, then start and join each of those processes. 

Replace Process with Thread, the time the process run is longer. Thread takes twice the time of Process. This is the cost 
of the GIL; in other languages, the threaded version would run at least as fast as the multiprocessing version. 
"""