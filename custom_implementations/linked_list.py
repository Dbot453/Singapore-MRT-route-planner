class EmptyListError(Exception):
    pass

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self._size = 0
        self.head = None
        self.tail = None

    def size(self): 
        return self._size
    
    def is_empty(self):
        return self._size == 0
    
    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value
    
    def dequeue(self):
        if self.is_empty():
            raise EmptyListError("cannot dequeue from an empty list!")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return value
    
    def pop(self):
        if self.is_empty():
            raise EmptyListError("cannot pop from an empty list!")
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        self._size -= 1
        return value
    
    def print_list(self):
        current = self.head
        temp = []
        while current is not None:
            temp.append(current.value)
            current = current.next
        print(temp)

    def insert(self,index,value):
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")
        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            current = self.head
            for _ in range(index-1):
                current = current.next
            new_node.next = current.next
            new_node.prev = current
            if current.next is not None:
                current.next.prev = new_node
            current.next = new_node
            if new_node.next is None:
                self.tail = new_node
        self._size += 1

    def merge_sort(self):
        if not self.head or not self.head.next:
            return
        self.head = self._merge_sort_list(self.head)
        curr = self.head
        while curr.next:
            curr = curr.next
        self.tail = curr

    def _merge_sort_list(self, head):
        if not head or not head.next:
            return head
        left, right = self._split_list(head)
        left = self._merge_sort_list(left)
        right = self._merge_sort_list(right)
        return self._merge_lists(left, right)

    def _split_list(self, head):
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        right = slow.next
        slow.next = None
        if right:
            right.prev = None
        return head, right

    def _merge_lists(self, left, right):
        if not left:
            return right
        if not right:
            return left
        if left.value <= right.value:
            left.next = self._merge_lists(left.next, right)
            if left.next:
                left.next.prev = left
            return left
        else:
            right.next = self._merge_lists(left, right.next)
            if right.next:
                right.next.prev = right
            return right