import sys 
import re 

pattern = sys.argv[1] 
search_string = sys.argv[2] 
match = re.match(pattern, search_string)

if match:
    template = "'{}' matches  pattern '{}'" 
else:
    template = "'{}' does not match pattern '{}'"

print(template.format(search_string, pattern)) 


# run code 
# python regex_generic.py "hello worl" "hello world"

"""
If you need control over whether items happen at the beginning or end of a line (or if there
are no newlines in the string, or at the beginning and end of the string), you can use the ^
and $ characters to represent the start and end of the string respectively. If you want a
pattern to match an entire string, it's a good idea to include both of these:

run:
python regex_generic.py "^hello world$" "hello world"
python regex_generic.py "^hello world$" "hello worl"
"""

"""
Matching a selection of characters 
, if
we encounter the string [abc] in a regular expression pattern, we know that those five
(including the two square brackets) characters will only match one character in the string
being searched, and further, that this one character will be either an a, a b, or a c. Let's see a
few examples:

eg. 

python regex_generic.py "hello [a-z] world" "hello b world"
python regex_generic.py "hello [a-zA-Z] world" "hello B world"
python regex_generic.py "hello [a-zA-Z0-9] world" "hello 2 world"

"""

"""
Escaping characters:
One way might be to put the period inside square brackets to make
a character class, but a more generic method is to use backslashes to escape it. Here's a
regular expression to match two-digit decimal numbers between 0.00 and 0.99.

For this pattern, the two characters \. match the single . character. If the period character
is missing or is a different character, it will not match.

This backslash escape sequence is used for a variety of special characters in regular
expressions. You can use \[ to insert a square bracket without starting a character class,
and \( to insert a parenthesis, which we'll later see is also a special character.

More interestingly, we can also use the escape symbol followed by a character to represent
special characters such as newlines (\n) and tabs (\t). Further, some character classes can
be represented more succinctly using escape strings: \s represents whitespace
characters; \w represents letters, numbers, and underscore; and \d represents a digit:



python regex_generic.py "0\,[0-9][0-9]" "0,05"
python regex_generic.py "0\.[0-9][0-9]" "0.05"

python regex_generic.py "\s\d\w" " 5n"
python regex_generic.py "\(abc\]" "(abc]"
"""

"""
Matching multiple characters:
With this information, we can match most strings of a known length, but most of the time,
we don't know how many characters to match inside a pattern. Regular expressions can
take care of this, too. We can modify a pattern by appending one of several hard-to-
remember punctuation symbols to match multiple characters.
The asterisk (*) character says that the previous pattern can be matched zero or more times(ie. multples times 
or optional).
This probably sounds silly, but it's one of the most useful repetition characters. Before we
explore why, consider some silly examples to make sure we understand what it does

run:
python regex_generic.py "hel*o" "hello"
python regex_generic.py "hel*o" "heo" 
python regex_generic.py "hel*o" "hellllllllo"

run:
python regex_generic.py "[A-Z][a-z]* [a-z]*\." "A string."


The plus (+) sign in a pattern behaves similarly to an asterisk; it states that the previous
pattern can be repeated one or more times, but, unlike the asterisk, is not optional. 
The question mark (?) ensures a pattern shows up exactly zero or one times, but not more. Let's
explore some of these by playing with numbers (remember that \d matches the same
character class as [0-9]
run:
python regex_generic.py "\d+\.\d+" "0.4"   
python regex_generic.py "\d+\.\d+" "0.4" 

python regex_generic.py "\d?\d%" "1%"  
python regex_generic.py "\d?\d%" "99%"
"""

"""
Grouping patterns together: 
 If we want to repeat individual characters, we're covered, but what
if we want a repeating sequence of characters? Enclosing any set of patterns in parentheses
allows them to be treated as a single pattern when applying repetition operations. Compare
these patterns:

run:
python regex_generic.py "abc{3}" "abccc"
python regex_generic.py "(abc){3}" "abcabcabc"

Combined with complex patterns, this grouping feature greatly expands our pattern-
matching repertoire. Here's a regular expression that matches simple English sentences:
run:
python regex_generic.py "[A-Z][a-z]*( [a-z]+)*\.$" "Eat."

"""