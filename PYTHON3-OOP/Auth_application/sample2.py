 import random

def words(WORDS = ("priscilla","frederick")):
	
	word = random.choice(WORDS)
	correct = word
	jumble = ""
	while word:
	    position = random.randrange(len(word))
	    jumble += word[position]
	    word = word[:position] + word[(position + 1):]
	print(
	"""
	      Welcome to WORD JUMBLE!!!

	      Unscramble the leters to make a word.
	      (press the enter key at prompt to quit)
	      """
	      )
	print("The jumble is:", jumble)