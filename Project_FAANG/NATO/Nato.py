"""
Conversion functions for the NATO Phonetic Alphabet.
"""
import re 

# To save a lot of typing the code words are presented here
# as a dict, but feel free to change this if you'd like.
ALPHANUM_TO_NATO = {
    "A": "ALFA",
    "B": "BRAVO",
    "C": "CHARLIE",
    "D": "DELTA",
    "E": "ECHO",
    "F": "FOXTROT",
    "G": "GOLF",
    "H": "HOTEL",
    "I": "INDIA",
    "J": "JULIETT",
    "K": "KILO",
    "L": "LIMA",
    "M": "MIKE",
    "N": "NOVEMBER",
    "O": "OSCAR",
    "P": "PAPA",
    "Q": "QUEBEC",
    "R": "ROMEO",
    "S": "SIERRA",
    "T": "TANGO",
    "U": "UNIFORM",
    "V": "VICTOR",
    "W": "WHISKEY",
    "X": "XRAY",
    "Y": "YANKEE",
    "Z": "ZULU",
    "0": "ZERO",
    "1": "ONE",
    "2": "TWO",
    "3": "TREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINER",
}


def transmit(message: str) -> str:
    """
    Convert a message to a NATO code word transmission.
    """
    NATO_message = []
    message = re.findall(r'[\S+]', message)
    
    for char in message:
    	NATO_message.append(ALPHANUM_TO_NATO.get(char.upper()))
    
    NATO_message = [i for i in NATO_message if i]

    return str(" ".join(NATO_message))


def receive(transmission: str) -> str:
    """
    Convert a NATO code word transmission to a message.
    """
    transmission = re.findall(r'\S+', transmission)

    UNNATO_message =  []

    for word in transmission:
        for key, value in ALPHANUM_TO_NATO.items():
            if word == value:
                UNNATO_message.append(key)

    UNNATO_message = [i for i in UNNATO_message if i]

    return str("".join(UNNATO_message))


