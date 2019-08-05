Decimal based unit conversion

To get started, initialize the registry. It will automatically be loaded with the default units.
```
import unit
reg = unit.Registry()
```

If you don't want the default units loaded, set the load_defaults parameter to False.
```
import unit
reg = unit.Registry(load_defaults=False)
```

You can add custom units programatically. Make the scale is provided as a string, in order to avoid rounding.
```
reg.units.register(name="earth", symbol=None, dimension="mass", scale="5.9722e24", aliases=["earths"])
reg.units.register(name="moon", symbol=None, dimension="mass", scale="7.342e22", aliases=["moons"])
```

You can also load units via a json file.
```
reg.units.load_file("my_units.json")
```

Now you can parse values.
```
height = reg("5ft8in")
```

You can convert to other units.
```
height_in_meters = h.to("m")
```

You can also add different types of units together.
```
platform_shoes = reg("6in")
height_with_shoes = height_in_meters + platform_shoes
```

For presentation, you can convert a quantity to the most appropriate unit for a particular system.
```
height_with_shoes.to_best(system="USC")
```

