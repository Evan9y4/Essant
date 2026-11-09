#Parser for Essant


#Import neccasary classes
from EssantAST import Literal, Unary, Binary, Grouping, Expression, Print
from EssantErrors import ErrorHandler


#This class is for error handling
class ParseError(Exception):
    pass

      

# The class that does the parsing
class Parser:
    def __init__(self, token_list):
        self.tokens = token_list
        self.index = 0


    #Parses one complete expression
    def parse(self):
        
        #create an empty list
        statements = []

        #While we are not at the last token, if the statement is not None, add it to our list
        while not self.last_token():

            try:

                statement = self.statement()

                if statement is not None:
                    statements.append(statement)


            #If we get an error, print it and recover
            except ParseError as error:
                print(error)
                self.recover()

        #return list
        return statements


    # simply determines the statement type
    def statement(self):

        if self.match("PRINT"):
            return self.print_statement()

        return self.expression_statement()


    #handles expression statements
    def expression_statement(self):

        expression = self.expression()

        self.consume("SEMICOLON", "Expected ; after expression.")

        return Expression(expression)


    #handles expression statements
    def print_statement(self):

        expression = self.expression()

        self.consume("SEMICOLON", "Expected ; after expression.")

        return Print(expression)


    #Method for handling expressions. Expression -> equality
    def expression(self):
        return self.equality()


    #Method for hnadling equality comparisons(== or !=). Equality -> Comparison
    def equality(self):
        expression = self.comparison()

        while self.match("EQUAL_EQUAL", "EXCLAMATION_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)

        return expression


    #Method for handling comparisons (<, <=, >, >=). Comparison -> Term
    def comparison(self):
        expression = self.term()

        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)


        return expression


    #Method for handling terms (+ or -). Term -> factor
    def term(self):
        expression = self.factor()

        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)


        return expression


    #Method for handling factors (* or /) Factor -> Unary
    def factor(self):
        expression = self.unary()

        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)


        return expression


    #Method for handling unaries (! or -). Unary -> primary
    def unary(self):
        if self.match("EXCLAMATION", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()


    #Method for handling primaries, which will be literals and groups
    def primary(self):
        if self.match("FALSE"):
            return Literal(False)

        if self.match("TRUE"):
            return Literal(True)

        if self.match("NULL"):
            return Literal(None)

        if self.match("NUMBER", "STRING"):
            return Literal(self.previous().literal)

        if self.match("LEFT_PAREN"):
            expression = self.expression()

            self.consume("RIGHT_PAREN", "Expected ')' after expression.")

            return Grouping(expression)

        raise self.error(self.look(), "Expected an expression")


    # Check whether the current token matches any defined type
    def match(self, *token_types):

        for token in token_types:

            if self.check(token):
                self.advance()
                return True

        return False


    #Checks the current token without "consuming" it
    def check(self, token_type):

        if self.last_token():
            return token_type == "EOF"

        return self.look().token_type == token_type


    #Consume a token if it has the expected type
    def consume(self, token_type, message):

        if self.check(token_type):
            return self.advance()

        raise self.error(self.look(), message)


    #Looks at the current token WITHOUT moving
    def look(self):
        return self.tokens[self.index]


    #Moves forward to the next token
    def advance(self):

        if not self.last_token():
            self.index += 1

        return self.previous()


    #Returns the token that was recently consumed
    def previous(self):
        return self.tokens[self.index - 1]

    #Detects when all of the tokens have been scanned
    def last_token(self):
        return self.look().token_type == "EOF"


    #Create a syntax error
    def error(self, token, message):

        if token.token_type == "EOF":
            location = "at end"
        else:
            location = f"at '{token.lexeme}'"

        return ParseError(f"[Line {token.line}] Error {location}: {message}")


    #Recovery from parsing error
    def recover(self):

        #while we are not at the last token
        while not self.last_token():

            #The previous statment (the one with the error!) has ended
            if self.previous().token_type == "SEMICOLON":
                return

            #A new statment, which can be started with any of the following token types, is detected
            if self.look().token_type in ("PRINT", "FALSE", "TRUE", "NULL", "NUMBER", "STRING", "LEFT_PAREN", "EXCLAMATION", "MINUS"):
                return

            #Keep advancing until we end the previous statment or a new one begins
            self.advance()