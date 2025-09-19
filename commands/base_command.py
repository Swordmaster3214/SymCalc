from typing import Dict, Callable
from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """Base class for all command modules."""

    def __init__(self, environment, parser, formatter):
        self.env = environment
        self.parser = parser
        self.formatter = formatter

    @abstractmethod
    def get_commands(self) -> Dict[str, Callable]:
        """Return dictionary of command_name -> function."""
        pass

    @abstractmethod
    def get_help(self) -> Dict[str, str]:
        """Return dictionary of command_name -> help_text."""
        pass

    def _validate_args(self, args: str, min_args: int = 0) -> bool:
        """Validate minimum argument count."""
        if not args.strip() and min_args > 0:
            return False
        arg_count = len([x for x in args.split(',') if x.strip()]) if args.strip() else 0
        return arg_count >= min_args
