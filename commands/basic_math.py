"""
Basic mathematical operations and utilities.
"""
from .base_command import BaseCommand
from utils.exceptions import CommandError
from sympy import nsimplify
from decimal import getcontext
import decimal

class BasicMathCommands(BaseCommand):
    """Basic math operations: eval, simplify, expand, factor, etc."""

    def get_commands(self):
        return {
            'eval': self.cmd_eval,
            'simplify': self.cmd_simplify,
            'expand': self.cmd_expand,
            'factor': self.cmd_factor,
            'rationalize': self.cmd_rationalize,
            'precision': self.cmd_precision,
        }

    def get_help(self):
        return {
            'eval': "EVAL: Evaluate mathematical expressions. Usage: eval <expression>",
            'simplify': "SIMPLIFY: Simplify an expression. Usage: simplify <expr>",
            'expand': "EXPAND: Expand an expression. Usage: expand <expr>",
            'factor': "FACTOR: Factor an expression. Usage: factor <expr>",
            'rationalize': "RATIONALIZE: Convert float to rational. Usage: rationalize <num> [tolerance]",
            'precision': "PRECISION: Set display precision. Usage: precision <digits>"
        }

    def cmd_eval(self, args: str):
        """Evaluate expression. If expression begins with 'exact ' we attempt exact parsing."""
        if not args.strip():
            print("Usage: eval <expression>")
            return

        expr_str = args.strip()
        try:
            result = self.parser.parse(expr_str)
            self.formatter.display_result(result, "Result")
        except Exception as e:
            raise CommandError(f"Could not evaluate expression: {e}")

    def cmd_simplify(self, args: str):
        from sympy import simplify
        expr = self.parser.parse(args)
        self.formatter.display_result(simplify(expr), "Simplified")

    def cmd_expand(self, args: str):
        from sympy import expand
        expr = self.parser.parse(args)
        self.formatter.display_result(expand(expr), "Expanded")

    def cmd_factor(self, args: str):
        from sympy import factor
        expr = self.parser.parse(args)
        self.formatter.display_result(factor(expr), "Factored")

    def cmd_rationalize(self, args: str):
        if not args.strip():
            print("Usage: rationalize <number> [tolerance]")
            return
        parts = args.split()
        num_s = parts[0]
        tol = float(parts[1]) if len(parts) > 1 else 1e-10
        try:
            parsed = self.parser.parse(num_s)
            # Use nsimplify to find rational approximation
            root = nsimplify(parsed, tol)
            self.formatter.display_result(root, "Rationalized")
        except Exception as e:
            raise CommandError(f"Could not rationalize: {e}")

    def cmd_precision(self, args: str):
        if not args.strip():
            print(f"Current precision: {self.formatter.precision}")
            return
        try:
            p = int(args.strip())
            self.formatter.set_precision(p)
            # also adjust decimal context to match display precision
            getcontext().prec = max(50, p + 10)
            print(f"Precision set to {p}")
        except Exception as e:
            raise CommandError(f"Invalid precision value: {e}")
