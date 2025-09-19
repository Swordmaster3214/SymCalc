from .base_command import BaseCommand
from sympy import diff, integrate, Symbol

class CalculusCommands(BaseCommand):
    """Differentiation and integration commands."""

    def get_commands(self):
        return {
            'diff': self.cmd_diff,
            'integrate': self.cmd_integrate,
        }

    def get_help(self):
        return {
            'diff': "DIFF: Differentiate an expression. Usage: diff <expr> [, var]",
            'integrate': "INTEGRATE: Integrate an expression. Usage: integrate <expr> [, var]",
        }

    def cmd_diff(self, args: str):
        parts = [a.strip() for a in args.split(',') if a.strip()]
        if not parts:
            print("Usage: diff <expr> [, var]")
            return
        expr = self.parser.parse(parts[0])
        if len(parts) > 1:
            var = Symbol(parts[1])
            res = diff(expr, var)
        else:
            # If variable not given, try with default symbol(s)
            res = diff(expr)
        self.formatter.display_result(res, "Derivative")

    def cmd_integrate(self, args: str):
        parts = [a.strip() for a in args.split(',') if a.strip()]
        if not parts:
            print("Usage: integrate <expr> [, var]")
            return
        expr = self.parser.parse(parts[0])
        if len(parts) > 1:
            var = Symbol(parts[1])
            res = integrate(expr, var)
        else:
            res = integrate(expr)
        self.formatter.display_result(res, "Integral")
