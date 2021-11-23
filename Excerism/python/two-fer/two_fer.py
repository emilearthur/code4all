def two_fer(name="you"):
	return f"One for {name}, one for me."



def two_fer_one(name=None):
	if name:
		return f"One for {name}, one for me."
	else:
		return f"One for you, one for me."


def two_fer_two(name=''):
	if name:
		return f"One for {name}, one for me."
		
	else:
		return f"One for you, one for me."