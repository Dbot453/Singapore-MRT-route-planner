class EmptyStackError(Exception):
    pass

#custom_stack
class Stack:
    def __init__(self):
        self.data = []
        self.head = None
        
    def push(self, element):
        self.data.append(element)
        self.head = element
    
    def pop(self):
        if self.is_empty():
            raise EmptyStackError("cannot pop from an empty stack!")
        return self.data.pop()
    
    def peek(self):
        if self.is_empty():
            raise EmptyStackError("cannot peek from an empty stack!")
        return self.data[-1]
    
    def is_empty(self):
        return len(self.data) == 0
    
    def size(self):
        return len(self.data)
    