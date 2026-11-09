#Essant's evaluator


#Import several neccesary classes
from EssantErrors import ErrorHandler
from EssantAST import Literal, Unary, Binary, Grouping, Expression, Print
from EssantScanner import Token



#The actual evaluator
class Evaluator:
    def __init__(self, error_handler):
        self.error_handler = error_handler


    #Executes a given statement
    def execute(self, statement):

        #For expression statements, we will evaluate them without displaying them
        if isinstance(statement, Expression):
            self.evaluate(statement.expression)


        #For print statements, we evaluate them and then display the results
        elif isinstance(statement, Print):
            value = self.evaluate(statement.expression)

            print(value)

        else:
            self.error_handler.error("Unknown statement type detected")
    #Recursive evaluation. The recursiveness makes it work like post order traversal.
    def evaluate(self, expression):

        #Edge Case for when it's passed a Literal
        if isinstance(expression, Literal):
            return expression.value

        #Evaluate groupings
        if isinstance(expression, Grouping):
            return self.evaluate(expression.expression)


        #Evaluate Unary
        if isinstance(expression, Unary):
            right = self.evaluate(expression.value)
            return self.unary_eval(expression.operator, right)


        #Evaluate Binary
        if isinstance(expression, Binary):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            return self.binary_eval(expression.operator, left, right)

        #If we get this far, report an error and prevent a runtime error
        else:
            self.error_handler.error("Unknown expression type!")
            return None



    #Evaluate a Unary expression
    def unary_eval(self, operator, right):

        if operator.token_type == "MINUS":

            #If it receives a boolean, convert it into a number
            if type(right) is bool:
                right = int(right)

            #If the operand is not an integer or a float, report error and prevent a runtime error
            if type(right) not in (int, float):
                self.error_handler.error("Operand must be a number(Integer, Float, or a Boolean)!")
                return None

            return -right

        #If ! or Unary not
        if operator.token_type == "EXCLAMATION":
            return not self.is_truthy(right)


        #If this function gets this far, we have an unknown operator. Report the error and prevent a runtime error
        else:
            self.error_handler.error("Unknown Unary operator. Unary supports only '-' and '!'")
            return None


    #Evaluate a Binary expression
    def binary_eval(self, operator, left, right):
        token = operator.token_type
        
        #Set an initial value for equal, just in case
        equal = False

        #This part handles equalities, mismatched types are always false
        if token in ("EQUAL_EQUAL", "EXCLAMATION_EQUAL"):
            if type(left) is not type(right):
                equal = False
            else:
                equal = left == right

            if token == "EXCLAMATION_EQUAL":
                return not equal

            return equal

        #Since the above section is the only part that requires booleans, we can convert them now before the arithmetic
        if type(left) is bool:
            left = int(left)

        if type(right) is bool:
            right = int(right)


        #Addition gets it's own little section apart from other arithmetic because of cancatenation
        if token == "PLUS":
            if self.is_number(left) and self.is_number(right):
                return left + right

            elif type(left) is str and type(right) is str:
                return left + right

            #Unfortunately, operands have to be of the same type for "+" to work
            else:
                self.error_handler.error("Operands must BOTH be numbers or strings for + to work")
                return None

        #The other arithmetic operators, must all be numbers
        if token in ("MINUS", "STAR", "SLASH", "PERCENT"):
            #Edge case to prevent runtime errors
            if not self.is_number(left) or not self.is_number(right):
                self.error_handler.error("Both operands have to be numbers for arithmetic to work!")
                return None

            #Edge case to prevent runtime errors
            if token in ("SLASH", "PERCENT") and right == 0:
                self.error_handler.error("Tried to divide or modulo by zero")
                return None

            if token == "MINUS":
                return left - right

            if token == "STAR":
                return left * right

            if token == "SLASH":
                return left / right

            if token == "PERCENT":
                return left % right

        #Comparisons, only supports numbers as of now
        if token in ("LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"):
            #Edge case to prevent runtime error
            if not self.is_number(left) or not self.is_number(right):
                self.error_handler.error("Both operands have to be numbers for comparisons")
                return None


            if token == "LESS":
                return left < right

            if token == "LESS_EQUAL":
                return left <= right

            if token == "GREATER":
                return left > right

            if token == "GREATER_EQUAL":
                return left >= right

        #If the program gets this far without returning, than an unknown operator was sent
        self.error_handler.error("Unknown operator received")
        return None


    #Method to help define what is 'True' and what is 'False"
    def is_truthy(self, value):
        #Only returns false if given None or False
        if value is None or value is False:
            return False

        #In every other case, return True
        return True


    #This method just states that only integers and floats are number (remember, booleans get converted in the actual evaluation!)
    def is_number(self, value):
        return type(value) in (int, float)