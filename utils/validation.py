"""
Standardized input validation utilities.
"""
import re
from typing import List, Tuple
from utils.exceptions import ValidationError

class InputValidator:
    """Standardized input validation for all commands."""

    # Common patterns
    NUMBER_PATTERN = re.compile(r'^-?\d*\.?\d+([eE][-+]?\d+)?$')
    VARIABLE_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    def clean_input(self, raw_input: str) -> str:
        """Clean and validate raw input."""
        if not isinstance(raw_input, str):
            raise ValidationError("Input must be a string")

        # Remove extra whitespace
        cleaned = ' '.join(raw_input.split())

        # Check for dangerous patterns (case-insensitive)
        lowered = cleaned.lower()
        dangerous_patterns = ['__', 'eval ', 'exec ', 'import ', 'open(']
        for pattern in dangerous_patterns:
            if pattern in lowered:
                raise ValidationError(f"Potentially dangerous input detected: {pattern.strip()}")

        return cleaned

    def validate_variable_name(self, name: str) -> str:
        """Validate a variable name."""
        if not self.VARIABLE_PATTERN.match(name):
            raise ValidationError(
                f"Invalid variable name '{name}'. "
                f"Must start with letter/underscore, contain only alphanumeric/underscore."
            )
        return name

    def validate_number(self, value: str) -> str:
        """Validate a numeric string."""
        if not self.NUMBER_PATTERN.match(value.strip()):
            raise ValidationError(f"Invalid number format: '{value}'")
        return value.strip()

    def parse_comma_list(self, text: str) -> List[str]:
        """Parse comma-separated values."""
        if not text.strip():
            return []
        return [item.strip() for item in text.split(',') if item.strip()]

    def parse_equation_system(self, text: str) -> Tuple[List[str], List[str]]:
        """Parse system of equations input format."""
        # Look for quoted equations
        quoted_match = re.search(r'["\']([^"\']*)["\']', text)
        if quoted_match:
            equations_part = quoted_match.group(1)
            variables_part = text[quoted_match.end():].strip()
        else:
            # Try to split by semicolon presence
            if ';' in text:
                # Heuristic: split at last occurrence of semicolon-block vs variables
                # Simpler heuristic: split by ' to ' or by bracketed variables
                parts = text.split()
                equations_tokens = []
                variables_tokens = []

                # Work backwards to collect variables-like tokens
                for part in reversed(parts):
                    if part.startswith('[') or part.endswith(']') or ',' in part or self.VARIABLE_PATTERN.match(part):
                        variables_tokens.insert(0, part)
                    else:
                        # remainder is equations
                        idx = parts.index(part)
                        equations_tokens = parts[:idx+1]
                        break

                if not equations_tokens:
                    raise ValidationError("Could not separate equations from variables")

                equations_part = ' '.join(equations_tokens)
                variables_part = ' '.join(variables_tokens)
            else:
                raise ValidationError("No equations found (use semicolons to separate)")

        # Parse equations
        equations = [eq.strip() for eq in equations_part.split(';') if eq.strip()]
        if not equations:
            raise ValidationError("No equations found after parsing")

        # Parse variables
        vars_str = variables_part.strip()
        if vars_str.startswith('[') and vars_str.endswith(']'):
            vars_str = vars_str[1:-1]

        if ',' in vars_str:
            variables = [v.strip() for v in vars_str.split(',') if v.strip()]
        else:
            variables = [v.strip() for v in vars_str.split() if v.strip()]

        if not variables:
            raise ValidationError("No variables found")

        # Validate variable names
        for var in variables:
            self.validate_variable_name(var)

        return equations, variables
