"""
Exploring the join method in threads. 
Below wec heck the current temperature in the capital city of each province and territory in Canada. 
"""
from threading import Thread 
import time 
from urllib.request import urlopen 
from xml.etree import ElementTree 

CITIES = {"Charlottetown": ("PE","s0000583"),
            "Edmonton": ("AB","s0000045"),
            "Fredericton": ("NB", "s0000250"),
            "Halifax": ("NS", "s0000318"),
            "Iwaluit": ("NU", "s0000394"),
            "Quebec City": ("QC", "s0000620"),
            "Regina": ("SK", "s0000788"),
            "St. John's": ("NL", "s0000280"),
            "Toronto": ("ON", "s0000458"),
            "Victoria": ("BC","s0000775"),
            "Whitehorse": ("YT","s0000825"),
            "Winnipeg": ("MB","s0000193"),
            "Yellowknife": ("NT", "s0000366"),           
        }

class TempGetter(Thread):
    def __init__(self, city):
        super().__init__() 
        self.city = city 
        self.province, self.code = CITIES[self.city]
    
    def run(self):
        url = ("http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/"
                f"{self.province}/{self.code}_e.xml")
        with urlopen(url) as stream:
            xml = ElementTree.parse(stream) 
            self.temperature = xml.find("currentConditions/temperature").text 

if __name__ == "__main__":
    threads = [TempGetter(c) for c in CITIES]
    start = time.time() 

    for thread in threads:
        thread.start() 

    for thread in threads:
        thread.join() 


    for thread in threads:
        #thread.run() # this runs code on single thread. to run comment on for loops before and thread start and join method.
        print(f"it is {thread.temperature}°C in {thread.city}")
    print(f"Got {len(threads)} temps in {time.time() - start}") 

"""
The code above constructs 10 threads before starting them. We override the constructor to pass them into the Thread objet by 
calling super().__init__, this ensures the Thread is properly initialized. 
Data constructed in one thread is accessible from other running thread, due to references to global variables inside the 
run method. The data passed into the constructor is being assigned to self in the main thread but is accessed inside the 
second thread. 
After 10 threads has been started, we loop over them again, calling the join() method on each. This method say wait for the 
thread to complete before doing anything. We call this ten times in sequence; this for loop won't exit untill all then threads 
have completed. 
After we pring temperature stored in each thread object. 
"""