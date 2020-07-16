"""
Using functions are attributes

Functions can also be also set as callable attributes on other objects. 
"""

class A:
    def print(self):
        print("my class is A") 
    
def fake_print():
        print("my class is not A") 

a = A()
a.print()
a.print = fake_print
a.print()



"""
Just as function are objects that can have attributes set on them, it is possible to create an object that can be called as though it were a function. 

Any object can be made callable by simply giving it a  __call__ method that accepts the required args. Making our repeater class in test_7_7.py easier by making it a callable 
below
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


def format_time(message, *args):
    now = datetime.datetime.now() 
    print(f"{now: %I:%M:%S}: {message}") 


class Repeater:
        def __init__(self):
                self.count = 0

        def __call__(self, timer):
                format_time(f"repeat {self.count}") 
                self.count += 1 
                timer.call_after(5, self)

timer = Timer() 

timer.call_after(5, Repeater()) 
format_time("{now} : Starting") 
timer.run()