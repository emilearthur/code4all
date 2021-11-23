"""
Strings and Serialization 
String represents an immutable sequence of characters. 
Character is a bit of an ambiguous word. 

Python strings are all represented in Unicode, a character
definition standard that can represent virtually any character in any language on the planet
(and some made-up languages and random characters as well).

Thus python strings are an immutable sequence of Unicode characters. 
"""

"""
String formating 

A string can be turned into a format string (ie. f-string) by prefixing the open quotation mark 
with an f as in f"Hello World"
"""
name = "Dusty"
activity = "writing"
formatted = f"Hello {name}, you are currently {activity}"
print(formatted)


"""
Escaping braces 
Brace characters are often useful in strings, aside from formatting.  

We need a way to escape
them in situations where we want them to be displayed as themselves, rather than being
replaced. This can be done by doubling the braces.{{}}

using python to format a basic java program
"""
classname = "MyClass"
python_code = "print('Hello World')"
template = f"""
public class {classname} {{
    public static void main(String[] args) {{
        System.out.println("{python_code}");
        }}
    }}"""
print(template)

print("\n")

"""
f-string can contain python code 

Complex objects including lists, tuples, dictionaries, and arbitrary objects can be used, and we can access
indexes and variables or call functions on those objects from within the format string.

"""
emails = ("a@example.com", "b@example.com")
message = {"subject":"You Have a Mail!", "message": "Here's some mail for you!",}

formatted = f"""
From: <{emails[0]}>
To: <{emails[1]}>
Subject: {message['subject']}
{message['message']} """
print(formatted)

print("\n")

message["emails"] = emails
formatted = f"""
From: <{message['emails'][0]}>
To: <{message['emails'][1]}>
Subject: {message['subject']}
{message['message']}"""
print(formatted)