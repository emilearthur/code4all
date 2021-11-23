# Raising an exception 
class EvenOnly(list):
	def append(self, integer):
		if not isinstance(integer, int):
			raise TypeError("Only integers can be added")
		if integer%2:
			raise ValueError("Only even numbers can be added") 
		super().append(integer)


def no_return():
	print("I am about tho raise an exception") 
	raise Exception("This is always raised")
	print("This line will never execute")
	return "I won't be returned"

#def call_exceptor():
#	print("call_exceptor starts here...")
#	no_return()
#	print("an exception was raised...")
#	print("...so these lines don't run") 
	
def call_exceptor():
	try: 
		no_return()

	except:
		print("I caught an except")
	print("executed after the exception")

# catching a zero division error in a code 
def funny_division(divider):
	try:
		return 100 / divider

	except ZeroDivisionError:
		return "Zero is not a good idea!"
	except TypeError:
		return "Enter an integer"


# catches but typeerror and zeroerror 
def funny_division2(divider):
	try:
		if divider == 13:
			raise ValueError("13 is an unlucky number")
		return 100 / divider
	except (ZeroDivisionError, TypeError):
		return "Enter a number other than zero"


def funny_division3(divider):
	try:
		if divider == 13:
			raise ValueError("13 is an unlucky number")
		return 100/ divider
	except ZeroDivisionError:
		return "Enter a number other than zero"
	except TypeError:
		return "Enter a numerical value"
	except ValueError:
		print("No, No, not 13!")
		raise
		
def val_():
	for val in (0, "hello", 50.0, 13):
		print("Testing {}:".format(val), end=" ")
		print(funny_division3(val))


def python_finally_else():
	import random 
	some_exceptions = [ValueError, TypeError, IndexError, None]

	try:
		choice = random.choice(some_exceptions)
		print("raising {}".format(choice))
		if choice:
			raise choice("An error")
	except ValueError:
		print("Caught a ValueError")
	except TypeError:
		print("Caught a TypeError")
	except Exception as e:
		print("Caught some other error: %s" %(e.__class__.__name__))

	else:
		print("This code called if there is no except")
	finally:
		print("This cleanup code is always called")