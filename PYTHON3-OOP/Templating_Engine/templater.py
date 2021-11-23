"""
We builidng a basic regular expression-powered templating engine in Python. 
THis engine will parse a text file (such as an HTML page) and replace cetain directives with text 
calculated from the input of those directives. 

"""

# boilerplate code for processing files and grabbing data from the cmd. 

import re
from re import L 
import sys 
import json 
from pathlib import Path
from sys import gettrace

DIRECTIVE_RE = re.compile(
    r'/\*\*\s*(include|variable|loopover|endloop|loopvar)' # r stand for raw string. 
    r'\s*([^ *]*)\s*\*\*/')

class TemplateEngine:
    def __init__(self, infilename, outfilename, contextfilename):
        self.template = open(infilename).read() 
        self.working_dir = Path(infilename).absolute().parent
        self.pos = 0 #indicate the current character in the content that we are processing 
        self.outfile = open(outfilename,"w") 
        with open(contextfilename) as contextfile:
            self.context = json.load(contextfile)

    def process(self):
        """
        This method find each directive that matches a regular expression and do the appropriate 
        work with it. Its also takes care of outputting the normal text before, after, and between 
        each directive to the output file, unmodified. 

        In simple terms; This function finds the first string in the text that matches the regular 
        expression, outputs everything from the current position to the start of that match, and then 
        advances the position to the end of the aforesaid match. Once it's of matches, it outputs 
        everything since the last position. 

        NB: One good feature of the compiled version of regular expression is that we can tell 
        the search method to start searching at a specific position by passing the pos keyword args. 
        If we temp define doing the appropriate work with a directive as ignore the directive and 
        delete it from the output file. 

        So, we grab the directive and the single argument from the regular expression. The
        directive becomes a method name and we dynamically look up that method name on the
        self object (a little error processing here, in case the template writer provides an invalid
        directive, would be better). We pass the match object and argument into that method and
        assume that method will deal with everything appropriately, including moving the pos
        pointer.

        """
        print("PROCESSING....")
        match = DIRECTIVE_RE.search(self.template, pos=self.pos) 
        while match:
            self.outfile.write(self.template[self.pos:match.start()])
            directive, argument = match.groups()
            method_name = "process_{}".format(directive)
            getattr(self, method_name)(match, argument)
            match = DIRECTIVE_RE.search(self.template, pos=self.pos) 
        self.outfile.write(self.template[self.pos:]) 

    
    def process_include(self, match, argument):
        """
        This function looks up the included file and insert the file contents. 
        """
        with (self.working_dir / argument).open() as includefile:
            self.outfile.write(includefile.read()) 
            self.pos = match.end() 

    def process_variable(self, match, argument):
        """
        This function looks up the variable name in the context dict.(which is loaded in json 
        in the __init__ method), defaulting to an empty string if it does not exit)
        """
        self.outfile.write(self.context.get(argument, "")) 
        self.pos = match.end()


    def process_loopover(self, match, argument):
        """
        This function set the initial state to three variables. 
        loop_list variable assuming to be list pulled from the context dictionary 
        loop_index variable indicates which position of that list should be output in the interation
        of the loop. 
        loop_pos to get the end of the loop 
        """
        self.loop_index = 0  
        self.loop_list = self.context.get(argument, []) 
        self.pos = self.loop_pos = match.end() 

    
    def process_loopvar(self, match, argument):
        """
        THis function outputs the value at the current position in the loop_list varaible and 
        skips to the end of the directive. 
        NB: It doesn't increment the loop index, because it could be called multiple times inside 
        a loop. 
        """
        self.outfile.write(self.loop_list[self.loop_index])
        self.pos = match.end() 

    
    def process_endloop(self, match, argument):
        """
        This function determines whether there are more elements in the loop loop_list. If there is, 
        it jumps back to the start of the loop, incrementing the index. Otherwise it resets all the 
        directive so the engine can carry on with the next match. 
        """
        self.loop_index += 1 
        if self.loop_index >= len(self.loop_list):
            self.pos = match.end() 
            del self.loop_index
            del self.loop_list 
            del self.loop_pos
        else:
            self.pos = self.loop_pos

if __name__ == "__main__":
    infilename, outfilename, contextfilename = sys.argv[1:]
    engine = TemplateEngine(infilename, outfilename, contextfilename) 
    engine.process() 

    