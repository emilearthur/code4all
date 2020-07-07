# defining our own exceptions 
class InvalidWithdrawal(Exception):
	def __init__(self, balance, amount):
		super().__init__(f"account doesn't have ${amount}")
		self.amount = amount
		self.balance = balance

	def overage(self):
		return self.amount - self.balance

#raise InvalidWithdrawal("You don't have $50 in your account")

try:
	raise InvalidWithdrawal(25, 50)

except InvalidWithdrawal as e:
	print("I'm sorry, but your Withdrawal is "
			"more than your balance by "
			f"${e.overage}")


# inventory example raising errors 
class Inventory:
	def lock(self, item_type):
		"""Select the type of item that is going to be 
		manipulated. This method will lock the item so 
		nobody else can manipulate this inventory until 
		it's returned. This prevents selling the same 
		item to two different customers."""
		pass 

	def unlock(self, item_type):
		"""Release the given type so that others customers 
		can access it."""
		pass 

	def purchase(self, item_type):
		"""If the ite is not locked, raise an exception. If 
		the item_type does not exist, raise an exception. If 
		the tiem is currently out of stock, raise an exception.
		If the item is available, subtract one item and return 
		the number of items left."""
		pass

# implementation 
item_type = "widget"
inv = Inventory()
inv.lock(item_type)

try: 
	num_left =inv.purchase(item_type)

except InvalidItemType:
	print("Sorry, we don't sell {}".format(item_type))

except OutOfStock:
	print("Sorry, that item is out of stock.")

else:
	print("Purchase complete. There are {num_left} {item_type}s left")

finally:
	inv.unlock(item_type)