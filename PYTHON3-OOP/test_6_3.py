# do not use list for collecting different attributes of individual items. 
# collections of different attributes can be done with dictionary, tuples, named tuples or 
# objects suited for that purpose 

# counting frequency using a list. NB: Refer to notes above 
import string 

CHARACTERS = list(string.ascii_letters) + [" "]

def letter_frequency(sentence):
    frequencies = [(c,0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter) 
        frequencies[index] = (letter, frequencies[index][1]+1)
    return frequencies



# sorting lists 
# creating a class that does sorting based on a string or a number.  Its uses the 
# __lt__ method which stands for less than and its should be defined on the class to 
# to make instances of that class comparable. 

class WeirdSortee:
    def __init__(self, string, number, sort_num):
        self.string = string 
        self.number = number 
        self.sort_num = sort_num  

    def __lt__(self, object): # compare object to another instance of the same class
        if self.sort_num:
            return self.number < object.number
        return self.string < object.string 
    
    def __repr__(self): # repr method makes it easy to see two values when you print a list. 
        return f"{self.string}:{self.number}"


# to be free of __lt__, __gt__, __eq__, __ne__, __ge__ and __le__ to work properly 
# without explicit code, we can get these free using @total_ordering class decorator 

from functools import total_ordering 

@total_ordering
class WeirdSortee:
    def __init__(self, string, number, sort_num):
        self.string = string 
        self.number = number 
        self.sort_num = sort_num 
    
    def __lt__(self, object):
        if self.sort_num:
            return self.number < object.number 
        return self.string < object.string 

    def __repr__(self):
        return f"{self.string}:{self.number}"
    
    def __eq__(self,object):
        return all((
            self.string == object.string, 
            self.number == object.number,
            self.sort_num == object.number
        ))


# SETS 
# sets holds any hashable object not just numbers.  Sets only stores one copy of each
# object. 

song_libarary = [("Phantom of the Opera", "Sarah Brightman"),
                ("Knocking on Heaven's Door","Guns N' Roses"),
                ("Captain Nemo", "Sarah Brightman"),
                ("Patterns in the Ivy", "Opeth"),
                ("November Rain","Guns N' Roses"),
                ("Beautiful", "Sarah Brightman"),
                ("Mal's Song", "Vixy and Tony"),]

artists = set() 
for song, artist in song_libarary:
    artists.add(artist)

print(artists)


print("\n")
first_artists = {"Sarah Brightman","Guns N' Roses", "Opeth","Vixy and Tony"}
second_artists = {"Nickelback","Guns N' Roses","Savage Garden"}

print(f"All: {first_artists.union(second_artists)}")
print(f"Both: {second_artists.intersection(first_artists)}")
print(f"Either but not both: {first_artists.symmetric_difference(second_artists)}")

print("\n") 
first_artists = {"Sarah Brightman", "Gun N' Roses", "Opeth","Vixy and Tony"}
bands = {"Gun N' Roses", "Opeth"}

print("First_artist is to bands:")
print(f"issupeerset: {first_artists.issuperset(bands)}")
print(f"issubset: {first_artists.issubset(bands)}")
print(f"difference: {first_artists.difference(bands)}")
print("*"*20) 
print("bands is to first_artist:") 
print(f"issuperset: {bands.issuperset(first_artists)}")
print(f"issubset: {bands.issubset(first_artists)}")
print(f"difference: {bands.difference(first_artists)}")