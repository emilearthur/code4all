"""
Regular Express:

Regular expressions are used to solve a common problem: Given a string, determine
whether that string matches a given pattern and, optionally, collect substrings that contain
relevant information. They can be used to answer questions such as the following:
    Is this string a valid URL?
    What is the date and time of all warning messages in a log file?
    Which users in /etc/passwd are in a given group?
    What username and document were requested by the URL a visitor typed?

"""

"""
Matching Pattern:
Regular expressions are a complicated mini-language. They rely on special characters to
match unknown strings, but let's start with literal characters, such as letters, numbers, and
the space character, which always match themselves

"""
from os import pardir
import re
from re import template
from typing import Pattern 

search_string = "hello world"
pattern = "hello world"

match = re.match(pattern, search_string) 

if match:
    print("regex matches")


# Example two 

