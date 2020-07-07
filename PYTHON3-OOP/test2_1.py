# The Contact class is responsible for
# maintaining a list of all contacts in a class variable, 
# and for initializing the name and address for an individual 
# contact

class Contact:
	all_contacts = []

	def __init__(self, name, email):
		self.name = name 
		self.email = email
		Contact.all_contacts.append(self)

class Supplier(Contact):
	def order(self, order):
		print(
			"If this were a real system we would send "
			f" '{order}' order to '{self.name}'"
			)