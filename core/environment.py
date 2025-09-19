"""
Variable storage and environment management.
"""
import re
from typing import Any, Dict
from utils.exceptions import EnvironmentError

class Environment:
    """Manages stored variables and symbols."""

    VALID_NAME_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    MAX_VARIABLES = 1000  # Prevent memory issues

    def __init__(self):
        self._variables: Dict[str, Any] = {}

    def store(self, name: str, value: Any) -> None:
        """Store a variable."""
        if not self._is_valid_name(name):
            raise EnvironmentError(
                f"Invalid variable name '{name}'. "
                f"Must start with letter/underscore, contain only letters/digits/underscores."
            )

        if len(self._variables) >= self.MAX_VARIABLES:
            raise EnvironmentError(f"Maximum {self.MAX_VARIABLES} variables exceeded")

        self._variables[name] = value

    def get(self, name: str) -> Any:
        """Retrieve a variable."""
        if name not in self._variables:
            raise EnvironmentError(f"Variable '{name}' not found")
        return self._variables[name]

    def has(self, name: str) -> bool:
        """Check if variable exists."""
        return name in self._variables

    def remove(self, name: str) -> None:
        """Remove a variable."""
        if name not in self._variables:
            raise EnvironmentError(f"Variable '{name}' not found")
        del self._variables[name]

    def clear_all(self) -> None:
        """Remove all variables."""
        self._variables.clear()

    def list_variables(self) -> Dict[str, Any]:
        """Get all variables."""
        return self._variables.copy()

    def get_symbol_dict(self) -> Dict[str, Any]:
        """Get variables formatted for SymPy parsing."""
        from sympy import Symbol

        result = {}
        for name, value in self._variables.items():
            if not self._is_valid_name(name):
                continue

            # Handle pint quantities
            if hasattr(value, 'units') and hasattr(value, 'magnitude'):
                try:
                    result[name] = float(value.magnitude)
                except:
                    result[name] = value.magnitude
            else:
                result[name] = value

        return result

    def _is_valid_name(self, name: str) -> bool:
        """Validate variable name."""
        return bool(self.VALID_NAME_PATTERN.match(name))
