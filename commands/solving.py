from .base_command import BaseCommand
from utils.exceptions import CommandError
from sympy import solve, symbols
from utils.validation import InputValidator

class SolvingCommands(BaseCommand):
    """Equation solving commands."""

    def get_commands(self):
        return {
            'solve': self.cmd_solve,
            'solve_system': self.cmd_solve_system,
        }

    def get_help(self):
        return {
            'solve': "SOLVE: Solve an equation. Usage: solve <equation>, [var]",
            'solve_system': "SOLVE_SYSTEM: Solve system. Usage: solve_system \"eq1; eq2\" vars",
        }

    def cmd_solve(self, args: str):
        if not args.strip():
            raise CommandError("Usage: solve <equation>[, var]")
        parts = [p.strip() for p in args.split(',') if p.strip()]
        eq = self.parser.parse(parts[0])
        if len(parts) > 1:
            vars_ = symbols(parts[1])
            solutions = solve(eq, vars_)
        else:
            solutions = solve(eq)
        self.formatter.display_result(solutions, "Solutions")

    def cmd_solve_system(self, args: str):
        if not args.strip():
            raise CommandError("Usage: solve_system \"eq1; eq2\" vars")
        validator = InputValidator()
        try:
            equations, variables = validator.parse_equation_system(args)
        except Exception as e:
            raise CommandError(str(e))

        eqs = [self.parser.parse(eq) for eq in equations]
        vars_ = [symbols(v) for v in variables]
        try:
            solutions = solve(eqs, vars_)
        except Exception as e:
            raise CommandError(f"Solving error: {e}")

        self.formatter.display_result(solutions, "System Solutions")

        # If solutions is a dict (or list[dict]) attempt verification
        try:
            if isinstance(solutions, dict):
                self.formatter.format_verification(eqs, solutions)
            elif isinstance(solutions, (list, tuple)) and len(solutions) == 1 and isinstance(solutions[0], dict):
                self.formatter.format_verification(eqs, solutions[0])
            else:
                # Converter: try to pick a dict if possible
                if isinstance(solutions, (list, tuple)):
                    for sol in solutions:
                        if isinstance(sol, dict):
                            self.formatter.format_verification(eqs, sol)
                            break
        except Exception:
            pass
