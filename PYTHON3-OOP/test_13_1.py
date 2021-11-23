"""
Concurrency:
Is the art of making a computer do (or appear to do) multiple things at once. Simply means doing tow or more things 
simultaneously on seperate processor cores. 


Threads:
Often concurrency is created so that work continues while the program is waiting for I/O to happen. Eg. a server can start 
processing a new network request while it waits for data from a previous request to arrive Or an interactive program might 
render an animation or perform a calculation while waiting for the user to press a key. 
It's theoretically possible to manage all this switching between activities within your program, but it would be virtually 
impossble to get right. Instead, we rely on python and the os to take care of the tricky switching part, while we create 
object that appear to be running independently but simultaneously. These objects are called threads. 
Eg. below. 
"""
from threading import Thread 

class InputRead(Thread):
    def run(self):
        self.line_of_text = input() 
    
print("Enter some text and press enter: ") 
thread = InputRead() 
thread.start() 

count = result = 1 
while thread.is_alive():
    result = count * count 
    count += 1 

print(f"calculated squares up to {count} * {count} = {result}")
print(f"while you typed '{thread.line_of_text}'") 

"""
The example above runs two threads. Every program has (at least) one thread, called the main thread. The code that executes 
from startup is happening in this thread. Thet more visible second thread exists as the InputReader class. 
To construct a thread, we must extend the Thread class and implement the run method. Any code executed by the run method 
happens in a seperate thread. 
The new thread does not start running until we call the start() method on the object. In this case, the thread immediately 
pauses to wait for input from the keyboard. In the meantime, the original thread continues executing from the point start 
was called. Its starts calculating squares inside a while loop. The conditinon in the while loop checks whether the 
InputReader thread has exited its run method yet; once it does, it output some summary information to the screen 

"""
