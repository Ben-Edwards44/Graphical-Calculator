class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[0]
    

class Token:
    OPERATORS = "+-*/"

    #token types
    OPERATOR_TYPE = 0
    NUMBER_TYPE = 1
    FUNCTION_TYPE = 2
    BRACKET_TYPE = 3

    def __init__(self):
        self.string = ""
        self.type = None

    def get_type(self, string):
        if len(string) == 1 and string in Token.OPERATORS:
            return Token.OPERATOR_TYPE
        elif len(string) == 1 and (string == "(" or string == ")"):
            return Token.BRACKET_TYPE
        else:
            #the string is either a number or a function
            is_number = True
            for char in string:
                if char not in "0123456789.":
                    is_number = False
                    break

            if is_number:
                return Token.NUMBER_TYPE
            else:
                return Token.FUNCTION_TYPE

    def add_char(self, new_char):
        #check whether the new_char should be added to the token. If so, add it. Return whether the char has been added
        if self.string == "":
            self.string = new_char
            self.type = self.get_type(self.string)

            return True
        
        type_of_char = self.get_type(new_char)
        should_add_char = type_of_char == self.type

        if should_add_char:
            self.string += new_char
        
        return should_add_char


class InfixExpression:
    def __init__(self, expression):
        self.expression = expression

    def tokenise(self):
        tokens = []
        current_token = Token()

        for char in self.expression:
            if char == " ":
                continue
            
            char_added_to_token = current_token.add_char(char)
            
            if not char_added_to_token:
                #The end of the current token has been reached - start adding a new token
                tokens.append(current_token)

                current_token = Token()
                current_token.add_char(char)

        tokens.append(current_token)  #add the final token

        return tokens
        
    def covert_to_postfix(self):
        #use the Shunting Yard algorithm to convert self.expression to postfix
        return ""
    
    def evaluate(self):
        postfix = self.convert_to_postfix()