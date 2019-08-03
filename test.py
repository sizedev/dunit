import dunit
reg = dunit.Registry()
reg.units.register(name="meter", symbol="m", dimension="length")
q = reg.parse_quantity("3.14m")
print(q + q)
