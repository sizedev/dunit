import json
import re

from dunit import Unit
from dunit import Quantity


class UnitRegistry():
    __slots__ = ("_units", )

    def __init__(self):
        self._units = {}

    # reg.units["unit_string"] - find a unit that matches the given unit_string
    def __getitem__(self, key: str) -> Unit:
        return self._units[key]

    # reg.units.unit_string - find a unit that matches the given unit_string
    def __getattr__(self, name: str) -> Unit:
        return self._units[name]

    def __contains__(self, name: str) -> Unit:
        return name in self._units

    # add a unit to the unit registry
    def register(self, *args, **kwargs) -> Unit:
        unit = Unit(*args, **kwargs)
        all_names = [unit, unit.name, unit.symbol] + unit.aliases
        for name in all_names:
            self._units[name] = unit
        return unit

    # load definitions from a JSON file
    def load_file(self, path) -> None:
        with open(path) as f:
            data = json.load(f)
            for u in data:
                self.register(Unit.from_dict(u))


class Registry():
    __slots__ = ("_unit_registry", )

    def __init__(self):
        self._unit_registry = UnitRegistry()

    @property
    def units(self):
        return self._unit_registry

    def parse_quantity(self, quantity_string: str) -> Quantity:
        # Handle feet and inches as ' and "
        quantity_string = quantity_string.replace("'", "ft").replace('"', "in")

        # Get all value/unit pairs
        quantity_pairs = re.findall(r'(\d+\.?\d*)\s*([a-zA-Z]+)', quantity_string)

        if not quantity_pairs:
            raise "No quantities found"

        # Add them all together to get a total
        quantity = 0

        for value_string, unit_string in quantity_pairs:
            if unit_string not in self.units:
                raise f"Unit '{unit_string}' not recognized"
            unit = self.units[unit_string]
            quantity += Quantity(registry=self, value=value_string, unit=unit)

        return quantity
