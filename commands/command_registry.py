# commands/command_registry.py

import sys
import pkgutil
import importlib
import inspect
from .base_command import BaseCommand


class CommandRegistry:
    """
    Registry that discovers and manages all available command classes.
    Commands live in modules under the 'commands' package and must
    subclass BaseCommand.
    """

    def __init__(self, environment, parser, formatter):
        self.env = environment
        self.parser = parser
        self.formatter = formatter
        self._commands = {}
        self._help_text = {}
        self._register_all_commands()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def execute_command(self, command_name, args):
        """
        Look up and execute the given command.
        """
        command_name = command_name.lower()
        if command_name in self._commands:
            return self._commands[command_name](args)
        else:
            print(f"Unknown command: {command_name}")
            return None

    def get_all_commands(self):
        """
        Return a dict of {command_name: help_text}.
        """
        return dict(self._help_text)

    # ------------------------------------------------------------------
    # Automatic discovery
    # ------------------------------------------------------------------
    def _register_all_commands(self):
        """
        Auto-discover command modules under the 'commands' package and
        instantiate any class that subclasses BaseCommand (except
        BaseCommand itself).

        Handles both constructors:
          - (env, parser, formatter)
          - (env, parser, formatter, registry)  <-- e.g. HelpCommands
        """
        pkg = importlib.import_module("commands")
        prefix = pkg.__name__ + "."

        for finder, modname, ispkg in pkgutil.iter_modules(pkg.__path__, prefix):
            if modname.endswith("command_registry") or modname.endswith("__init__"):
                continue

            try:
                mod = importlib.import_module(modname)
            except Exception as e:
                if "--debug" in sys.argv:
                    print(f"[debug] failed to import {modname}: {e}")
                continue

            for _, obj in inspect.getmembers(mod, inspect.isclass):
                try:
                    if not issubclass(obj, BaseCommand) or obj is BaseCommand:
                        continue

                    # Determine constructor arity (exclude 'self')
                    sig = inspect.signature(obj.__init__)
                    params = [p for p in sig.parameters.values() if p.name != "self"]
                    param_count = len(params)

                    instance = None
                    if param_count == 3:
                        # common: (env, parser, formatter)
                        instance = obj(self.env, self.parser, self.formatter)
                    elif param_count == 4:
                        # help commands: (env, parser, formatter, registry)
                        instance = obj(self.env, self.parser, self.formatter, self)
                    else:
                        # attempt flexible instantiation
                        try:
                            instance = obj(self.env, self.parser, self.formatter)
                        except Exception:
                            try:
                                instance = obj(self.env, self.parser, self.formatter, self)
                            except Exception:
                                if "--debug" in sys.argv:
                                    print(f"[debug] could not instantiate {obj} (sig: {sig})")
                                continue

                    if instance is not None:
                        try:
                            for cmd_name, cmd_func in instance.get_commands().items():
                                self._commands[cmd_name] = cmd_func
                            for cmd_name, help_text in instance.get_help().items():
                                self._help_text[cmd_name] = help_text
                        except Exception as e:
                            if "--debug" in sys.argv:
                                print(f"[debug] registration failed for {obj}: {e}")

                except Exception:
                    if "--debug" in sys.argv:
                        import traceback
                        traceback.print_exc()
                    continue
