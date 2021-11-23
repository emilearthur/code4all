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
Running code:
i = Inventory() 
c = ConsoleObserver(i) 
i.attach(c) 
i.product = "Widget" 
i.quantity = 5

also try:
i = Inventory() 
c1 = ConsoleObserver(i)
c2 = ConsoleObserver(i)  
i.attach(c1) 
i.attach(c2) 
i.product = "Gadget"
"""


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

"""
The Strategy pattern:

The strategy pattern is a common demonstration of abstraction in OOP. The pattern implements different solutions
to a single problem, each in a different object. The client code can then choose the most appropriate
implementation dynamically at runtime. Typically, different algo. have different trade-offs, one might be faster 
than the other but uses a lot more memory, whiile a third algo. may be most suitable when multiple CPUs are 
present or a distrbuted system is provided. 

"""

"""
A Strategy Eg. 
A canonical eg. of the strategy pattern is sort runtines. Several algos have been implmented such as quicksort, 
merge sort & heap sort which are fast with different features.  
If we have client code that needs to sort a collection, we could pass it to an object with the sort() method. 
This object may be a QuickSorter or MergeSorter object but the results will be the same in either case: a sorted
list. The strategy used to do the sorting is abstracted from the calling code, making it modular and replaceable.

Considering a  desktop wallpaper manager. when an image is displayed on a desktop background, it can be adjusted 
to the screen size in different ways. For eg., assuming the image is smaller than the screen, it can be tiled 
across the screen, centered on it or scaled to fit. Others strategies include scaling to max. height or width, 
combining it with solid, semi-transparent or gradient background color or other manipulations. 

The strategy takes two two inputs; the image to be displayed and a tupe of the width and height of the screen. 
They each return a new image the size of the screen with image manipulated to fit according to the given strategy.

"""

from PIL import Image 
class TiledStrategy:
    def make_ground(self, img_file, desktop_size):
        in_img = Image.open(img_file) 
        out_img = Image.new("RGB", desktop_size) 
        num_tiles = [o // i + 1 for o, i in zip(out_img.size, in_img.size)]
        for x in range(num_tiles[0]):
            for y in range(num_tiles[1]):
                out_img.paste(in_img, (in_img.size[0] * x,
                                        in_img.size[1] * y,
                                        in_img.size[0] * (x + 1),
                                        in_img.size[1] * (y+1),),)
        return out_img

class CenteredStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file) 
        out_img = Image.new("RGB", desktop_size) 
        left = (out_img.size[0] - in_img.size[0]) // 2 
        top = (out_img.size[1] - out_img.size[1]) // 2 
        out_img.paste(in_img, (left, top, left + in_img.size[0], top + in_img.size[1]),)
        return out_img  

class ScaledStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file) 
        out_img = in_img.resize(desktop_size) 
        return out_img 

"""
Notes:
Considering swtiching b/n these options would be implemented without strategy pattern. We'd need to put all the 
code inside one big method and use if statement to select the expected one. Every time we want to add a new 
strategy, we'd have to make the edit the method. 
"""