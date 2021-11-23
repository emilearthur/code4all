"""
Strategy in Python:
These classes each represent object that do nothing but provide a single function. We could just as easy call that 
function __call__ and make the object callable directly. Since there is no other data assocaited with the object, 
we need do no more than create a set of top-level functions and pass them around as our strategies instead. 

The state pattern:
The  state pattern is structurally similar to the strategy pattern, but its intent and purpose are very different. 
The goal of the state pattern is to represent state-transition systems: systems where it is obvious that an object 
can be in a specific state and that certain activites may drive it to a different state.  
To make this work, we need a manager or context class that provides an interface for switching states. Interally, 
this class contains a pointer to the current state. Each state know what other states it is allowed to be in and 
will transition to those state depending on the actions invocked upon it. 
So we have two types of classes: the context class and multiple state classes. The context class maintains the
current state, and forwards action to the state classes. The state classes are typically hidden from any other
objects that are calling the context; it acts like a black box that happens to perform state management internally.
Eg:
We build an XML pasrsing tool. The context class will be the parser itself. It will take a string as input and 
place the tool in an initial parsing state. The various parsing state will eat characters, looking for a specific 
value and when that value is found, changes to a different state. 
The goal is to create a tree of node objects for each tag its contents. To keep things manageable, we'll parse only 
subset of XML - tags and tag names. We won't be able to handle attributes on tags. It will parse text contents of 
tags, but won't attempt to parse mixed content, which has tags inside of text. 
Output of program:  We want a tree of Node object. It will clearly need to know the name of the tag it is parsing 
and since it's a tree, it should probably maintain a pointer to the parent node and a ist of node's children in order. 
Some node have a text value but not all of them. 

"""
class Node:
    def __init__(self, tag_name, parent=None):
        self.parent = parent 
        self.tag_name = tag_name 
        self.children = [] 
        self.text = ""
    
    def __str__(self):
        """
        This method helps visualize the tree structure
        """
        if self.text:
            return self.tag_name + ": " + self.text 
        else:
            return self.tag_name 

class Parser:
    def __init__(self, parser_string):
        self.parser_string = parser_string 
        self.root = None 
        self.current_node = None 
        self.state = FistTag() 
    
    def process(self, remaining_string):
        """Accepts remaining string and pases it off to the current state. The parse(the self arg) is also passed into 
        the state's process method so that the state can manipulate it. The state is expected to return the remainder 
        of the unparsed string when its is finished processing. The parser then recursively calls the process method on 
        the remaining string to contruct the rest of the treee

        Args:
            remaining_string ([type]): [description]
        """
        remaining = self.state.process(remaining_string, self) 
        if remaining:
            self.process(remaining) 
    
    def start(self):
        self.process(self.parser_string)


class FistTag:
    def process(self, remaining_string, parser):
        """
        This method extracts the name of the tag and assigns it to the root node of the parser. It also assigns it to 
        currnet_node, since that's the one we'll be adding to the children next. 
        After the method changes the current state on the parser object to a ChildNode state.
        After it returns the remainder of the string(after opening tag) to allow it to be processed.
        """
        ndx_start_tag =  remaining_string.find("<")
        ndx_end_tag = remaining_string.find(">") 
        tag_name = remaining_string[ndx_start_tag + 1 :  ndx_end_tag]
        root = Node(tag_name) 
        parser.root = parser.current_node = root 
        parser.state = ChildNode() 
        return remaining_string[ndx_end_tag + 1 :]


class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()  # removes whitespaces from string. 
        if stripped.startswith("</"):
            parser.state = ClosingTag() 
        elif stripped.startswith("<"):
            parser.state = OpenTag() 
        else:
            parser.state = TextNode() 
        return stripped 


class OpenTag:
    """
    Similar to FirstTag state expect it adds the newly create node to the previous current_node object's children and 
    set a new current_node. It places the processor back in the ChildNode state befor returning the reminder of the tag.
    """
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<")
        ndx_end_tag = remaining_string.find(">") 
        tag_name = remaining_string[ndx_start_tag+1 : ndx_end_tag] 
        node = Node(tag_name, parser.current_node)
        parser.current_node.children.append(node)
        parser.current_node = node 
        parser.state = ChildNode() 
        return remaining_string[ndx_end_tag + 1 :]


class ClosingTag:
    """
    Its set the parser's current node back to the parent node so any further children in the outside tag can be added
    to it. 
    """
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<") 
        ndx_end_tag = remaining_string.find(">") 
        assert remaining_string[ndx_start_tag + 1] == "/" 
        tag_name = remaining_string[ndx_start_tag + 2 : ndx_end_tag] 
        assert tag_name == parser.current_node.tag_name 
        parser.current_node = parser.current_node.parent
        parser.state = ChildNode() 
        return remaining_string[ndx_end_tag + 1 :].strip() 


class TextNode:
    """
    Extracts the texx before the next close tag and sets it as value on currnet node 
    """
    def process(self, remaining_string, parser):
        ndx_start_tag = remaining_string.find("<") 
        text = remaining_string[:ndx_start_tag] 
        parser.current_node.text = text 
        parser.state = ChildNode() 
        return remaining_string[ndx_start_tag:]


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
            