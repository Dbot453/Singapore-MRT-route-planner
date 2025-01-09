from custom_implementations.binary_heap import BinaryHeap
from custom_implementations.linked_list import CustomList

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

class Queue:
    def __init__(self):
        self._list = CustomList()

    def enqueue(self, element):
        self._list.append(element)

    def dequeue(self):
        if self._list.is_empty():
            raise EmptyQueueError("cannot dequeue from an empty queue!")
        return self._list.pop(0)

    def peek(self):
        if self._list.is_empty():
            return None
        return self._list.get(0)

    def is_empty(self):
        return self._list.is_empty()

    def size(self):
        return self._list.size()
    
    def sort(self):
        self._list = self._list.sort()