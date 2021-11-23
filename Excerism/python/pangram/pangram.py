import string


def is_pangram(sentence):
    chars = [i.lower() for i in sentence if i.isalpha()]
    _ascii_chars = string.ascii_lowercase

    return all(char in chars for char in _ascii_chars)
