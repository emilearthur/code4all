# function accepts a tuple and a date, and returns a tuple of the date and the middle value between the stock's high and low value

import datetime 

def middle(stock, date):
    symbol, current, high, low = stock 
    return ((high+low)/2, date) 


mid_value, date = middle(("FB", 177.46,178.67,175.79), datetime.date(2018,8,27))
print(mid_value, date)


# named tuples:  Named tuples are tuples with attitude. They are a great way to group read-only data together.
# The namedtuple constructor accepts two arguments. The first is an identifier for the named
# tuple. The second is a list of string attributes that the named tuple requires.

from collections import namedtuple
Stock = namedtuple("Stock", ["symbol", "current", "high", "low"])
stock = Stock("FB", 177.46, high=178.67, low=175.79)


# The resulting namedtuple can then be packed, unpacked, indexed, sliced, and otherwise
# treated like a normal tuple, but we can also access individual attributes on it as if it were an
#object:
print(stock.high) 

symbol, current, high, low = stock
print(current)


# Dataclasses are basically regular objects with a clean syntax for predefining attributes. 
# There are a few ways to create one, and we'll explore each in this section.
from dataclasses import make_dataclass
Stock = make_dataclass("Stock", ["symbol", "current", "high", "low"])
stock = Stock("FB", 177.46, high=178.67, low=175.79)
# we can add and modify some attributes 
stock.current=178.25
stock.unexpected_attribute = 'allowed'

# creating a class like the dataclasses 
class StockRegClass:
    def __init__(self, name, current, high, low):
        self.name = name
        self.current = current
        self.high = high
        self.low = low

stock_reg_class = Stock("FB", 177.46, high=178.67, low=175.79)

# an alternative (more common) way to define dataclass are below 
from dataclasses import dataclass 

@dataclass
class StockDecorated:
    name: str
    current: float
    high: float
    low: float


@dataclass 
class StockDefaults:
    name: str 
    currrent: float = 0.0
    high: float = 0.0
    low: float = 0.0


@dataclass(order=True)
class StockOrdered:
    name: str 
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0


stock_ordered1 = StockOrdered("FB", 177.46, high=178.67, low=175.79)
stock_ordered2 = StockOrdered("FB")
stock_ordered3 = StockOrdered("FB", 178.42, high=179.28, low=176.39)




