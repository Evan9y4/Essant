from EssantScanner import Token
from EssantAST import Literal, Unary, Binary, Grouping
from EssantEvaluator import Evaluator
from Essant import ErrorHandler


errors = ErrorHandler()
evaluator = Evaluator(errors)


def token(name, lexeme):
    return Token(name, lexeme, None, 1)


def binary(left, op, right):
    return Binary(Literal(left), token(op, op), Literal(right))


tests = [
    ("addition", binary(2, "PLUS", 3), 5),
    ("subtraction", binary(7, "MINUS", 2), 5),
    ("multiplication", binary(3, "STAR", 4), 12),
    ("division", binary(8, "SLASH", 2), 4.0),
    ("modulo", binary(7, "PERCENT", 3), 1),
    ("concatenation", binary("Hello ", "PLUS", "world"), "Hello world"),
    ("boolean coercion", binary(True, "PLUS", 2), 3),
    ("false coercion", binary(False, "STAR", 10), 0),
    ("less than", binary(2, "LESS", 3), True),
    ("equality", binary(5, "EQUAL_EQUAL", 5), True),
    ("different types", binary(5, "EQUAL_EQUAL", "5"), False),
    ("inequality", binary(5, "EXCLAMATION_EQUAL", 3), True)
]

tests_that_must_fail = [
    ("division by zero", binary(17, "SLASH", 0), None),
    ("modulo by zero", binary(25, "PERCENT", 0), None)
    ]

for name, expression, expected in tests:
    errors.has_error = False
    result = evaluator.evaluate(expression)

    assert not errors.has_error, f"{name}: unexpected error"
    assert result == expected, (
        f"{name}: expected {expected!r}, got {result!r}"
    )
    print(f"PASS: {name}")


for name, expression, expected in tests_that_must_fail:
    errors.has_error = False
    result = evaluator.evaluate(expression)

    assert errors.has_error
    assert result is None
    print(f"PASS: {name}")
