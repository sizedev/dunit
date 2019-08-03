from __future__ import annotations
from typing import Any
from decimal import Decimal
import numbers

from dunit.unit import Unit


class Quantity:
    __slots__ = ("_registry", "_value", "_unit")

    def __init__(self, registry: "Registry", value: Any, unit: Unit):
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

    def to_unit(self, new_unit):
        if not (isinstance(new_unit, str) or isinstance(new_unit, Unit)):
            raise "new_unit must be a string or a Unit instance"

        if isinstance(new_unit, str):
            if new_unit not in self.registry.units:
                raise "Unrecognized unit"
            new_unit = self.registry.units[new_unit_string]

        if new_unit is self.unit:
            return self
        new_value = self.value * (new_unit.scale / self.unit.scale)
        return Quantity(registry=self.registry, value=new_value, unit=new_unit)

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
    def __lt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        if self.value == 0 and isinstance(other, numbers.Number) and other == 0:
            return True
        if not isinstance(other, Quantity):
            return False
        if self.unit.dimension != other.unit.dimension:
            return False
        other_value = other.to_unit(self.unit).value
        if self.value != other_value:
            return False
        return True

    def __ne__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __add__(self, other: Quantity):
        if isinstance(other, numbers.Number) and other == 0:
            return self
        if not isinstance(other, Quantity):
            raise "Cannot add Quantity with non-Quantity"
        if self.unit.dimension != other.unit.dimension:
            raise "Cannot add Quantities with different dimenions"
        new_value = self.value + other.to_unit(self.unit).value
        return Quantity(self.registry, new_value, self.unit)

    def __radd__(self, other: Quantity):
        return self.__add__(other)

    def __sub__(self, other: Quantity):
        raise NotImplementedError

    def __rsub__(self, other: Quantity):
        raise NotImplementedError

    def __mul__(self, other: Quantity):
        raise NotImplementedError

    def __rmul__(self, other: Quantity):
        raise NotImplementedError

    def __truediv__(self, other: Quantity):
        raise NotImplementedError

    def __rtruediv__(self, other: Quantity):
        raise NotImplementedError

    def __floordiv__(self, other: Quantity):
        raise NotImplementedError

    def __rfloordiv__(self, other: Quantity):
        raise NotImplementedError

    def __mod__(self, other: Quantity):
        raise NotImplementedError

    def __rmod__(self, other: Quantity):
        raise NotImplementedError

    def __divmod__(self, other: Quantity):
        raise NotImplementedError

    def __rdivmod__(self, other: Quantity):
        raise NotImplementedError

    def __pow__(self, other: Quantity):
        raise NotImplementedError

    def __rpow__(self, other: Quantity):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __pos__(self):
        raise NotImplementedError

    def __abs__(self):
        raise NotImplementedError

    def __invert__(self):
        raise NotImplementedError

    def __int__(self):
        if self.unit.dimension is None:
            return int(self.value)
        raise "Cannot convert quantity to int"

    def __float__(self):
        if self.unit.dimension is None:
            return float(self.value)
        raise "Cannot convert quantity to float"

    def __round__(self, ndigits: int = None):
        raise NotImplementedError

    def __trunk__(self):
        raise NotImplementedError

    def __floor__(self):
        raise NotImplementedError

    def __ceil__(self):
        raise NotImplementedError
