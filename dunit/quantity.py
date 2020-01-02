from typing import Any
from decimal import Decimal
import numbers
import math

from dunit.unit import Unit


def zero_to_quantity(fn):
    def wrapper(self, other):
        if isinstance(other, numbers.Number) and other == 0:
            other = Quantity(registry=self.registry, value=0, unit=self.unit)
        return fn(self, other)
    return wrapper


def require_quantity(fn):
    def wrapper(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("Quantity required")
        return fn(self, other)
    return wrapper


def require_same_dimensions(fn):
    def wrapper(self, other):
        if self.unit.dimension != other.unit.dimension:
            raise TypeError("Incompatible dimensions")
        return fn(self, other)
    return wrapper


def require_dimensionless(fn):
    def wrapper(self, other):
        if not isinstance(other, numbers.Number):
            raise TypeError("Number required")
        return fn(self, other)
    return wrapper


class Quantity:
    __slots__ = ("_registry", "_value", "_unit")

    def __init__(self, registry, value: Any, unit: Unit):
        self._registry = registry
        self._value = Decimal(value)
        self._unit = unit

    @property
    def registry(self):
        return self._registry

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    def to(self, new_unit):
        if not (isinstance(new_unit, str) or isinstance(new_unit, Unit)):
            raise "new_unit must be a string or a Unit instance"

        if isinstance(new_unit, str):
            if new_unit not in self.registry.units:
                raise "Unrecognized unit"
            new_unit = self.registry.units[new_unit]

        if new_unit is self.unit:
            return self

        if new_unit.dimension != self.unit.dimension:
            raise "Cannot convert between units of different dimensions"
        new_value = self.value * (self.unit.scale / new_unit.scale)
        return Quantity(registry=self.registry, value=new_value, unit=new_unit)

    def to_best(self, system=None):
        raise NotImplementedError

    # Formatting methods
    def __str__(self) -> str:
        return f"{self.value}{self.unit.symbol}"

    def __repr__(self) -> str:
        params = ", ".join((
            f"value={self.value!r}",
            f"unit={self.unit.name!r}"
        ))
        return f"Quantity({params})"

    def __format__(self, format_spec):
        raise NotImplementedError

    # Math methods
    @zero_to_quantity
    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return False
        if self.unit.dimension != other.unit.dimension:
            return False
        other_value = other.to(self.unit).value
        if self.value != other_value:
            return False
        return True

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __lt__(self, other):
        left_value = self.value
        right_value = other.to(self.unit).value
        raise left_value < right_value

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __le__(self, other):
        left_value = self.value
        right_value = other.to(self.unit).value
        raise left_value <= right_value

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __gt__(self, other):
        left_value = self.value
        right_value = other.to(self.unit).value
        raise left_value > right_value

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __ge__(self, other):
        left_value = self.value
        right_value = other.to(self.unit).value
        raise left_value >= right_value

    def __hash__(self):
        raise NotImplementedError

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __add__(self, other):
        new_value = self.value + other.to(self.unit).value
        return Quantity(self.registry, new_value, self.unit)

    def __radd__(self, other):
        return self.__add__(other)

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __sub__(self, other):
        new_value = self.value - other.to(self.unit).value
        return Quantity(self.registry, new_value, self.unit)

    @zero_to_quantity
    @require_quantity
    @require_same_dimensions
    def __rsub__(self, other):
        new_value = other.to(self.unit).value - self.value
        return Quantity(self.registry, new_value, self.unit)

    @require_dimensionless
    def __mul__(self, other):
        new_value = self.value * other
        return Quantity(self.registry, new_value, self.unit)

    def __rmul__(self, other):
        return self.__mul__(self, other)

    @require_dimensionless
    def __truediv__(self, other):
        new_value = self.value / other
        return Quantity(self.registry, new_value, self.unit)

    def __rtruediv__(self, other):
        raise TypeError("Cannot divide by Quantity")

    @require_dimensionless
    def __floordiv__(self, other):
        new_value = self.value // other
        return Quantity(self.registry, new_value, self.unit)

    def __rfloordiv__(self, other):
        raise TypeError("Cannot divide by Quantity")

    @require_dimensionless
    def __mod__(self, other):
        new_value = self.value % other
        return Quantity(self.registry, new_value, self.unit)

    def __rmod__(self, other):
        raise TypeError("Cannot divide by Quantity")

    @require_dimensionless
    def __divmod__(self, other):
        new_quotient_value = self.value // other
        new_remainder_value = self.value % other
        return (
            Quantity(self.registry, new_quotient_value, self.unit),
            Quantity(self.registry, new_remainder_value, self.unit)
        )

    def __rdivmod__(self, other):
        raise TypeError("Cannot divide by Quantity")

    def __pow__(self, other):
        raise TypeError("Cannot raise Quantity to a power")

    def __rpow__(self, other):
        raise TypeError("Cannot raise Quantity to a power")

    def __neg__(self):
        new_value = -self.value
        return Quantity(self.registry, new_value, self.unit)

    def __pos__(self):
        return self

    def __abs__(self):
        new_value = abs(self.value)
        return Quantity(self.registry, new_value, self.unit)

    def __invert__(self):
        raise "Cannot invert Quantity"

    def __int__(self):
        if self.unit.dimension is None:
            return int(self.value)
        raise "Cannot convert Quantity to int"

    def __float__(self):
        if self.unit.dimension is None:
            return float(self.value)
        raise "Cannot convert Quantity to float"

    def __round__(self, ndigits: int = None):
        new_value = round(self.value, ndigits)
        return Quantity(self.registry, new_value, self.unit)

    def __trunc__(self):
        new_value = math.trunc(self.value)
        return Quantity(self.registry, new_value, self.unit)

    def __floor__(self):
        new_value = math.floor(self.value)
        return Quantity(self.registry, new_value, self.unit)

    def __ceil__(self):
        new_value = math.ceil(self.value)
        return Quantity(self.registry, new_value, self.unit)
