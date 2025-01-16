import math


DIGITS = "0123456789"


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
    ALGEBRA_TERM_TYPE = 4

    def __init__(self):
        self.string = ""
        self.type = None

    is_number = lambda self: self.type == Token.NUMBER_TYPE
    is_operator = lambda self: self.type == Token.OPERATOR_TYPE
    is_function = lambda self: self.type == Token.FUNCTION_TYPE
    is_algebra_term = lambda self: self.type == Token.ALGEBRA_TERM_TYPE
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
    
    def get_algebra_term_name(self):
        if not self.is_algebra_term():
            return
        
        return self.string

    def get_type(self, string):
        if len(string) == 1:
            if string in Token.OPERATOR_PRECEDENCE.keys():
                return Token.OPERATOR_TYPE
            elif string == "(" or string == ")":
                return Token.BRACKET_TYPE
            elif string in DIGITS or string == ".":
                return Token.NUMBER_TYPE
            else:
                return Token.ALGEBRA_TERM_TYPE
        else:
            #the string is either a number (longer than one digit) or a function
            is_number = True
            for char in string:
                if char not in DIGITS and char != ".":
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
        should_add_char = type_of_char == self.type and (not self.is_open_bracket() and not self.is_close_bracket() and not self.is_algebra_term())

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
    
    def __repr__(self):
        #for debugging purposes only
        return f"<Token: type={self.type}, string={self.string}>"


class InfixExpression:
    def __init__(self, expression):
        self.expression = expression
        self.postfix_expression = self.covert_to_postfix()

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
    
    def detect_unary_minus(self, tokenised_expression):
        #detect any unary minus operators and place a 0 before them
        for token_inx, token in enumerate(tokenised_expression):
            if token.is_operator() and token.string == "-":
                if token_inx > 0:
                    prev_token = tokenised_expression[token_inx - 1]
                    is_unary = prev_token.is_operator() or prev_token.is_open_bracket()
                else:
                    is_unary = True

                if is_unary:
                    #the number -12 is the same as 0-12, therefore placing a 0 before the unary minus will ensure it is evaluated correctly
                    zero_token = Token()
                    zero_token.add_char("0")

                    tokenised_expression.insert(token_inx, zero_token)

        return tokenised_expression
    
    def detect_implied_multiplication(self, tokenised_expression):
        #detect if the expression is (1+2)(3+4) instead of (1+2)*(3+4), or 2sin(5) instead of 2*sin(5)
        for token_inx, token in enumerate(tokenised_expression):
            if token_inx == 0: continue  #the first token can never be an implied multiplication

            prev_token = tokenised_expression[token_inx - 1]

            prev_can_be_implied = prev_token.is_number() or prev_token.is_close_bracket() or prev_token.is_algebra_term()
            current_can_be_implied = token.is_open_bracket() or token.is_function() or token.is_algebra_term()

            if prev_can_be_implied and current_can_be_implied:
                #insert a multiplication token to make the multiplication explicit
                mult_token = Token()
                mult_token.add_char("*")

                tokenised_expression.insert(token_inx, mult_token)

        return tokenised_expression

    def covert_tokens_to_postfix(self, tokenised_expression):
        #use the Shunting Yard algorithm to return postfix expression of tokens
        tokenised_postfix = []
        operator_stack = Stack()

        for token in tokenised_expression:
            if token.is_number() or token.is_algebra_term():
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
    
    def covert_to_postfix(self):
        tokenised_infix = self.tokenise()
        
        tokenised_infix = self.detect_unary_minus(tokenised_infix)
        tokenised_infix = self.detect_implied_multiplication(tokenised_infix)

        tokenised_postfix = self.covert_tokens_to_postfix(tokenised_infix)

        return tokenised_postfix
    
    def evaluate(self):
        evaluate_stack = Stack()
        for token in self.postfix_expression:
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
    

class AlgebraicInfixExpression(InfixExpression):
    def __init__(self, expression):
        super().__init__(expression)

    def substitute_variables(self, variable_substitutions):
        substituted_expression = []
        for token in self.postfix_expression:
            if token.is_algebra_term():
                substituted_value = variable_substitutions[token.get_algebra_term_name()]
                substituted_string = str(substituted_value)

                #replace the algebra term token with a number token
                number_token = Token()
                for char in substituted_string:
                    number_token.add_char(char)

                token = number_token

            substituted_expression.append(token)

        return substituted_expression

    def evaluate(self, variable_substitutions):
        new_postfix_expression = self.substitute_variables(variable_substitutions)
        origional_postfix_expression = [i for i in self.postfix_expression]

        self.postfix_expression = new_postfix_expression
        evaluation = super().evaluate()
        self.postfix_expression = origional_postfix_expression

        return evaluation


def evaluate_expression(expression):
    expression_object = InfixExpression(expression)
    result = expression_object.evaluate()

    return result