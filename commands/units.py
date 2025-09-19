from .base_command import BaseCommand
from utils.exceptions import ConversionError

class UnitCommands(BaseCommand):
    """Unit conversion and management commands."""

    def get_commands(self):
        return {
            'convert': self.cmd_convert,
        }

    def get_help(self):
        return {
            'convert': "CONVERT: Convert units. Usage: convert <value and units> to <unit>",
        }

    def cmd_convert(self, args: str):
        try:
            from pint import UnitRegistry
            ureg = UnitRegistry()
            if ' to ' not in args:
                raise ConversionError("Usage: convert <value and units> to <unit>")
            value_str, unit_str = args.split(' to ', 1)
            value = ureg(value_str.strip())
            converted = value.to(unit_str.strip())
            print(f"{value} = {converted}")
        except Exception as e:
            raise ConversionError(str(e))
