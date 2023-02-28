class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        return self.items.pop()
    
    def __str__(self):
        return "".join(str(x) for x in self.items)
    
    def peek(self):
        return self.items[-1]
    
    def is_empty(self):
        return not self.items

class ChrQueue:
    def __init__(self, string):
        self.items = [char for char in string]
    
    def dequeue(self):
        return self.items.pop(0)
    
    def __str__(self):
        return "".join(self.items)
    
    def is_empty(self):
        return not self.items
    
    def peek(self):
        return self.items[0]
    
    def items_left(self):
        return len(self.items)
    
class TypedQueue:
    def __init__(self):
        self.items = []
    
    def dequeue(self):
        return self.items.pop(0)
    
    def enqueue(self, item):
        self.items.append(item)
    
    def is_empty(self):
        return self.items == []
    
    def peek(self):
        return self.items[0]

    def __str__(self):
        return "".join(str(x) for x in self.items)        