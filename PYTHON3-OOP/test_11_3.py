"""
The composite pattern:
The composite pattern allows complex tree-like structure to be buid from simple components. These components, called 
composite objects are able to behave sort of like a container and sort of like a variable, depending on whether they 
have child components. Composite objects are container objects, where the content may actually be another composite 
to another composite object. 

Traditional, each component in a compsite object must be either a leaf node (that cannot contain other objects) or 
a composite node(can contain children). The key is that both composite and leaf nodes can have the same interface. 

This simple pattern, allows us to create complex arrangements of elements, all of which satisfy the interface of the 
component object. 
Composite pattern is commonly useful in file/folder-like trees. Regardless of whether a node in the tree is a normal 
file or a folder, it is still subject to operation such as moving, copying or deleting a the node. 
We can create a component interface that support these operations and then use a composite object to represent folders,
and leaf nodes to represent normal files. 
"""

class Folder:
    def __init__(self, name):
        self.name = name 
        self.children = {} 
    
    def add_child(self, child):
        pass
    
    def move(self, new_path):
        pass 

    def copy(self, new_path):
        pass 

    def delete(self):
        pass


class File:
    def __init__(self, name, contents):
        self.name = name 
        self.contents = contents 
        
    def move(self, new_path):
        pass 

    def copy(self, new_path):
        pass

    def delete(self):
        pass

"""
For each folder(composite) object, we maintain a dictionary of children. For many composite implementations, a ilst 
is sufficient but in this case a dictionary will be useful for looking up children by name. Our paths will be specified 
as node names seperated by the / character, similar to paths in the Unix shell. 

Thinking about the methods involved, we can see that moving or deleting a node behaves in a similar way, regardless of 
whether or not it is a file or folder node. Copying, however, has to do a recursive copy for folder nodes, while 
copying a file node is a trivial operation. To take advantage of the similar operations, we can extract some of the 
common methods into a parent class.
"""

class Component:
    def __init__(self, name):
        self.name = name 

    def move(self, new_path):
        new_folder = get_path(new_path)
        del self.parent.children[self.name] 
        new_folder.children[self.name] = self 
        self.parent = new_folder

    def delete(self):
        del self.parent.children[self.name] 


class Folder(Component):
    def __init__(self, name):
        super().__init__(name) 
        self.children = {}

    def add_child(self, child):
        child.parent = self 
        self.children[child.name] = child 

    def copy(self, new_path):
        new_folder = get_path(new_path)
        new_folder.children[self.name] = self 
        self.parent = new_folder
        # use recusive method to move file in folder. 
        #while self.parent.children:
        #    self.parent.children.copy(new_path)
        


class File(Component):
    def __init__(self, name, contents):
        super().__init__(name)
        self.contents = contents 
    
    def copy(self, new_path):
        new_folder = get_path(new_path) 
        new_folder.children[self.name] = self 
        self.parent = new_folder

root = Folder("") 

def get_path(path):
    names = path.split("/")[1:]
    node = root  
    for name in names: 
        node = node.children[name] 
    return node 

"""
Run: 
folder1 = Folder("folder1")
folder2 = Folder("folder2")
root.add_child(folder1) 
root.add_child(folder2) 
folder11 = Folder("folder11") 
folder1.add_child(folder11) 
file111 = File("file111","contents") 
folder11.add_child(file111) 
file21 = File("file21","other contents") 
folder2.add_child(file21) 
folder2.children
folder2.move('/folder1/folder11')
folder11.children
file21.move('/folder1')
folder1.children

"""