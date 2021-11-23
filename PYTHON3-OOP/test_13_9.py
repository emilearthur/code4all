"""
Using executors to wrap blocking code:
Asyncio provides its own version of the futures library to allow us to run code in a seperate thread or 
process when there isn't appropriate non-blocking call to be made.  This allows us to combine threads 
and processes with the asynchronous model. One of the more useful applications of this feature is to get the 
best of both worlds when an application has bursts of I/O-bound and CPU-bound activity. The I/O bound portions 
can happen in the event loop whiles the CPU-intensive work can spin off to different process. 

Eg. belwo is a sorting as a service using AsyncIO 

"""
import asyncio 
import json 
from concurrent.futures import ProcessPoolExecutor 

def sort_in_process(data):
    nums = json.loads(data.decode())
    curr = 1 
    while curr < len(nums):
        if nums[curr] >= nums[curr -1]:
            curr += 1
        else:
            nums[curr], nums[curr - 1] = nums[curr], nums[curr]
            if curr > 1:
                curr -= 1 
    return json.dumps(nums).encode()

async def sort_request(reader, writer):
    print("Recieved connection")
    length = await reader.read(8) 
    data = await reader.readexactly(int.from_bytes(length, "big"))
    result = await asyncio.get_event_loop().run_in_executor(None, sort_in_process, data) 
    print("Sorted list") 
    writer.write(result) 
    writer.close()
    print("Connection closed") 

loop = asyncio.get_event_loop() 
loop.set_default_executor(ProcessPoolExecutor()) 
server = loop.run_until_complete(asyncio.start_server(sort_request, "127.0.0.1", 2015))
print("Sort Service running") 

loop.run_forever() 
server.close() 
loop.run_until_complete(server.wait_closed()) 
loop.close()

"""
The idea of the cote implemented above is sorting as a service. Here we use our sorting algorithm instead of python's 
sorted. The alogorithm above called the gnome sort. It's a slow sort algorithm implemented in pure python. 
We define our own protocol instead of using one of the many perfect suitable application protocols that exist. 

In design, first, we are passing bytes into and out of the subprocess. This is a lot smarter than decoding the JSON 
in the main process. It means the (relatively expensive) decoding happens on a different CPU. 
Also, pickled JSON strings are generally smaller than pickled list so less data is passed between processes. 

Second, the two methods are very linear; it looks like code is being executed one line after
another. Of course, in AsyncIO, this is an illusion, but we don't have to worry about shared
memory or concurrency primitives.

Streams: 
The sort service eg. above has similar boilerplate to other AsyncIO programs, however, there are a few difference:
* We called start_server instead of create_server. This method hooks into AsyncIO's streams instead of using the 
underlying transport/protocol code. It allows us to pass in a normal coroutine, which receives reader and writer 
parameters. These both represent streams of bytes that can read from and written, like files or sockets. 
* Because is a TCP server instead of UDP, there is some socket cleanup required when the program finishes. The cleanup 
is blocking call, so we have to run the wait_closed coroutine on the event loop. 
Streams are fairly simple to understand. Reading is a potentially blocking call so we have to call with await. 
Writing doesn't block; it just puts the data in a queue, which AsyncIO sends out in the background. 
Our code inside the sort_request method makes two read requests:
* First, it reads 8 bytes from the wire and converts them to an integer using big endian notation. This integer 
represents the number of bytes of data the client intends to send. 
* The next call, to readexactly, it reads that many bytes. 
The difference between read and readexactly is that the former will read up to the requested number of bytes, while 
the latter will buffer reads until its recieves all of them or until the connection closes. 

Executor:
From the code above we imported the ProcessPoolExecutor. Here we did not need any special AsyncIO version of it. The event 
loop has a handy run_in_executor coroutine that we used to run features on. By default, the loop runs code in ThreadPoolExecutor,
but we can pass in a different executor if we wish, or as done above we can set a different default when we setup the event 
loop by calling loop.set_default_exector(). 
As stated in the beginning, there is not a lot of boilerplate for using features with an executor. However, when we use them 
with AsyncIO, there is none at all. The coroutine auto. wraps the function call in a feature and submits it to the executor. 
The code above blocks until the future completes, while the event loop continues processing other connections, tasks and futures. 
When the future is done, the coroutines wakes up and continues on to write the data back to the client. 

"""



