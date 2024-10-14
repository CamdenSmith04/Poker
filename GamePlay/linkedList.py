from player import Player

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None

    # Insert player data at end
    def insertAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while (current_node.next):
            current_node = current_node.next
    
        current_node.next = new_node


    # Necessary for following command
    def remove_first_node(self):
        if(self.head == None):
            return

        self.head = self.head.next

    # Used to remove a player if they fold
    def remove_node(self, data):
        current_node = self.head

        if current_node.data == data:
            self.remove_first_node()
            return

        while(current_node != None and current_node.next.data != data):
            current_node = current_node.next

        if current_node == None:
            return
        else:
            current_node.next = current_node.next.next

    def printLL(self):
        curr = self.head
        while (curr):
            print(curr.data.initialize())
            curr = curr.next