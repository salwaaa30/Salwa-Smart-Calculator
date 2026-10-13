import ast
import math
import operator

MAX_RESULT = 1e100


def _checked_result(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalculationError("Hasil di luar batas")
    if abs(value) > MAX_RESULT or (isinstance(value, float) and not math.isfinite(value)):
        raise CalculationError("Hasil di luar batas")
    return value


class CalculationError(Exception):
    """Raised when an expression cannot be evaluated safely."""


class _ExpressionEvaluator(ast.NodeVisitor):
    _binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }
    _unary_operators = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return _checked_result(node.value)
        raise CalculationError("Ekspresi tidak valid")

    def visit_Num(self, node):
        return node.n

    def visit_BinOp(self, node):
        operation = self._binary_operators.get(type(node.op))
        if operation is None:
            raise CalculationError("Operator tidak didukung")

        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise CalculationError("Pangkat terlalu besar")
        try:
            return _checked_result(operation(left, right))
        except ZeroDivisionError as error:
            raise CalculationError("Tidak dapat membagi dengan nol") from error
        except (OverflowError, ValueError) as error:
            raise CalculationError("Hasil di luar batas") from error

    def visit_UnaryOp(self, node):
        operation = self._unary_operators.get(type(node.op))
        if operation is None:
            raise CalculationError("Operator tidak didukung")
        return _checked_result(operation(self.visit(node.operand)))

    def visit_Call(self, node):
        if (
            not isinstance(node.func, ast.Name)
            or node.func.id != "sqrt"
            or len(node.args) != 1
            or node.keywords
        ):
            raise CalculationError("Ekspresi tidak valid")
        try:
            return _checked_result(math.sqrt(self.visit(node.args[0])))
        except ValueError as error:
            raise CalculationError("Akar bilangan negatif tidak terdefinisi") from error

    def generic_visit(self, node):
        raise CalculationError("Ekspresi tidak valid")


def evaluate_expression(expression):
    """Evaluate basic arithmetic without executing arbitrary Python code."""
    if len(expression) > 256:
        raise CalculationError("Ekspresi terlalu panjang")
    normalized = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
    try:
        tree = ast.parse(normalized, mode="eval")
        result = _ExpressionEvaluator().visit(tree)
    except CalculationError:
        raise
    except (SyntaxError, TypeError, ZeroDivisionError, RecursionError) as error:
        raise CalculationError("Ekspresi tidak valid") from error

    return _checked_result(result)


def format_result(value):
    if isinstance(value, int):
        return str(value)
    if value.is_integer():
        return str(int(value))
    return format(value, ".12g")