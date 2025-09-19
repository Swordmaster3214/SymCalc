"""
Dual-format output system (exact + decimal).
"""
from typing import Any, Optional
from sympy import N, nsimplify, pprint, Rational
from decimal import getcontext

# Set high precision for decimal operations
getcontext().prec = 50

class OutputFormatter:
    """Handles all output formatting with exact + decimal display."""

    def __init__(self, precision: int = 15):
        self.precision = precision

    def display_result(self, result: Any, label: Optional[str] = None) -> None:
        """Display a result in both exact and decimal form when appropriate."""
        if label:
            print(f"{label}:")

        # Determine if we should show dual format
        should_show_dual = self._should_show_dual_format(result)

        if should_show_dual:
            # Show exact form
            print("Exact:")
            self._pretty_print_with_indent(result)

            # Show decimal approximation
            try:
                decimal_result = N(result, self.precision)
                if decimal_result != result:  # Only show if different
                    print("Decimal:")
                    self._pretty_print_with_indent(decimal_result)
            except Exception:
                pass  # Skip decimal if conversion fails
        else:
            # Show single format
            self._pretty_print(result)

    def _should_show_dual_format(self, obj: Any) -> bool:
        """Determine if object should be shown in both exact and decimal forms."""
        try:
            if hasattr(obj, 'is_Rational') and obj.is_Rational and obj.q != 1:
                return True
            if hasattr(obj, 'has') and obj.has(Rational):
                return True
            if hasattr(obj, 'atoms'):
                rationals = obj.atoms(Rational)
                if rationals and any(r.q != 1 for r in rationals):
                    return True
        except Exception:
            pass
        return False

    def _pretty_print(self, obj: Any) -> None:
        """Pretty print an object."""
        try:
            pprint(obj)
        except Exception:
            print(obj)

    def _pretty_print_with_indent(self, obj: Any) -> None:
        """Pretty print with indentation."""
        try:
            # Capture pprint output and indent it
            import io
            import contextlib

            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                pprint(obj)
            output = f.getvalue()

            # Indent each line
            for line in output.strip().split('\n'):
                print(f"  {line}")
        except Exception:
            print(f"  {obj}")

    def format_verification(self, equations: list, solutions: dict) -> None:
        """Format equation verification results."""
        print("\nVerification:")
        all_satisfied = True

        for i, eq in enumerate(equations, 1):
            try:
                substituted = eq.subs(solutions)

                # Check if equation is satisfied
                if hasattr(substituted, 'equals') and substituted.equals(True):
                    print(f"  Equation {i}: ✓ Satisfied")
                else:
                    # Calculate residual
                    if hasattr(eq, 'lhs') and hasattr(eq, 'rhs'):
                        residual = (eq.lhs - eq.rhs).subs(solutions)
                    else:
                        residual = substituted

                    # Check if numerically zero
                    try:
                        residual_val = float(N(residual, 15))
                        if abs(residual_val) < 1e-12:
                            print(f"  Equation {i}: ✓ Satisfied")
                        else:
                            print(f"  Equation {i}: ✗ Residual = {residual}")
                            all_satisfied = False
                    except:
                        if residual == 0:
                            print(f"  Equation {i}: ✓ Satisfied")
                        else:
                            print(f"  Equation {i}: ? Residual = {residual}")

            except Exception as e:
                print(f"  Equation {i}: Could not verify - {e}")

        if all_satisfied:
            print("✓ All equations satisfied!")

    def set_precision(self, precision: int) -> None:
        """Set display precision."""
        if precision < 1 or precision > 100:
            raise ValueError("Precision must be between 1 and 100")
        self.precision = precision
