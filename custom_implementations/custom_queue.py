from custom_implementations.binary_heap import BinaryHeap

class EmptyQueueError(Exception):
    pass
      
class PriorityQueue:
    def __init__(self):
        self.data = BinaryHeap()

    def enqueue(self, element):
        self.data.insert(element)
        
    def dequeue(self):
        if self.data.is_empty():
            raise EmptyQueueError("cannot dequeue from an empty queue!")
        return self.data.extract_min()

    def peek(self):
        return self.data.get_minimum()

    def is_empty(self):
        return self.data.is_empty()
    
    def size(self):
        return self.data.size()

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def print_queue(self):
        current = self.head
        temp = []
        while current is not None:
            temp.append(current.value)
            current = current.next
        temp.reverse()
        print(temp)

    def enqueue(self, element):
        new_node = Node(element)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueError("cannot dequeue from an empty queue!")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise EmptyQueueError("cannot peek from an empty queue!")
        return self.head.value

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size