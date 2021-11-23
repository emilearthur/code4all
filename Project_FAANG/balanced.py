"""
source: Geek for Geek 
Question: Given an expression string exp, write a program to examine whether the pairs and the orders of “{“, “}”, “(“, “)”, “[“, “]” are correct in exp.
"""

"""
Solution:
Algorithm:
* Declare a character stack S
* Now trasverse the expression string exp. 
    * If the current character is a starting bracket ('(' or '{' or '[') then push it to the stack 
    * if the current character is a closing bracket (')' or '}' or ']') the pop from the stack and if the popped character is the matching starting bracket then fine 
      else bracket are not blanced 
    * After complete traversal, if there is some starting bracket left in stack then "not balanced"

"""

def areBracketsBalanced(expr):
    stack = [] 

    # transversing the expression 
    for char in expr:
        if char in ["(","{","["]:
            stack.append(char) 
        else:
            if not stack:
                return False 
            
            current_char = stack.pop()
            if current_char == "(":
                if char != ")":
                    return False 
                if current_char == "{":
                    if char != "}":
                        return False 
                if current_char == "[":
                    if char != "]":
                        return False 
    
    # checking for empty stack
    if stack:
        return False 
    return True 

# Driver Code 
if __name__ == "__main__":
    expr = "{()}[]" 
    
    # call function 
    if areBracketsBalanced(expr):
        print("Balanced") 
    else:
        print("Not Balanced")


"""
Notes: 
Functional complexities:
* Accessing : O(n) 
* Searching : O(n)
* Inserting : O(1) 
* Deleting : O(1)

* Time complexity: O(n) 
* Auxillary space: O(n)

"""