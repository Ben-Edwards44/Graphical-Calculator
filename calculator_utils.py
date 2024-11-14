class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[0]
    

class InfixExpression:
    def __init__(self, expression):
        self.expression = expression
        
    def covert_to_postfix(self):
        #use the Shunting Yard algorithm to convert self.expression to postfix
        return ""
    
    def evaluate(self):
        postfix = self.convert_to_postfix()