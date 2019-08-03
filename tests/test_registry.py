import pytest
from dunit import Registry


@pytest.fixture()
def registry():
    reg = Registry()
    return reg


def test_registry(registry):
    assert registry is not None


def test_register(registry):
    meter_unit = registry.units.register(name="meter", symbol="m", dimension="length")
    assert registry.units.meter is meter_unit
    assert registry.units.m is meter_unit
    assert registry.units["meter"] is meter_unit
    assert registry.units["m"] is meter_unit
