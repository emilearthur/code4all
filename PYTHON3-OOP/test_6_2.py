stocks = { "GOOG" : (1235.20, 1242.54, 1231.06),
            "MSFT" : (110.41, 110.45, 109.84)}

# counts the number of times a letter occurs in a given sentence\
# here we using the setdefault dict method 
def letter_frequency(sentence):
    frequencies = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0) 
        frequencies[letter] = frequency + 1
    return frequencies

# we using defaultdict to make the function above easier 

from collections import defaultdict
def letter_frequency(sentence):
    frequencies = defaultdict(int)
    for letter in sentence:
        frequencies[letter] += 1
    return frequencies

# The defaultdict accepts a function in its constructor. Whenever a key is accessed that is not already in the dictionary, it calls that
# function, with no parameters, to create a default value.



from collections import defaultdict

num_items = int(0)

def tuple_counter():
    global num_items 
    num_items += 1 
    return (num_items, []) 

d = defaultdict(tuple_counter)



# To make the function above more simpler, we use the Counter method to count specific instance in an iterable 
from collections import Counter 

def _letter_frequency(sentence):
    return Counter(sentence)
