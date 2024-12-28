import math


class Stack:
    def __init__(self):
        self.items = []

    is_empty = lambda self: len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
    

class Token:
    OPERATOR_PRECEDENCE = {"+" : 1, "-" : 1, "*" : 2, "/" : 3, "^" : 4}

    FUNCTIONS = {
        "sin" : math.sin,
        "cos" : math.cos,
        "tan" : math.tan,
        "sqrt" : math.sqrt
    }

    #token types
    NUMBER_TYPE = 0
    OPERATOR_TYPE = 1
    FUNCTION_TYPE = 2
    BRACKET_TYPE = 3

    def __init__(self):
        self.string = ""
        self.type = None

    is_number = lambda self: self.type == Token.NUMBER_TYPE
    is_operator = lambda self: self.type == Token.OPERATOR_TYPE
    is_function = lambda self: self.type == Token.FUNCTION_TYPE
    is_open_bracket = lambda self: self.type == Token.BRACKET_TYPE and self.string == "("
    is_close_bracket = lambda self: self.type == Token.BRACKET_TYPE and self.string == ")"

    def get_float(self):
        if not self.is_number:
            return
        
        return float(self.string)

    def get_precedence(self):
        if not self.is_operator():
            return  #stops an error being thrown when the OPERATOR_PRECEDENCE dictionary is being accessed
        
        return Token.OPERATOR_PRECEDENCE[self.string]

    def get_type(self, string):
        if len(string) == 1 and string in Token.OPERATOR_PRECEDENCE.keys():
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

        #if the char is a different token type or the current token should only be 1 char long (open bracket or close bracket), this char is a completely new token and should not be added
        should_add_char = type_of_char == self.type and (not self.is_open_bracket() and not self.is_close_bracket())

        if should_add_char:
            self.string += new_char
        
        return should_add_char
    
    def apply_operator(self, operand1, operand2):
        if not self.is_operator():
            return
        
        match self.string:
            case "+":
                return operand1 + operand2
            case "-":
                return operand1 - operand2
            case "*":
                return operand1 * operand2
            case "/":
                return operand1 / operand2
            case "^":
                return operand1 ** operand2
            
    def apply_function(self, argument):        
        func = Token.FUNCTIONS[self.string]

        return func(argument)


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
                #the end of the current token has been reached - start adding a new token
                tokens.append(current_token)

                current_token = Token()
                current_token.add_char(char)

        tokens.append(current_token)  #add the final token

        return tokens
        
    def covert_to_postfix(self, tokenised_expression):
        #use the Shunting Yard algorithm to return postfix expression of tokens
        tokenised_postfix = []
        operator_stack = Stack()

        for token in tokenised_expression:
            if token.is_number():
                tokenised_postfix.append(token)
            elif token.is_function():
                operator_stack.push(token)
            elif token.is_operator():
                is_operator_on_stack = not operator_stack.is_empty() and not operator_stack.peek().is_open_bracket()
                is_operator_precendece_higher = is_operator_on_stack and operator_stack.peek().get_precedence() >= token.get_precedence()

                while is_operator_precendece_higher:
                    #pop the operator on top of the stack onto the output
                    operator_on_stack = operator_stack.pop()
                    tokenised_postfix.append(operator_on_stack)

                    #update is_operator_precendece_higher to check if we need to loop again
                    is_operator_on_stack = not operator_stack.is_empty() and not operator_stack.peek().is_open_bracket()
                    is_operator_precendece_higher = is_operator_on_stack and operator_stack.peek().get_precedence() >= token.get_precedence()

                operator_stack.push(token)  #push the current operator onto the stack
            elif token.is_open_bracket():
                operator_stack.push(token)
            elif token.is_close_bracket():
                while not operator_stack.is_empty() and not operator_stack.peek().is_open_bracket():
                    operator_on_stack = operator_stack.pop()
                    tokenised_postfix.append(operator_on_stack)

                    if operator_stack.is_empty():
                        print("Mismatched brackets")

                #there will be an open bracket and (potentially) a function left on the operator stack
                operator_stack.pop()  #remove the open bracket

                if not operator_stack.is_empty() and operator_stack.peek().is_function():
                    #there is a function on the stack, so remove it
                    function_operator = operator_stack.pop()
                    tokenised_postfix.append(function_operator)

        #any operators still on the operator stack should be appended to the output
        while not operator_stack.is_empty():
            operator = operator_stack.pop()
            tokenised_postfix.append(operator)

        return tokenised_postfix
    
    def evaluate(self):
        tokenised_infix = self.tokenise()
        tokenised_postfix = self.covert_to_postfix(tokenised_infix)

        evaluate_stack = Stack()
        for token in tokenised_postfix:
            if token.is_number():
                numerical_value = token.get_float()
                evaluate_stack.push(numerical_value)
            elif token.is_operator():
                operand2 = evaluate_stack.pop()
                operand1 = evaluate_stack.pop()
            
                result = token.apply_operator(operand1, operand2)

                evaluate_stack.push(result)
            elif token.is_function():
                argument = evaluate_stack.pop()

                result = token.apply_function(argument)

                evaluate_stack.push(result)

        final_result = evaluate_stack.pop()  #evaluation will be only item left in the stack

        return final_result