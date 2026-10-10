
# Testing occurs here

#Import the stuff we want to test
from EssantScanner import Token
from EssantAST import Literal, Unary, Binary, Grouping, ASTPrinter

# Create the literal numbers we will be using
ten = Literal(10)
five = Literal(5)
onetwothree = Literal(123)
string = Literal("hello")

# The addition operand
plus = Token("PLUS", "+", None, 1)

# Actually perform the addition
addition = Binary(ten, plus, five)

# Group the addition expression into parenthesis
grouped_addition = Grouping(addition)

# Minus operand
minus = Token("Minus", "-", None, 1)

# Use Unary to put the minus in front of the expression
expression = Unary(minus, grouped_addition)

grouper = Grouping(onetwothree)

printer = ASTPrinter()


# This function compares the results of a test to the expected output
def run_test(name, expression, expected):
    actual = printer.print(expression)

    if actual == expected:
        print(f"PASS: {name}:  {actual}")
    else:
        print(f"FAIL: {name}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")


# Note that the Expected result (and as mentioned in the report, the successfully provided result), is the right most string in each run_test() call

# Test 1: Integer literal
run_test("Integer literal", onetwothree, "123")

# Test 2: String literal
run_test("String literal", string, "hello")

# Test 3: Grouped integer
run_test("Grouped integer", grouper, "(group 123)")

# Test 4: Binary addition
run_test("Binary addition", addition, "(+ 10 5)")

# Test 5: Grouped addition
run_test("Grouped addition", grouped_addition, "(group (+ 10 5))")

# Test 6: Unary minus with grouped addition
run_test("Unary minus with grouping", expression, "(- (group (+ 10 5)))")

# Test 7: True literal
run_test("True literal", Literal(True), "True")

# Test 8: False literal
run_test("False literal", Literal(False), "False")

# Test 9: Null literal
run_test("Null literal", Literal(None), "null")

# Test 10: Unary NOT with true
not_op = Token("EXCLAMATION", "!", None, 1)
not_true = Unary(not_op, Literal(True))

run_test("Unary NOT", not_true, "(! True)")


# Test 11: Subtraction
run_test("Subtraction", Binary(ten, minus, five), "(- 10 5)")

# Test 12: Multiplication
multiply = Token("STAR", "*", None, 1)
run_test("Multiplication", Binary(ten, multiply, five), "(* 10 5)")

# Test 13: Division
divide = Token("SLASH", "/", None, 1)
run_test("Division", Binary(ten, divide, five), "(/ 10 5)")

# Test 14: Modulo
modulo = Token("PERCENT", "%", None, 1)
run_test("Modulo", Binary(ten, modulo, five), "(% 10 5)")

# Test 15: Equal to
equal_equal = Token("EQUAL_EQUAL", "==", None, 1)
run_test("Equal to", Binary(ten, equal_equal, five), "(== 10 5)")

# Test 16: Not equal to
not_equal = Token("EXCLAMATION_EQUAL", "!=", None, 1)
run_test("Not equal to", Binary(ten, not_equal, five), "(!= 10 5)")

# Test 17: Less than
less = Token("LESS", "<", None, 1)
run_test("Less than", Binary(ten, less, five), "(< 10 5)")

# Test 18: Less than or equal to
less_equal = Token("LESS_EQUAL", "<=", None, 1)
run_test("Less than or equal", Binary(ten, less_equal, five), "(<= 10 5)")

# Test 19: Greater than
greater = Token("GREATER", ">", None, 1)
run_test("Greater than", Binary(ten, greater, five), "(> 10 5)")

# Test 20: Greater than or equal to
greater_equal = Token("GREATER_EQUAL", ">=", None, 1)
run_test("Greater than or equal", Binary(ten, greater_equal, five), "(>= 10 5)")

# Test 21: Logical AND
and_operator = Token("AND", "and", None, 1)
run_test("Logical AND", Binary(Literal(True), and_operator, Literal(False)), "(and True False)")

# Test 22: Logical OR
or_operator = Token("OR", "or", None, 1)
run_test("Logical OR", Binary(Literal(True), or_operator, Literal(False)), "(or True False)")

# Test 23: Nested Binary Expression
nested = Binary(addition, multiply, onetwothree)

run_test("Nested binary expression", nested, "(* (+ 10 5) 123)")

# Test 24: Nested unary expressions: -(-10)
inner_minus = Unary(minus, ten)
outer_minus = Unary(minus, inner_minus)

run_test("Nested unary expressions", outer_minus, "(- (- 10))")

# Test 25: Grouping inside a binary expression: 10 + (5)
grouped_five = Grouping(five)
addition_with_group = Binary(ten, plus, grouped_five)

run_test("Grouping inside binary expression", addition_with_group, "(+ 10 (group 5))")