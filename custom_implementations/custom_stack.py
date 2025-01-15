############################
# GROUP A Skill : Stack    #
############################

class EmptyStackError(Exception):
    pass

class Stack:
    def __init__(self):
        self.data = []
        self.head = 0
        
    def push(self, element):
        self.data.append(element)
        self.head += 1
    
    def pop(self):
        if self.is_empty():
            raise EmptyStackError("cannot pop from an empty stack!")
        
        self.head -= 1
        return self.data.pop(self.head)
    
    def peek(self):
        if self.is_empty():
            raise EmptyStackError("cannot peek from an empty stack!")
        return self.data[-1]
    
    def is_empty(self):
        return len(self.data) == 0
    
    def size(self):
        return self.head
    