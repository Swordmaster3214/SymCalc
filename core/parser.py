"""
Expression parsing with standardized validation.
"""
import re
from decimal import Decimal
from sympy import (
    parse_expr, sympify, Eq, Lt, Gt, Le, Ge, Ne,
    Rational
)
from sympy.parsing.sympy_parser import (
    standard_transformations, implicit_multiplication_application, convert_xor
)
from utils.exceptions import ParseError

class ExpressionParser:
    """Handles all expression parsing with consistent behavior."""

    TRANSFORMATIONS = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

    def __init__(self, environment):
        self.env = environment

    def parse(self, expression: str):
        """Parse a mathematical expression or equation."""
        if not expression.strip():
            raise ParseError("Empty expression")

        # Check for inequalities first
        inequality_ops = ['<=', '>=', '<', '>', '!=']
        for op in inequality_ops:
            if op in expression and not expression.strip().startswith('Matrix'):
                return self._parse_inequality(expression, op)

        # Check for equations
        if '=' in expression and not expression.strip().startswith('Matrix'):
            return self._parse_equation(expression)

        # Regular expression
        return self._parse_expression(expression)

    def _parse_expression(self, expr_str: str):
        """Parse a regular mathematical expression."""
        try:
            return parse_expr(
                expr_str,
                transformations=self.TRANSFORMATIONS,
                local_dict=self.env.get_symbol_dict(),
                evaluate=True
            )
        except Exception as e:
            raise ParseError(f"Could not parse expression '{expr_str}': {e}")

    def _parse_equation(self, eq_str: str):
        """Parse an equation (contains =)."""
        try:
            left, right = eq_str.split('=', 1)
            left_expr = self._parse_expression(left.strip())
            right_expr = self._parse_expression(right.strip())
            return Eq(left_expr, right_expr)
        except ValueError:
            raise ParseError("Multiple = signs not supported")
        except Exception as e:
            raise ParseError(f"Could not parse equation: {e}")

    def _parse_inequality(self, ineq_str: str, op: str):
        """Parse an inequality."""
        try:
            left, right = ineq_str.split(op, 1)
            left_expr = self._parse_expression(left.strip())
            right_expr = self._parse_expression(right.strip())

            op_map = {
                '<': Lt, '>': Gt, '<=': Le,
                '>=': Ge, '!=': Ne
            }
            return op_map[op](left_expr, right_expr)
        except Exception as e:
            raise ParseError(f"Could not parse inequality: {e}")

    def parse_number(self, number_str: str):
        """Parse a number with maximum precision preservation."""
        try:
            # Try fraction first
            if '/' in number_str and 'e' not in number_str.lower():
                parts = number_str.split('/')
                if len(parts) == 2:
                    return Rational(int(parts[0].strip()), int(parts[1].strip()))

            # Try decimal
            decimal_val = Decimal(number_str)
            return Rational(str(decimal_val))

        except Exception:
            # Fallback to sympify
            return sympify(number_str)
