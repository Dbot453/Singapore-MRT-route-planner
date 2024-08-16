class EmptyQueueError(Exception):
    pass

class PriorityQueue:
    def __init__(self):
        self.__queue = []
        self.__head = 0
        self.__tail = 0
        
    def isempty(self):
        return self.__head == self.__tail
    
    def isfull(self):
        return False
    
    def enq(self, value):
        if self.isempty():
            self.__queue = [value]
            self.__tail += 1
            return
        for i in range(self.__head, self.__tail):
            #lower number is higher priority
            if value < self.__queue[i-1]:
                self.__queue = self.__queue[:i] + [value] + self.__queue[i:]
                self.__tail += 1
                return
 
    def dq(self):
        if not self.isempty():
            value = self.__queue[self.__head]
            self.__head += 1
            return value
        else:
            return EmptyQueueError("Queue is empty")
