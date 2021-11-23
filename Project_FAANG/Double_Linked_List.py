# Done of a Doubly linked list 
class Node:
    def __init__(self, next=None, prev=None, data=None):
        self.next = next 
        self.prev = prev  
        self.data = data


class DoublyLinkedList:
    def __init__(self):
        self.head = None
    # Adding a node at the front of the list 
    def push(self, new_data):
        # define new node
        new_node = Node(data = new_data) 
        # define head and previous of new node. ie. make the new nonde as head and previous as NULL 
        new_node.next = self.head 
        new_node.prev = None 

        # change the previous head node to new node 
        if self.head is not None:
            self.head.prev = new_node
        
        # move the head to point to the new node 
        self.head = new_node


    # adding a node after given node 
    def insertAfter(self, prev_node, new_data):
        # check if given node is NULL 
        if prev_node is None:
            print(f"This {prev_node} does not exist")
            return 
        
        # putting data into new node 
        new_node = Node(data = new_data)

        # make the next of new node as next of previous node 
        new_node.next = prev_node.next 

        # make the next of the prev_node as the new_node 
        prev_node.next = new_node

        # make prev_node as previous of new node 
        new_node.prev = prev_node 

        # change previous of new_nodes's to next node 
        if new_node.next is not None:
            new_node.next.prev = new_node


    # adding to the tail of a doubly linkedlist 

    def append(self, new_data):
        # define new node 
        new_node = Node(data=new_data) 
        last = self.head

        # this new node is the last node thus the next is NULL 
        new_node.next = None 

        # if the linked list is empty, then make the new node as head 
        if self.head  is None:
            new_node.prev = None 
            self.head = new_node 
            return
        
        # transverse till the last node 
        while (last.next is not None):
            last = last.next 
        
        # change the next of last node  and make last node as previous of new node 
        last.next = new_node 
        new_node.prev = last


    def printList(self, node):
        last = None
        print("Traversal in forward direction ")
        while (node != None):
            print(node.data, end = " ")
            last = node
            node = node.next
    
        print("\nTraversal in reverse direction ")
        while (last != None):
            print(last.data,end = " ")
            last = last.prev


if __name__ == '__main__':
   
    # /* Start with the empty list */
    llist = DoublyLinkedList()
    llist.append(6)
    llist.push(7)
    llist.push(1)
    llist.append(4)
    llist.insertAfter(llist.head.next, 8)

    llist.printList(llist.head)
