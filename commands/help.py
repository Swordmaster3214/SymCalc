from .base_command import BaseCommand

class HelpCommands(BaseCommand):
    """Help command listing all available commands."""

    def __init__(self, environment, parser, formatter, registry):
        super().__init__(environment, parser, formatter)
        self.registry = registry

    def get_commands(self):
        return { 'help': self.cmd_help }

    def get_help(self):
        return { 'help': "HELP: Show help for commands. Usage: help [command]" }

    def cmd_help(self, args: str):
        if not args:
            print("Available commands:")
            for cmd, help_text in self.registry.get_all_commands().items():
                first_line = help_text.strip().splitlines()[0]
                print(f"  {cmd} - {first_line}")
        else:
            cmd = args.strip().lower()
            if cmd in self.registry.get_all_commands():
                print(self.registry.get_all_commands()[cmd])
            else:
                print(f"No help available for '{cmd}'")
