#Tests used for the parser


#I was having trouble with file structures and locations, so I did use an AI for the imports AND setting up the test cases.
#// --- start AI code ---
import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

print("Testing scanner import...")

try:
    import EssantScanner
    print("Scanner imported successfully!")

    from EssantScanner import Scanner
    from EssantParser import Parser
    from EssantAST import Literal, Unary, Binary, Grouping, ASTPrinter
    from Essant import ErrorHandler

    print("All Essant modules imported successfully!")

except Exception as error:
    print("Import failed:", repr(error))




def parse_source(source):
    """Scan source code and parse it into an AST."""
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    return parser.parse()

class TestParserExpressions(unittest.TestCase):

    def parse_valid(self, source):
        expression = parse_source(source)
        self.assertIsNotNone(expression, f"Failed to parse: {source}")
        return expression


#// --- end AI code ---


    # ----- Literal types -----

    def test_number_literal(self):
        expression = self.parse_valid("123")
        self.assertIsInstance(expression, Literal)
        self.assertEqual(expression.value, 123)

    def test_string_literal(self):
        expression = self.parse_valid('"hello"')
        self.assertIsInstance(expression, Literal)
        self.assertEqual(expression.value, "hello")

    def test_true_literal(self):
        expression = self.parse_valid("true")
        self.assertIsInstance(expression, Literal)
        self.assertIs(expression.value, True)

    def test_false_literal(self):
        expression = self.parse_valid("false")
        self.assertIsInstance(expression, Literal)
        self.assertIs(expression.value, False)

    def test_null_literal(self):
        expression = self.parse_valid("null")
        self.assertIsInstance(expression, Literal)
        self.assertIsNone(expression.value)

    # ----- Unary expressions -----

    def test_unary_minus(self):
        expression = self.parse_valid("-123")
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.lexeme, "-")
        self.assertEqual(expression.value.value, 123)

    def test_unary_not(self):
        expression = self.parse_valid("!true")
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.lexeme, "!")
        self.assertIsInstance(expression.value, Literal)

    def test_chained_unary(self):
        expression = self.parse_valid("!-123")
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.lexeme, "!")
        self.assertIsInstance(expression.value, Unary)
        self.assertEqual(expression.value.operator.lexeme, "-")

    # ----- Binary operators -----

    def test_arithmetic_operators(self):
        cases = [
            ("10 + 5", "+"),
            ("10 - 5", "-"),
            ("10 * 5", "*"),
            ("10 / 5", "/"),
        ]

        for source, operator in cases:
            with self.subTest(source=source):
                expression = self.parse_valid(source)
                self.assertIsInstance(expression, Binary)
                self.assertEqual(expression.operator.lexeme, operator)

    def test_comparison_operators(self):
        cases = [
            ("1 > 2", ">"),
            ("1 >= 2", ">="),
            ("1 < 2", "<"),
            ("1 <= 2", "<="),
        ]

        for source, operator in cases:
            with self.subTest(source=source):
                expression = self.parse_valid(source)
                self.assertIsInstance(expression, Binary)
                self.assertEqual(expression.operator.lexeme, operator)

    def test_equality_operators(self):
        cases = [
            ("1 == 2", "=="),
            ("1 != 2", "!="),
        ]

        for source, operator in cases:
            with self.subTest(source=source):
                expression = self.parse_valid(source)
                self.assertIsInstance(expression, Binary)
                self.assertEqual(expression.operator.lexeme, operator)


    # ----- Grouping, precedence, and associativity -----

    def test_grouping(self):
        expression = self.parse_valid("(123)")
        self.assertIsInstance(expression, Grouping)
        self.assertIsInstance(expression.expression, Literal)

    def test_nested_grouping(self):
        expression = self.parse_valid("((123))")
        self.assertIsInstance(expression, Grouping)
        self.assertIsInstance(expression.expression, Grouping)

    def test_multiplication_precedes_addition(self):
        expression = self.parse_valid("1 + 2 * 3")
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.lexeme, "+")
        self.assertEqual(expression.right.operator.lexeme, "*")

    def test_parentheses_override_precedence(self):
        expression = self.parse_valid("(1 + 2) * 3")
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.lexeme, "*")
        self.assertIsInstance(expression.left, Grouping)

    def test_left_associative_subtraction(self):
        expression = self.parse_valid("10 - 5 - 2")
        self.assertEqual(expression.operator.lexeme, "-")
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.lexeme, "-")

    def test_left_associative_division(self):
        expression = self.parse_valid("20 / 5 / 2")
        self.assertEqual(expression.operator.lexeme, "/")
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.lexeme, "/")

    # ----- AST printer -----

    def test_ast_printer(self):
        expression = self.parse_valid("10 + 5")
        output = ASTPrinter().print(expression)
        self.assertEqual(output, "(+ 10 5)")

    # ----- Invalid syntax -----

    def test_invalid_expressions(self):
        invalid_cases = [
            "()",          # Empty grouping
            "(1 + 2",      # Missing closing parenthesis
            "1 +",         # Missing right operand
            "* 2",         # Operator without a left operand
            "1 2",         # Unexpected extra expression
            "-",           # Unary operator without an operand
            "1 + * 2",     # Two operators in an invalid sequence
            "1 == ",       # Missing equality operand
            "((1)",        # Missing closing parenthesis in nesting
        ]

        for source in invalid_cases:
            with self.subTest(source=source):
                self.assertIsNone(parse_source(source))



if __name__ == "__main__":
    unittest.main()