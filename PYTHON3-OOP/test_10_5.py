"""
State versus strategy:
The state pattern looks similar to the strategy pattern. 
Whiles the two patterns have identical structures, they solve completely different problems. 
The strategy pattern is used to choose an algorithm at runtime(since one algorithm will be chose for a particular case), 
the state pattern on the other hand is designed to allow switching between different strategy state dynamically as some 
process evolves. 
In code, the primary difference is that the strategy pattern is not typically aware of other strategy objects whiles in
the state pattern, either the state or the context needs to know which other states that it can switch to. 

State transition as coroutines:
The state pattern is the canonical OO solution to state-transition problems. However, you can get similar effect by 
constructing your objects as coroutines. 
The main difference between that implementation and on that defines all the objects (or functions) used in the state 
pattern that the coroutine solution allows us to encode more of the boilerplate in language constructs.
The state pattern is actually the only place I would consider using coroutines outside of asyncio. 

The Singleton pattern:
The basic idea behind the singleton pattern is to allow exactly one instance of a certain object to exit. Typically the 
object is a sort of manager class. Such objects needs often to be reference by a wide variety of other objects and passing 
references to the manager object around to the methods and constructors that need them can make code hard to read. 
Instead, when a singleton is used, the seperate objects request the single instance of the manager object from the class,
so a reference to it need not to be passed around. 
In most programming env., singletons are enforced by making the constructor private (so no one can create additional
instances of it), and providing a state method to retrieve the single instance. This method creates a new instance the
first time it is called, and then returns that same instance for all subsequent calls. 

Implementation below:
"""
# python does not have a private constructor but for this purpose, we can use the __new__ class method to ensure that 
# only one instance is ever create 




class OneOnly:
    _singleton = None 
    def __new__(cls, *args, **kwargs):
        """
        When __new__ is called, it normally constructs a new instance of that class. 
        When we override it, we fist check whether our singleton instance has been created; if not, we create it using
        a super call. Thus, whenever we call the constructor on OneOnly, we always get the exact same instance. 
        """
        if not cls._singleton:
            cls._singleton = super(OneOnly, cls).__new__(cls, *args, **kwargs) 
        return cls._singleton

"""run: o1 = OneOnly()
        o2 = OneOnly()
        o1 == o2 
        o1
        o2 
Notes: From the output above, you could see the object are equal and located at the same address; thus they are the same 
object. This particular implementation isn't very transparent, since its not obvious that a singleton object has been 
created. Whenever we call a constructor, we expect a new instacnec of the object, in this case that contract is voilated 
However, good docstrings on the classs could alleviate the problem if we really think we need a singleton. 
"""

"""
Module variable can mimic singletons:
Singleton pattern can be sufficiently mimicked using module-level variables. It's not as safe as a singleton in that 
people could reassign those variable to any time, but as with the private variables. 
Ideal, people shouold be given the mechanism to get access to default singleton value, which allowing them to create 
other instances if they need them. While technically it  provide the most pythonic mechnism for singleton-like behaviour. 

To use module-level variables instead of a singleton, we instantiate an instance of the class after we've defined it. 
We can improve our state pattern to use singletons. Instead of creating a new objec every time we change states, we can 
create a module-level variable that is always accessible. 
Eg below
"""

# Singleton State 
class Node:
    def __init__(self, tag_name, parent=None):
        self.parent = parent 
        self.tag_name = tag_name 
        self.children = [] 
        self.text = ""
    
    def __str__(self):
        if self.text:
            return self.tag_name + ": " + self.text 
        else:
            return self.tag_name 


class FirstTag:
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<") 
        ndx_end_tag = remaining_string.find(">") 
        tag_name = remaining_string[ndx_start_tag + 1 : ndx_end_tag]
        root = Node(tag_name) 
        parser.root = parser.current_node = root 
        parser.state = child_node 
        return remaining_string[ndx_end_tag + 1 : ]


class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip() 
        if stripped.startswith("</"):
            parser.state = close_tag 
        elif stripped.startswith("<"):
            parser.state = open_tag
        else:
            parser.state = text_node
        return stripped 


class OpenTag:
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<") 
        ndx_end_tag = remaining_string.find(">") 
        tag_name = remaining_string[ndx_start_tag + 1 : ndx_end_tag]
        node = Node(tag_name, parser.current_node) 
        parser.current_node.children.append(node)
        parser.current_node = node 
        parser.state = child_node
        return remaining_string[ndx_end_tag + 1: ]


class TextNode:
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<")  
        text = remaining_string[:ndx_start_tag] 
        parser.current_node.text = text 
        parser.state = child_node 
        return remaining_string[ndx_start_tag: ] 


class CloseTag:
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<") 
        ndx_end_tag = remaining_string.find(">") 
        assert remaining_string[ndx_start_tag + 1] == "/"
        tag_name = remaining_string[ndx_start_tag + 2 : ndx_end_tag] 
        assert tag_name == parser.current_node.tag_name 
        parser.current_node = parser.current_node.parent
        parser.state = child_node 
        return remaining_string[ndx_end_tag + 1: ].strip() 

class Parser:
    def __init__(self, parser_string):
        self.parser_string = parser_string 
        self.root = None 
        self.current_node = None 
        self.state = first_tag
    
    def process(self, remaining_string):
        remaining = self.state.process(remaining_string, self)
        if remaining:
            self.process(remaining)

    def start(self):
        self.process(self.parser_string)


first_tag = FirstTag()
child_node = ChildNode() 
text_node = TextNode() 
open_tag = OpenTag() 
close_tag = CloseTag() 

if __name__ == "__main__":
    import sys 
    with open(sys.argv[1]) as file:
        contents = file.read()
        p = Parser(contents)
        p.start()

        nodes = [p.root] 
        while nodes:
            node = nodes.pop(0) 
            print(node) 
            nodes = node.children + nodes
"""
Notes: All we have doen above is create instances of various classses that can be reused. 
Code inside the classes is not executed until the method is called and by this point, the entire module will be 
defined. 
The difference in this eg. is instead of wasting memory creating bunch of new instances that must be garbage collected, 
we are resuing a sinlge state object for  each state. Even if multuple parsers are running at one, only these state 
classes need to be used. 

When we originally created the state-based parser, you may have wondered why we didn't
pass the parser object to __init__ on each individual state, instead of passing it into the
process method as we did. The state could then have been referenced as self.parser.
This is a perfectly valid implementation of the state pattern, but it would not have allowed
leveraging the singleton pattern. If the state objects maintain a reference to the parser, then
they cannot be used simultaneously to reference other parsers
"""






        