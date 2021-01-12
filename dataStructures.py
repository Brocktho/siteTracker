class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue():


    def __init__(self):
        self.len = 0
        self.front = None
        self.back = None
        self.values = []
    

    def enqueue(self, item):
        if isinstance(item, Node):
            if len(self) == 0:
                self.front = item
                self.back = item
                self.values.append(item.value)
            else:
                item.next = self.back
                self.back = item
                self.values.append(item.value)
            self.len += 1
        else:
            return "Not valid"


    def dequeue(self):
        if len(self) == 0:
            return "Queue is Empty"
        else:
            if len(self) == 1:
                out = self.values.pop()
                self.front = None
                self.back = None
                self.len = 0
                return out
            else:
                out = self.values.pop()
                self.back = self.back.next
                self.len -= 1
                return out


    def __len__(self):
        return self.len

    
    def __str__(self):
        if len(self) == 0:
            return "Queue is Empty"
        else:
            return 'Queue Object with front equal to: ' + str(self.front.value)
        
    
    def __repr__(self):
        return self.values