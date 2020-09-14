"""
The abstract factory pattern:
The abstact factory pattern is normally used when we have multiple possible implementations of a system that depends on 
some configuration or platform issue. The calling code requests an object from the abstract factory, not knowing exactly 
what class of object will be returned. The underlying implementation returned may depend on a variety of factors, such 
as current locale, OS or local configuration. 
Eg_1. of abstract factory pattern include code for OS-independent toolkits, db backends, and country-specific formatters 
or calculators. Also an OS independent GUI toolkit might use abstract factory pattern that OS returns a set of WinForm 
widgets under Windows, Cocoa widget under Mac, GTK widget under Gnome and QT widget under KDE. 
Eg_2. Django provides an abstract factory that returns a set of object relational classes for interacting with specific 
db backend (MYSQL, PostgreSQL, SQLite and others) depending on a configuration setting for the current site. If the 
app. needs to be deployed in multiple places, each one can use a different db backend by changing only one configuration 
variable.
Eg_3. Differnet countries have different systems for calculating taxes, subtotals and totals on retail merchandise; 
an abstract factory can return a particular tex calculation object.  


There will be an abstract factory class that picks the specific factory, as well as a couple of example concrete 
factories, one for France and one for the USA. Each of these will create formatter objects for dates and times, 
which can be queried to format a specific value.
"""
class FranceDateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y, m, d))
        y = "20" + y if len(y) == 2 else y 
        m = "0" + m if len(m) == 1 else m 
        d = "0" + d if len(d) == 1 else d 
        return f"{d}/{m}/{y}" 


class USADateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y, m, d))
        y = "20" + y if len(y) == 2 else y 
        y = "0" + m if len(m) == 1 else m 
        d = "0" + d if len(d) == 1 else d
        return f"{m}-{d}-{y}"


class FranceCurrencyFormatter:
    def format_currency(self, base, cents):
        base, cents = (str(x) for x in (base, cents)) 
        if len(cents) == 0:
            cents = "00"
        elif len(cents) == 1:
            cents = "0" + cents 

        digits = [] 
        for i, c in enumerate(reversed(base)):
            if i and not i % 3 : 
                digits.append(" ") 
            digits.append(c) 
        base ="".join(reversed(digits)) 
        return f"{base}€{cents}"


class USACurrencyFormatter:
    def format_currency(self, base, cents):
        base, cents = (str(x) for x in (base, cents)) 
        if len(cents) == 0:
            cents = "00"
        elif len(cents) == 1:
            cents = "0" + cents 

        digits = [] 
        for i, c in enumerate(reversed(base)):
            if i and not i%3 :
                digits.append(",")
            digits.append(c) 
        base="".join(reversed(digits)) 
        return f"${base}.{cents}"

# Creating a formater factory 
class USAFormatterFactory:
    def create_date_formatter(self):
        return USADateFormatter()
    
    def create_currency_formatter(self):
        return USACurrencyFormatter() 
    

class FranceFormatterFactory:
    def create_date_formatter(self):
        return FranceDateFormatter()
    
    def create_currency_formatter(self):
        return FranceCurrencyFormatter()


# making the current formatter a modular-level variable instead of a singleton 
country_code = "US" # In practice this will based on the OS
factory_map = {"US": USAFormatterFactory, "FR":FranceFormatterFactory} #dict is used to associate the country code with 
#cont. factory class. Once we get the correct calls we instantiate it. 
formatter_factory = factory_map.get(country_code)() 

"""
Abstract factories often return a singleton object, but this is not required.  In the code above, it's returning a new 
instance of each formatter everytime it's called. 
We could also create module for each factory type and then ensure the correct module is accessed in a factory module. 

Below we import from the backends and set a current_backend variable to point to a specific module 
"""
from localize.backends import USA, France 

if country_code == "US":
    current_backend = USA 

