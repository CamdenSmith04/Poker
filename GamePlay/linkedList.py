from player import Player

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:

    def __init__(self):
        self.head = None

    # Get data at a certain index
    def getNode(self, index):
        curr = self.head
        for i in range(index):
            curr = curr.next
            if curr == self.head:
                return None
        return curr

    # Insert node after node
    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    # Insert node before node
    def insert_before(self, ref_node, new_node):
        self.insert_after(ref_node.prev, new_node)

    # Insert player data at end
    def insertAtEnd(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.head.prev, new_node)

    # Insert at beginning
    def insertAtBeginning(self, new_node):
        self.insertAtEnd(new_node)
        self.head = new_node


    # Remove node
    def remove(self, node):
        if self.head.next == self.head:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.head == node:
                self.head = node.next

    def removePost(self, node):
        if self.head.next == self.head:
            self.head = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.head == node:
                self.head = node.prev


    def printLL(self):
        if self.head is None:
            return
        curr = self.head
        while True:
            print(curr.data.initialize())
            curr= curr.next
            if curr == self.head:
                break
    