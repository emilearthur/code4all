class Silly:
	def _get_silly(self):
		print("You ar egetting silly")
		return self._get_silly

	def _set_silly(self, value):
		print("You are making  silly {}".format(value))
		self._silly = value 

	def _del_silly(self):
		print("Whoah, you killed silly!") 
		del self._silly

	silly = property(_get_silly,_set_silly,_del_silly,"This is a silly property")

# Decorator - another way to create properties 
# property function can be used with the decorator syntax to turn a get 
# function inot a property function. 

# func. 1
class Foo:
	@property 
	def foo(self):
		return "bar"

# setting a setter function for a the new porperty 
class Foo:
	@property 
	def foo(self):
		return self._foo

	@foo.setter
	def foo(self, value):
		self._foo = value



# rewritting the silly class
class Silly():
	@property
	def silly(self):
		"This is a silly property"
		print("You are getting silly")
		return self._silly

	@silly.setter 
	def silly(self, value):
		print("You are making silly {}".format(value))
		self._silly = value

	@silly.deleter
	def silly(self):
		print("Whoah, you killed silly!")
		del self._silly
#this code above is the same as first silly class. however
# this is kinda elegant and and good syntax pratice. 