"""
AsyncIO: It combines the concept of futures and an event loop with coroutines. 
AsnycIO can be used for a few different concurrent tasks, but it was specifically designed 
for network I/O. Most networking apps, especially on the server side spend a lot of time 
waiting for data to come from the netowrk. This can be solved by handling each client in a 
seperate thread, but threads use up memory and other resources. AsyncIO uses coroutines as 
a sort of lightweight thread. 

The library provides its own event loop, avoiding the need for several lines long the while 
loop. However, event lopps come with a cost. When we run code in an async task on the 
event loop, that code must return immediately, blocking neither on I/O nor on long-running 
calculations. This is a minor thing when writing our own code, but it means that any 
standard library or third-party functions that block on I/O have to have non-blocking version 
created. 

AsyncIO solves this by creating a set of coroutines that use a sync and await syntax to 
return control to the event loop immediately when code will block. These keywords repalce 
the yield, yield from and send syntax we use in the raw coroutines as well as the need to 
manually advance to the first send location. This results in concurrent code that we can 
reason about as if it were sequential. The event loop takes care of checking whether the 
blocking call has completed and performing any subsequent task. 

An example of blocking function is time.sleep call.
Illustrating the basics of AsyncIO event loop below. 

"""
import asyncio
import random 

async def random_sleep(counter):
    delay = random.random() * 5
    print(f"{counter} sleeps for {round(delay,2)} seconds") 
    await asyncio.sleep(delay) 
    print(f"{counter} awakens") 

async def five_sleepers():
    print("Creating five tasks") 
    tasks = [asyncio.create_task(random_sleep(i+1)) for i in range(10)] 
    print("Sleeping after starting five tasks")
    await asyncio.sleep(2) 
    print("Walking and waiting for five tasks") 
    await asyncio.gather(*tasks)

asyncio.get_event_loop().run_until_complete(five_sleepers()) 
print("Done five tasks")

"""
Notes: 
The code above covers several features of AsyncIO programming.The five_sleepers function gets the event loop and instructs 
it to run a task until it is finished. Once that task has done its work, the loop will exit and the code will terminate. 
A task is an object that asyncio knows how to schedule on the event loop. It includes:
* Coroutines defined with the async and await syntax. 
* Coroutines decorated with @asyncio.coroutine and using the yield from syntax. 
* asyncio.Future objects. THese are almost identical to the concurrent.features . 
* Any awaitable object, that is, one with an __await__ function. 

Looking an the function five_sleepers; coroutines first constructs five instance of the random_sleep coroutines. These are 
wrapped in a asyncio.create_task call, which adds the future to the loop's task queue so they can execute and start immediately 
when control is returned to the loop. That control is returned whenever we call await(ie. await asyncio.sleeep to pause 
the execution of the coroutine for two seconds). During the break, the event loop executes the tasks that it has queued up:
namely, the five random_sleep tasks. 
When the sleep call in the five_sleepers task wakes up, it calls asyncio.gather. This function accepts tasks ar varargs, 
and awaits each of them (among other things, to keep the loop running safely) before returning. Each of the random_sleep 
coroutines prints a starting message, then send control back to the event loop for a specifi amount of time using its 
own await calls. When the sleep has completed, the event loop passes control back to the relevant random_sleeep tasks, 
which prints its awakening messsage before returning. Each of th random_sleep coroutines prints a starting message, then 
sends control back to the event loop for specific amount of time using its own await calls. When the sleep has completed, 
the event loop passes control back to the relevant random_sleep task, which prints its awakening message before returning. 
Note that any tasks that less than two seconds to complete will output their own awakening message before the original 
five_sleepers coroutines awakes to run  until gatber task is called. Since the event queue is now empty (all six coroutines
have to run to complettion and are not awaiting any tasks), the run_until_complete call is able to terminate the program 
ends. 

The async keyword acts as documentation notifying the python interpreter (and coder) that the coroutine contains the await 
calls. It also does some work to prepare the coroutine to run on the event loop. It behaves much like a decorator. 



"""