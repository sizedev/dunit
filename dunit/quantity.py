import re
from decimal import Decimal

from dunit import Unit


class Quantity:
    __slots__ = ("value", "unit")

    def __init__(self, value=0, unit=None):
        self.value = Decimal(value)
        self.unit = unit

    @classmethod
    def parse(quantity_string):
        # Handle feet and inches as ' and "
        quantity_string = quantity_string.replace("'", "ft").replace('"', "in")

        # Get all value/unit pairs
        quantity_pairs = re.findall(r'(\d+\.?\d*)\s*([a-zA-Z]+)', quantity_string)

        if not quantity_pairs:
            # TODO: Do something useful here
            raise "No quantities found"

        # Add them all together to get a total
        quantity = 0

        for value_string, unit_string in quantity_pairs:
            quantity += Quantity(value_string, unit_string)
        return quantity

    def __add__(self, other):
        pass

    __radd__ = __add__
