"""
AsyncIO Clients:

Because it is capable of handling many thousands of simultaneous connections, AsyncIO is very common for implmentating servers. 
However, it is a generic networking library and provides full support for client processes as well. This is importnat since 
many microservers run servers that act as clients to other servers. 

Clients can be much simpler than servers, as they don't have to be set up to wait for incoming connnections. Like most networking 
libraries, you just open a connection, submit your requests and process any responses. The main difference is that you need 
to use await anytime you make a potentially blocking call. 

Below is an client example for sort service implmented in test_13_9.py

"""
import asyncio 
import random 
import json 

async def remote_sort():
    reader, writer = await asyncio.open_connection("127.0.0.1", 2015) 
    print("Generating random list...") 
    numbers = [random.randrange(10000) for r in range(10000)]
    data = json.dumps(numbers).encode() 
    print("List Generated, sending data")
    writer.write(len(data).to_bytes(8, "big")) 
    writer.write(data) 

    print("Waiting for data...") 
    data = await reader.readexactly(len(data))
    print("Received data") 
    sorted_values = json.loads(data.decode()) 
    print(sorted_values)
    print("\n") 
    writer.close() 

loop = asyncio.get_event_loop() 
loop.run_until_complete(remote_sort()) 
loop.close()
