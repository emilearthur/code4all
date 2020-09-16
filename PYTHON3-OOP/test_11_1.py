"""
Python Design Pattern II:

The adapter pattern:
The adapter pattern is designed to interact with existing code. We would not design a brand new set of objects that 
implement the adapter pattern. Adapters are used to allow two pre-existing objects to work together, even if their 
interfaces are not compactible. The adapter object's sole purpose is to perform this translation.  
Adapting may entail a variety of tasks such as converting arguments to a different format, rearranging the order of 
args. calling a differently named method or supplying defaults args. 

In some case; the adapter pattern is similar to a simplified decorator pattern. Decorators typically procide the same 
interface that they replace, whereas adapters map b/n two difference interfaces. 

Eg below: imagine we have the ff. preexisting class, which takes a string date in the format YYYY-MM-DD and calculates 
a person's age on that date. 

"""
class AgeCalculator:
    def __init__(self, birthday):
        self.year, self.month, self.day = (int(x) for x in birthday.split("-"))

    def calculate_age(self, date):
        year, month, day = (int(x) for x in date.split("-"))
        age = year - self.year 
        if (month,day) < (self.month, self.day):
            age -= 1
        return age 


# An adapter that allows a noraml date to be plugged into a normal AgeCalculator class
import datetime
from email import message
from os import set_inheritable

class DataAgeAdapter:
    """This adapter converts datetime.date adn datetime.time into a string that 
    Age calculator can use. 
    """
    def _str_date(self, date):
        return date.strftime("%Y-%m-%d") 
    
    def __init__(self, birtday):
        birthday = self._str_date(birtday) 
        self.calculator = AgeCalculator(birthday)
    
    def get_age(self, date):
        date = self._str_date(date)
        return self.calculator.calculate_age(date) 

import datetime 
class AgeableDate(datetime.date):
    """
    Using inheritance, we add an adapter on date class to that it works with the original AgeCalculator class.
    """
    def split(self, char):
        return self.year, self.month, self.day 

"""
RUN:
bd = AgeableDate(1975, 6, 14) 
today = AgeableDate.today() 
a = AgeCalculator(bd) 
a.calculate_age(today) 

Notes: 
 
"""

"""
The facade pattern:
The facade pattern is designed to provide a simpel interface to a complex system of components. For complex tasks, we 
may need to interact with these objects directly but there is often a typical usage for the system for which these 
complicated interactions aren't necessary. The facade patternn allows us to define a new object that encapsulates this 
typical usage of the system. Anytime we want access to common functionality, we can use the single object's simplified
interface. If another part of the project needs access to more complicated functionlity, it is still able to interact 
with the system directly. Facade pattern is really dependent on subsystems. 
A facade is like an adapter, however the primary difference is that a facade tries to abstract a simpler interface out
of a complex one whiles an adapter only tries to map one existing interface to another. 

Eg. below: A simple email application. Here we create a simple class that allows us to send a single email and 
list the emails currently in the inbox on an IMAP or POP3 connection. Here our facade performs two tasks: *sending 
email to a specific address * checking the inbox on an IMAP connection. It makes some common assumptions about 
connection, such as the host for both SMTP and IMAP is at the same address, that the username and password for both 
is the same and that they use standard ports. 
This covers the case for many email servers, but if a programmer needs more flexibility, they can always bypass the
facade and access the two subsystems directly.

"""
# Initializing with the hostname of the email server, a usernae and a password to login 
import smtplib 
import imaplib 

class EmailFacade:
    def __init__(self, host, username, password):
        self.host = host 
        self.username = username 
        self.password = password 

    def send_email(self, to_email, subject, message):
        """This method formats the email address and message and sends it using stmplib. 
        """
        if not "@" in self.username:
            from_email = f"{self.username}@{self.host}"
        else:
            from_email = self.username
        message = ("From: {0}\r\n" "To: {1}\r\n" "Subject: {2}\r\n\r\n{3}").format(from_email, to_email, subject, 
                                                                                                            message)
        smtp = smtplib.SMTP(self.host) 
        smtp.login(self.username, self.password) 
        smtp.sendmail(from_email, [to_email], message)
    
    def get_inbox(self):
        """Get the message currently in the inbox
        """
        mailbox = imaplib.IMAP4(self.host)
        mailbox.login(bytes(self.username, "utf8"), bytes(self.password, "utf8"))
        mailbox.select() 
        x, data  = mailbox.search(None, "ALL") 
        messages = [] 
        for num in data[0].split():
            x, message = mailbox.fetch(num, "(RFC822)")
            messages.append(message[0][1])
        return messages 


"""
The flyweight pattern:
The flyweight pattern is a memory optimization pattern. Often times memory optimization is ignored, as it assumed that 
built-in garbage collector will take care of them. However, when building large applications with many related objects, 
paying attention to memory concerns can have a huge payoff. 
The flyweight pattern ensure that objects that share a state can use the same memory for the shared state.
It's normally implmented only after a program has demonstrated memory problems. It may make sense to design an optimal 
configuration from the beginning in some situations, but put in mind that premature optimizaiton is the most effective 
way to create a program that is too complicated to maintain. 
Each Flyweight has no specific state. Any time it needs to perform an operation on SpecificState, that state needs to 
be passed into the Flyweight by the calling code.

Flyweight factory is often implmented using the __new__ constructor, similar to what we did with the singleton pattern. 
Unlike the singleton pattern, which only needs to return one instance of the class, we need to be able to return 
different instances depending on the keys. 
This solution is problematic because the item will remain in memory as long as it is in the dictionary. We solve this 
by taking advantage of Python's weakref module. This module provides a WeakValueDictionary object, which basically 
allows us to store items in a dictionary without the garbage collector caring about them. If a value is in weak 
referenced dictionary and there are no other references to that object store anywhere in the application, the garbage
collector will eventually clean up for us

Eg. below: build the factory for our flyweights first . 
"""
import weakref
import gc 

class CarModel:
    _models = weakref.WeakValueDictionary() 

    def __new__(cls, model_name, *args, **kwargs):
        model = cls._models.get(model_name)
        if not model:
            model = super().__new__(cls)
            cls._models[model_name] = model 
        return model 
    
    def __init__(self, model_name, air=False, tilt=False, cruise_control=False, power_locks=False, alloy_wheels=False,
                 usb_charger=False,):
        if not hasattr(self, "initted"): #make sure we only initilaize the objet first time __init__ is called
            self.model_name = model_name 
            self.air = air 
            self.tilt = tilt
            self.cruise_control = cruise_control 
            self.power_locks = power_locks 
            self.alloy_wheels = alloy_wheels 
            self.usb_charger = usb_charger 
            self.initted = True 

    def check_serial(self, serial_number):
        """
        Looks up a serial number on a specific model of vechile an determines whether it has been involved in any 
        accident. 
        """
        print(f"Sorry, we are unable to check the serial number {serial_number} on the {self.model_name} at the time")


class Car:
    def __init__(self, model, color, serial):
        """
        Stores addition information as well as reference to the flyweight

        """
        self.model = model 
        self.color = color 
        self.serial = serial

    def check_serial(self):
        return self.model.check_serial(self.serial) 

"""
Run:
dx = CarModel("FIT DX")
lx = CarModel("FIT LX", air=True, cruise_control=True, power_locks=True, tilt=True)
car1 = Car(dx, "blue", "12345")
car2 = Car(dx, "black", "12346")
car3 = Car(lx, "red", "12347")
demonstrating weak referencing 
id(lx) 
del lx 
del car3 
gc.collect()
lx = CarModel("FIT LX", air=True, cruise_control=True, power_locks=True, tilt=True)
id(lx)
lx = CarModel("FIT LX")

id(lx) 
lx.air 
"""

"""
Notes: The flyweight pattern is designed for conserving memory; if we have hundreds of thousand of siimilar objects, 
combining similar properties into a flyweight can have an enormous impact on memory consumption. 
It is common for programming solutions that optimize CPU, memory, or disk space to result in more complicated code 
than their unoptimized brethren. It is therefore important to weigh up the trade-offs when deciding between code 
maintainability and optimization. When choosing optimization, try to use patterns such as flyweight to ensure that the
complexity introduced by optimization is confined to a single (well-documented) section of the code.

"""


"""
The command pattern:
The command pattern adds a level of abstraction between actions that must be done and the object that invokes those 
actions, normally at a later time. In the command pattern, client code creates a command object that can be executed at
a later later. 
This object know about a receiver object that manages its own internal state when the command is execute or do_action 
method, and keeps track of any arguments required to perform the action. Finallly, one or more invoker objects execute 
the command at the correct time. 
A common eg. of the command pattern is acitons on a graphical window. Often, an action can be invoked by a menu item on 
the menu bar, a keyboard shortcut or a toolbar icon, or a context menu => These are all examples of Invoker objects. 
The actions tha actually occur, such as Exit, Save or Copy are implementations of CommandInterfcace. 
A GUI window to recieve exit, a document to recieve save, and ClipboardManager to recieve copy commands are all eg. of 
possible Recievers. 

Eg.: Let's implement a simple cmd pattern that provides commands for Save and Exit actions.  We'll start with some 
modest receiver classes. 

"""
import sys 

class Window:
    def exit(self):
        sys.exit(0) 

class Document:
    def __init__(self, filename):
        self.filename = filename 
        self.contents = "This file cannot be modified" 
    
    def save(self):
        with open(self.filename, "w") as file:
            file.write(self.contents) 

# Define some invoker classes. These will model toolbar, menu and keyboard events that can happen; again, they aren't 
# actually hooked up to anything, but we can use how they are decoupled from the command, receiever and client code 
# as below 

class ToolbarButton:
    def __init__(self, name, iconname):
        self.name = name 
        self.iconname = iconname 

    def click(self):
        self.command.execute() 


class MenuItem:
    def __init__(self, menu_name, menuitem_name):
        self.menu_name = menu_name
        self.menuitem_name = menuitem_name

    def click(self):
        self.command.execute() 


class KeyboardShortcut:
    def __init__(self, key, modifier):
        self.key = key 
        self.modifier = modifier  
    
    def keypress(self):
        self.command.execute() 


#Notes: Notice how the various action methods each call the execute method on thier respective commands? THis code does 
#not show the commnand attribute being set on each object. They coulld be passed into the __init__ function, but becos 
#they may be change with eg. keybinding editor, it makes more sense to set attributes on the objects aftwards. 

# Hookup commands themselves. 
class SaveCommand:
    def __init__(self, document):
        self.document = document 
    
    def execute(self):
        self.document.save()


class ExitCommand:
    def __init__(self, window):
        self.window = window 
    
    def execute(self):
        self.window.exit() 

# Testing  
window = Window()
document = Document("a_document.txt") 
save = SaveCommand(document) 
exit = ExitCommand(window)

save_buttom = ToolbarButton("save", "save.png")
save_buttom.command = save 
save_keystroke = KeyboardShortcut("s","ctrl") 
save_keystroke.command = save
exit_menu = MenuItem("File", "Exit")
exit_menu.command = exit 


"""
Notes:
The code above is not pythonic since it have lots of boilerplate code (code that is does 
not accomplish anything, but only procide structure to the pattern), and the Command 
classes are all eerily similar to each other. But we could create a generic command 
object that takes a function as a callback.  
Here we write a function aand use that as the command directly. 

# Re-writting the function in a pythonic way """
import sys 

class Window:
    def exit(self):
        sys.exit(0) 


class MenuItem:
    def click(self):
        self.command() 

window = Window() 
menu_item = MenuItem() 
menu_item.command = window.exit


class Document:
    def __init__(self, filename):
        self.filename = filename 
        self.contents = "This file cannnot be modified" 
    
    def save(self):
        with open(self.filename, "w") as file:
            file.write(self.contents) 


class KeyboardShortcut:
    def keypress(self):
        self.commmand() 


class SaveCommand:
    def __init__(self, document):
        self.document = document 
    
    def __call__(self):
        self.document.save() 

document = Document("a_file.txt")
shortcut = KeyboardShortcut()
save_command = SaveCommand(document) 
shortcut.command = save_command

"""
Here, we have something that looks like the first command pattern, but a bit more
idiomatic. As you can see, making the invoker call a callable instead of a command object
with an execute method has not restricted us in any way. In fact, it's given us more
flexibility. We can link to functions directly when that works, yet we can build a complete
callable command object when the situation calls for it.
The command pattern is often extended to support undoable commands. For example, a
text program may wrap each insertion in a separate command with not only an execute
method, but also an undo method that will delete that insertion. A graphics program may
wrap each drawing action (rectangle, line, freehand pixels, and so on) in a command that
has an undo method that resets the pixels to their original state. In such cases, the
decoupling of the command pattern is much more obviously useful, because each action
has to maintain enough of its state to undo that action at a later date.

"""
