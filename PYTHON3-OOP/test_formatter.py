def format_string(string, formatter=None):
	"""Format a string using the formatter object , 
	which is expected to have a format() method that 
	accepts a string"""

	class DefaultFormatter:
		"""Format a string in title case."""
		
		def format(self, string):
			return str(string).title() 

	if not formatter:
		formatter = DefaultFormatter()


	return formatter.format(string)
			

## Accessing data 
class SecretString:
	"""A not-at-all secure way to store a secret string."""

	def __init__(self, plain_string, pass_phrase):
		self.__plain_string = plain_string
		self.__pass_phrase = pass_phrase

	def decrypt(self, pass_phrase):
		"""Only show the string if the pass_phrase is correct."""
		if pass_phrase == self.__pass_phrase:
			return self.__plain_string
		else: 
			return " "

