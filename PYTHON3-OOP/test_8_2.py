"""
Since template stings are sometimes difficult to understand. 
Alternatively one can create an object or class which can execute object lookups or even call methods 
inside the f-string. 

"""
class EMail:
    def __init__(self, from_addr, to_addr, subject, message):
        self.from_addr = from_addr 
        self.to_addr = to_addr
        self.subject = subject 
        self._message = message 

    def message(self):
        return self._message 

email = EMail("a@example.com","b@example.com", "You are Late","Here's some mail for you!",)

formatted = f"""
From: <{email.from_addr}>
To: <{email.to_addr}>
Subject: {email.subject}

{email.message()}
"""
print(formatted)


"""
Making it look right. 
It's nice to be able to include variables in template strings, but sometimes the variables need
a bit of coercion to make them look the way we want them to in the output.
"""
subtotal = 12.32
tax = subtotal*0.07
total = subtotal + tax 

print("Sub: ${0:0.2f} Tax: ${1:0.2f} Total: ${total:0.2f}".format(subtotal, tax, total=total))

print("\n")

orders = [("burger", 2, 5), ("fries", 3.5, 1), ("cola", 1.75, 3)]
print("PRODUCT QUANTITY PRICE SUBTOTAL")
for product, price, quantity in orders:
    subtotal = price * quantity 
    print(
        f"{product:10s}{quantity: ^9d} "
        f"${price: <8.2f}${subtotal: >7.2f}")


"""
Custom formatters:

While these standard formatters apply to most built-in objects, it is also possible for other
objects to define nonstandard specifiers. For example, if we pass a datetime object into
format, we can use the specifiers used in the datetime.strftime function, as follows:

"""


print("\n")
import datetime
from os import replace 
print("{the_date:%Y-%m-%d %I:%M%p }".format(the_date=datetime.datetime.now()))


"""
The format method:

The format method behaves similarly to f-strings, but there are a couple of differences:
1. It is restricted in what it can look up. You can access attributes on objects or look
up an index in a list or dict, but you can't call a function inside the template
string.
2. You can use integers to access positional arguments passed to the format
method: "{0} world".format('bonjour'). The indexes are optional if you
specify the variables in order: "{} {}".format('hello', 'world').
Eg. is below 

"""
template = "abc{number:*^10d}"
print(template.format(number=32))

"""
Strings are Unicode 

Converting bytes to text:
If we have an array of bytes from somewhere, we can convert it to Unicode using the .decode method on bytes class 
There are many such names; common ones for Western Languages include ASCII, UTF-8 and latin-1. 
eg below
"""
print("\n")
characters = b'\x63\x6c\x69\x63\x68\xe9' # create a byte object. b'' tels it that we creating a byte object instead of normal unicode string
print(characters) 
print(characters.decode("latin-1"))

# converting text to bytes 
print("\n")
characters = "cliché" 
print(characters.encode("UTF-8"))
print(characters.encode("latin-1"))
print(characters.encode("CP437")) 
print(characters.encode("ascii", errors="replace"))