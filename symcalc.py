#!/usr/bin/env python3
"""
SymCalc - Main entry point and REPL
"""
import sys
from pathlib import Path

# Ensure package modules are importable (project root)
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.environment import Environment
from core.parser import ExpressionParser
from core.formatter import OutputFormatter
from commands.command_registry import CommandRegistry
from utils.validation import InputValidator
from utils.exceptions import SymCalcError

class SymCalc:
    """Main SymCalc application class."""

    def __init__(self):
        self.env = Environment()
        self.parser = ExpressionParser(self.env)
        self.formatter = OutputFormatter()
        self.validator = InputValidator()
        self.commands = CommandRegistry(self.env, self.parser, self.formatter)

        # Setup SymPy pretty printing
        from sympy import init_printing
        init_printing(use_unicode=True)

    def show_welcome(self):
        """Display welcome message."""
        print("""
SymCalc - SymPy REPL + Science Calculator
Modular architecture with exact + decimal output
Type 'help' for commands, 'exit' to quit.

Features:
- Persistent variables with 'let'
- Unit conversions with 'convert'
- Equation solving with 'solve', 'solve_system'
- Statistical functions: mean, stdev, etc.
- Both exact and decimal results shown automatically
        """)

    def process_command(self, raw_input: str) -> bool:
        """
        Process a single command input.
        Returns True to continue REPL, False to exit.
        """
        try:
            # Validate and clean input
            cleaned_input = self.validator.clean_input(raw_input)
            if not cleaned_input:
                return True

            # Handle exit commands
            if cleaned_input.lower() in ('exit', 'quit', 'q'):
                return False

            # Parse command and arguments
            parts = cleaned_input.split(None, 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Try to execute as registered command
            if self.commands.has_command(command):
                self.commands.execute(command, args)
            else:
                # Treat as mathematical expression
                self._evaluate_expression(cleaned_input)

        except KeyboardInterrupt:
            return False
        except SymCalcError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            if "--debug" in sys.argv:
                import traceback
                traceback.print_exc()

        return True

    def _evaluate_expression(self, expression: str):
        """Evaluate a mathematical expression."""
        try:
            result = self.parser.parse(expression)
            self.formatter.display_result(result, label="Result")
        except Exception as e:
            print(f"Expression evaluation error: {e}")

    def run_repl(self):
        """Run the main REPL loop."""
        self.show_welcome()

        while True:
            try:
                raw_input = input("SymCalc> ").strip()
                if not self.process_command(raw_input):
                    break
            except (EOFError, KeyboardInterrupt):
                break

        print("\nGoodbye!")

    def run_file(self, filename: str):
        """Execute commands from a file."""
        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(f"[{line_num}] {line}")
                        if not self.process_command(line):
                            break
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error reading file: {e}")

def main():
    """Main entry point."""
    calc = SymCalc()

    if len(sys.argv) > 1:
        # File mode
        calc.run_file(sys.argv[1])
    else:
        # Interactive mode
        calc.run_repl()

if __name__ == '__main__':
    main()
