"""
Functions are objcts too 
"""

def my_function():
    print("The Function was Called") 

my_function.description = "A silly function"


def second_function():
    print("The second was called") 

second_function.description = "A sillier function"

def another_function(function):
    print("The description:", end=" ")
    print(function.description) 
    print("The name:", end=" ")
    print(function.__name__) 
    print("The class:", end=" ") 
    print(function.__class__) 
    print("Now I'll call the function passed in")
    function() 

def sub(verbose=False):
    if verbose:
        another_function(my_function) 
        print("\n")
        another_function(second_function)



"""
Building an event-driven timer

The Timer class simply stores a list of upcoming events. 
It has a call_after method for add a new event. This method accepts a delay parameter 
"""
import datetime 
import time 

class TimedEvent:
    """
    This class stores only endtime and callbacks 
    """
    def __init__(self, endtime, callback):
        self.endtime = endtime 
        self.callback = callback 

    def ready(self):
        return self.endtime <= datetime.datetime.now()
    
class Timer:
    """
    Stores list of upcoming events 
    """
    def __init__(self):
        self.events = [] 
    
    def call_after(self, delay, callback):
        """
        This method accepts delay(number of seconds to execute callback) parameter and callback (a function to be executed at a correct time) parameter. 
        The callback function should accept one argument. 
        """
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        self.events.append(TimedEvent(end_time,callback))

    def run(self):
        """
        This method uses a generator expression to filter out any event whose time has come and executes them in order. 
        The timer looper run indifinately, thus it can be interupped with a Ctrl+C.
        We sleep for halp a second after each iteration to avoid grinding the system to halt. 
        """
        while True:
            ready_events = (e for e in self.events if e.ready())
            for event in ready_events:
                event.callback(self)
                self.events.remove(event)
            time.sleep(0.5)

# Sets of callbacks below 

def format_time(message, *args):
    now = datetime.datetime.now() 
    print(f"{now: %I:%M:%S}: {message}") 

def one(timer):
    format_time("Called One") 

def two(timer):
    format_time("Called Two")

def three(timer):
    format_time("Called Three")



class Repeater:
    def __init__(self):
        self.count = 0
    
    def repeater(self, time):
        format_time(f"repeat {self.count}") 
        self.count += 1
        timer.call_after(5, self.repeater)

timer = Timer() 
timer.call_after(1, one) 
timer.call_after(2, one) 
timer.call_after(2, two)
timer.call_after(4, two)
timer.call_after(3, three)
timer.call_after(6, three) 
repeater = Repeater()
timer.call_after(5, repeater.repeater) 
format_time("Starting")
timer.run()



