# Essant's AST and printer


# Base class: Expression
class Expr:
    pass


# Class for Literal values
class Literal(Expr):

    def __init__(self, value):
        self.value = value


# Class for Unary expressions
class Unary(Expr):

    def __init__(self, operator, value):
        self.operator = operator
        self.value = value


# Class for Binary expressions
class Binary(Expr):

    def __init__(self, left, operator, right):
        self.operator = operator
        self.left = left
        self.right = right


# Class for grouped expressions
class Grouping(Expr):

    def __init__(self, expression):
        self.expression = expression



# This is where we actually construct the printer
class ASTPrinter:

    def print(self, expression):

        # Literals
        if isinstance(expression, Literal):
            # Essant uses null instead of None, so this is just for consistency
            if expression.value is None:
                return "null"
            return str(expression.value)


        # Unary 
        elif isinstance(expression, Unary):
            return "(" + expression.operator.lexeme + " " + self.print(expression.value) + ")"


        # Binary
        elif isinstance(expression, Binary):
            return "(" + expression.operator.lexeme + " " + self.print(expression.left) + " " + self.print(expression.right) + ")"


        # Grouped
        elif isinstance(expression, Grouping):
            return "(group " + self.print(expression.expression) + ")"

        else:
            raise TypeError(f"Unknown expression type: {type(expression).__name__}")

