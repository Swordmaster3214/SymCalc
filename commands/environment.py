"""
Environment management commands (let, view, clear).
"""
from .base_command import BaseCommand
from utils.exceptions import CommandError, EnvironmentError

class EnvironmentCommands(BaseCommand):
    """Commands for variable management."""

    def get_commands(self):
        return {
            'let': self.cmd_let,
            'view': self.cmd_view,
            'clear': self.cmd_clear,
        }

    def get_help(self):
        return {
            'let': """
LET: Store variables and expressions.

Usage:
  let <name>           - Create symbolic variable
  let <name> = <expr>  - Store expression or value
""",
            'view': "VIEW: Display all stored variables. Usage: view",
            'clear': "CLEAR: Remove stored variables. Usage: clear <name> | clear all"
        }

    def cmd_let(self, args: str):
        """Handle let command."""
        if not args.strip():
            print("Usage: let <name> [= <expr>]")
            return

        try:
            if '=' in args:
                # Assignment
                name_part, value_part = args.split('=', 1)
                name = name_part.strip()
                value_str = value_part.strip()

                # Parse and store value
                try:
                    # Try as unit quantity first (if pint available)
                    if self._try_store_unit_quantity(name, value_str):
                        return

                    # Parse as expression
                    value = self.parser.parse(value_str)
                    self.env.store(name, value)

                    # Display what was stored
                    if hasattr(value, 'is_Number') and value.is_Number:
                        self.formatter.display_result(value, f"Stored {name}")
                    else:
                        print(f"Stored symbolic expression: {name} = {value}")

                except Exception as e:
                    # Fallback to direct numeric parsing
                    try:
                        numeric_val = self.parser.parse_number(value_str)
                        self.env.store(name, numeric_val)
                        self.formatter.display_result(numeric_val, f"Stored {name}")
                    except Exception:
                        raise CommandError(f"Could not parse value: {e}")
            else:
                # Just create symbol
                name = args.strip()
                from sympy import Symbol
                symbol = Symbol(name)
                self.env.store(name, symbol)
                print(f"Created symbol: {name}")

        except EnvironmentError as e:
            raise CommandError(str(e))

    def _try_store_unit_quantity(self, name: str, value_str: str) -> bool:
        """Try to store as pint unit quantity."""
        try:
            from pint import UnitRegistry
            ureg = UnitRegistry()
            quantity = ureg(value_str)
            self.env.store(name, quantity)
            print(f"Stored unit quantity: {name} = {quantity}")
            return True
        except Exception:
            return False

    def cmd_view(self, args: str):
        """Handle view command."""
        variables = self.env.list_variables()

        if not variables:
            print("Environment is empty.")
            return

        print("Stored variables:")
        for name, value in sorted(variables.items()):
            # Determine type and display format
            if hasattr(value, 'units'):  # pint quantity
                print(f"  {name:12} (unit)       = {value}")
            elif hasattr(value, 'is_Symbol') and value.is_Symbol:
                print(f"  {name:12} (symbol)     = {value}")
            elif hasattr(value, 'is_Number') and value.is_Number:
                print(f"  {name:12} (number)     = {value}")
            else:
                print(f"  {name:12} (expression) = {value}")

    def cmd_clear(self, args: str):
        """Handle clear command."""
        if not args.strip():
            print("Usage: clear <name> | clear all")
            return

        target = args.strip().lower()

        if target in ('all', '*'):
            self.env.clear_all()
            print("Cleared all variables.")
        else:
            try:
                self.env.remove(args.strip())  # Use original case
                print(f"Cleared variable: {args.strip()}")
            except EnvironmentError as e:
                raise CommandError(str(e))
