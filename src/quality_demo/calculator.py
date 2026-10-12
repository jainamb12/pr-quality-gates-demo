from math import fsum
from numbers import Real


def calculate_statistics(numbers: list[Real]) -> dict[str, float | int]:
    """Calculate basic statistics for a non-empty list of numbers."""
    if not numbers:
        raise ValueError("The input list cannot be empty.")

    if any(
        isinstance(number, bool) or not isinstance(number, Real)
        for number in numbers
    ):
        raise TypeError("All values must be real numbers.")

    values = [float(number) for number in numbers]

    total = fsum(values)

    return {
        "count": len(values),
        "total": total,
        "mean": total / len(values),
        "minimum": min(values),
        "maximum": max(values),
    }