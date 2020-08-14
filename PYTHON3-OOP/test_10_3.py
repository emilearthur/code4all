"""
The observer pattern. 
The observer pattern is useful for moinitoring and event handing situations. This pattern allow a given object to be 
monitored by an unknown and dynamic group of observer objects. Whenever a value on the core object changes, it lets all the 
observer objects know that a change has occured by calling an update() method.  Each observer may be responsible for 
different tasks whenever the core object changes; the core objects does't know or care what those tasks are and same for the 
observer as to what other observes are doing. 

Observer pattern might be useful in a redundant backup system. We can write a core object that maintains certain values, and
then have one or more observers create serialized copies of that object.
Eg below. 
"""

# implementing core object using properties 
class Inventory:
    def __init__(self):
        self.observers = []
        self._product = None 
        self._quantity = 0
    
    def attach(self, observer):
        self.observers.append(observer) 
    
    @property 
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value 
        self._update_observers()
    
    @property
    def quantity(self):
        return self._quantity 
    
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self._update_observers()

    def _update_observers(self):
        for observer in self.observers:
            observer() 

# implementing a obsever object 
class ConsoleObserver:
    def __init__(self, inventory):
        self.inventory = inventory

    def __call__(self):
        print(self.inventory.product) 
        print(self.inventory.quantity) 


"""
Notes:

This time when we change the product, there are two sets of output, one for each observer.
The key idea here is that we can easily add totally different types of observers that back up
the data in a file, database, or internet application at the same time.
The observer pattern detaches the code being observed from the code doing the observing.
If we were not using this pattern, we would have had to put code in each of the properties
to handle the different cases that might come up; logging to the console, updating a
database or file, and so on. The code for each of these tasks would all be mixed in with the
observed object. Maintaining it would be a nightmare, and adding new monitoring
functionality at a later date would be painful.

"""