import unittest

from calculator import CalculationError, evaluate_expression, format_result


class EvaluateExpressionTests(unittest.TestCase):
    def test_respects_operator_precedence(self):
        self.assertEqual(evaluate_expression("2 + 3 * 4"), 14)

    def test_supports_parentheses_and_power(self):
        self.assertEqual(evaluate_expression("(2 + 3) ^ 2"), 25)

    def test_supports_square_root(self):
        self.assertEqual(evaluate_expression("sqrt(81)"), 9)

    def test_reports_division_by_zero(self):
        with self.assertRaisesRegex(CalculationError, "membagi dengan nol"):
            evaluate_expression("8 / 0")

    def test_rejects_arbitrary_python(self):
        with self.assertRaises(CalculationError):
            evaluate_expression("__import__('os').system('whoami')")

    def test_formats_decimal_results(self):
        self.assertEqual(format_result(2.5), "2.5")
        self.assertEqual(format_result(4.0), "4")

    def test_rejects_extreme_results(self):
        with self.assertRaisesRegex(CalculationError, "di luar batas"):
            evaluate_expression("9 ^ 1000")

    def test_rejects_negative_square_root(self):
        with self.assertRaisesRegex(CalculationError, "bilangan negatif"):
            evaluate_expression("sqrt(-1)")


if __name__ == "__main__":
    unittest.main()