"""
The many problems with threads:
Queues:
If we need more control over communication between processes, we can use a Queue. 
Queue data structures are useful for sending messages from one process into one or more other processes. 
Any pickable object can be sent into Queue but remember that pickling can be a costly operation, so keep such object 
small. 
Eg. we build a little search engine for text content that stores all relevant enteries in memory. The search engine scans 
all files in the current directory in parallel. A process is constructed for each core on the CPU. Each of these is 
instructed to load some of the files into memoery. 
"""
def search(paths, query_q, results_q):
    lines = [] 
    for path in paths:
        lines.extend(l.strip() for l in path.open())
    
    query = query_q.get() 
    while query:
        results_q.put([l for l in lines if query in l]) 
        query = query_q.get() 

if __name__ == "__main__":
    from multiprocessing import Process, Queue, cpu_count 
    from path import Path
    cpus = cpu_count() 
    pathnames = [f for f in Path(".").listdir() if f.isfile()]
    paths = [pathnames[i::cpus] for i in range(cpus)]
    query_queues = [Queue() for p in range(cpus)]
    results_queue = Queue() 
    search_procs = [Process(target=search, args=(p, q, results_queue)) for p, q in zip(paths, query_queues)]
    for proc in search_procs:
        proc.start()
    
    for q in query_queues:
        q.put("def") 
        q.put(None) # signal process termination 
    
    for i in range(cpus):
        for match in results_queue.get():
            print(match)
    for proc in search_procs:
        proc.join()

