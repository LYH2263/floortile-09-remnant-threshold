import math

EPS = 1e-9


def ceil_units(value: float) -> int:
    """Ceil for positive tile/panel counts with stable float edge handling."""
    return int(math.ceil(float(value) - EPS))


def stable_remainder(total: float, unit: float) -> float:
    """total mod unit with near-seam floats folded to 0.0."""
    rem = math.fmod(float(total), float(unit))
    if abs(rem) < EPS or abs(abs(rem) - float(unit)) < EPS:
        return 0.0
    return rem
