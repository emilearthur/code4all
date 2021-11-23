"""
Reading an AsyncIO Future:
An AsyncIO coroutine executes each line in order until it encouters an await statement, at which point, it returns 
control to the event loop. The event loop then executes any other tasks that are ready to run, including the one that the 
original coroutine was waiting on. Whenever that child task completes, the evnt loop send the results back into the coroutine 
so that it can pick up execution until it encounters another await statement or returns. 
This allows us to write code that executes synchronously until we explicitly need to wait for something. As a result, 
there is no nondeterminstic behavior of threads, so we don't need to worry nearly so much about shared state. 

Notes: Its a goood idea to aviod accessing share state from inside a coroutines. It makes code much easier to reason about. 

Also, AsyncIO allows us to collect logical sections of code together inside a single coroutines, even if we are waiting 
for other work elsewhere.
As a specific instance, even though the await asyncio.sleep call in the random_sleep coroutine is allowing a ton
of stuff to happen inside the event loop, the coroutine itself looks like it's doing everything in order. This ability to
read related pieces of asynchronous code without worrying about the machinery that waits for tasks to complete is the 
primary benefit of the AsyncIO module.
"""

"""
AsyncIO for networking:
Here we build a basic feature of a DNS server. The DNS's basic purpose is to translate domain name such as https://fidocredit.com 
into IP addresses, such as IPv4 addresses (for eg 23.253.135.79) or IPv6 addresses (eg 2001:4802:7901:0:e60a:1375:0:6).
It has to be able to perform many types of queries and know how to contact other DNS servers if it doesn't have the answer 
required. The example below is to be able to respond directly to a standard DNS quuery to lookup IPs for a few sites:

"""
import asyncio 
from contextlib import suppress 
from typing import Tuple

ip_map = {
    b"facebook.com.": "173.252.120.6",
    b"yougov.com.": "213.52.133.246",
    b"wipo.int." : "193.5.93.80",
    b"dataquest.io.": "104.20.20.199",
}



def lookup_dns(data):
    domain = b""
    pointer, part_length = 13, data[12] 
    while part_length:
        domain += data[pointer : pointer + part_length] + b"." 
        pointer += part_length + 1 
        part_length = data[pointer - 1] 
    
    ip = ip_map.get(domain, "127.0.0.1")
    return domain, ip 

def create_response(data, ip):
    ba = bytearray 
    packet = ba(data[:2]) + ba([129, 128]) + data[4:6] * 2 
    packet += ba(4) + data[12:] 
    packet += ba([192, 12, 0, 1, 0, 1, 0, 0, 0, 60, 0, 4])
    for x in ip.split("."):
        packet.append(int(x))
    return packet 


class DNSProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport) -> None:
        self.transport = transport 

    def datagram_received(self, data:bytes, addr: Tuple[str, int]) -> None:
        print(f"Recieved request from {addr[0]}") 
        domain, ip = lookup_dns(data) 
        print(f"Sending IP {domain.decode()} for {ip} to {addr[0]}")
        self.transport.sendto(create_response(data, ip), addr) 

loop = asyncio.get_event_loop() 
transport, protocol = loop.run_until_complete(loop.create_datagram_endpoint(
    DNSProtocol, local_addr=("127.0.0.1", 4343)
    )
)
print("DNS Server running") 

with suppress(KeyboardInterrupt):
    loop.run_forever() 
transport.close()
loop.close()



"""
Notes: 
The code above sets up a dict. that maps a few domains to IPv4 addresses. It followed by two function that 
extract information from a binary DNS query packet and construct the response. 
AsyncIO networking revolves around the intimately linked concepts of transports and protocols. A protocol 
is a class that has specific methods that are called when relevant events happen. Since DNS runs on top 
of UDP, we build the protocol class as a subclass of DatagramProtocol.  
For DNS, each recieved datagram must be parsed and responded to, at which point, the interaction is over. 

Thus, when a datagram is recieved, we process the packet, lookup the IP and construct a response using the 
functions we arent talking about. Then , we instruct the underlying transport to send the resulting packet 
back to the requesting client using sendto method. 
The transport represents a communication stream, thus abstracting away all the fuss of sending and receiving 
data on a UDP socket on an event loop. 

The UDP transport is constructed by calling the loop's create_datagram_endpoint coroutine. This constructs 
the appropiate UDP socket and start listening on it. We pass it the address that the socket needs to listen on 
and more importantly the protocl class we created so that the transport know what to call when it receives 
the data. 

Since the process of initializing a socket takes a non-trivial amount of time and would block the event loop,
the create_datagram_endpoint function is a coroutine. In our example, we don't need to do anything while we
wait for this initialization, so we wrap the call in loop.run_until_complete. The event loop takes care of 
managing the future, and when it's complete, it returns a tuple of two values: the newly initialized 
transport and the protocol object that was constructed from the class we passed in.

Behind the scenes, the transport has set up a task on the event loop that is listening for
incoming UDP connections. All we have to do, then, is start the event loop running with the
call to loop.run_forever() so that the task can process these packets. When the packets
arrive, they are processed on the protocol and everything just works.

The only other major thing to pay attention to is that transports (and, indeed, event loops)
are supposed to be closed when we are finished with them. In this case, the code runs just
fine without the two calls to close(), but if we were constructing transports on the fly (or
just doing proper error handling!), we'd need to be quite a bit more conscious of it.
You may have been dismayed to see how much boilerplate is required in setting up a
protocol class and the underlying transport. AsyncIO provides an abstraction on top of
these two key concepts, called streams. We'll see an example of streams in the TCP server in
the next example.



"""

