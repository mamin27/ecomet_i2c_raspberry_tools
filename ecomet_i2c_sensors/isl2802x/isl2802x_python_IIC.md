# ISL28022 Python I2C API

The ISL28022 driver provides voltage, shunt-voltage, current, and power
measurement helpers for an I2C power monitor.

## Files and initialization

`isl2802x.py` contains `ISL28022`; register definitions are in
`isl2802x_constant.py`. The module-level `conf_register_list()` returns
decoded configuration for the selected address.

```python
from ecomet_i2c_sensors.isl2802x import isl2802x

monitor = isl2802x.ISL28022(busnum=1)
size, unit, readings = monitor.measure_voltage()
```

## Python API

| Function | Description and result |
|---|---|
| `measure_voltage(stime=1, unit='V', voltage_scale=60)` | Measure bus voltage; returns `(sample_count, unit, readings_by_sample)`. |
| `measure_shunt_voltage(stime=1, unit='mV', voltage_shunt_scale='80mV')` | Measure shunt voltage; returns `(sample_count, unit, readings_by_sample)`. |
| `current_conversion(current, unit)` | Convert a current value to the requested supported unit. |
| `voltage_conversion(voltage, vtype, unit)` | Convert a voltage value to the requested unit/type. |
| `power_conversion(power, unit)` | Convert a power value to the requested unit. |
| `read_funct(function)` | Read the named configuration/measurement function from the device. |
| `write_funct(function, value)` | Write a configuration value; returns a status code. |
| `read_register(register)` | Read a named register; returns `(value, status)`. |
| `write_register(register, value)` | Write a named register; returns status. |
| `bit_init(...)`, `bit_get(...)`, `bits_init(...)`, `bits_get(...)` | Prepare or read a bit or bit field in a register. |
| `bit_set(...)`, `bits_set(...)` | Update a bit or bit field in a register. |
| `unaryStruct_get(...)`, `unaryStruct_set(...)` | Read or write a packed register using the selected `struct` format. |
| `conf_register_list(address=...)` | Return decoded configuration registers for the selected I2C address. |

The measurement dictionary contains readings indexed by sample. Supported
units and register/function names are defined in the module constants.

## Example

```python
size, unit, values = monitor.measure_shunt_voltage(
    stime=1, unit="mV", voltage_shunt_scale="80mV"
)
print(unit, values)
```

Example script: `python_test_scripts/isl28022_i2c_test.py`.

The separate `isl2802x_ui.py` module currently defines `INA260_UI` and
imports the INA260 driver; it is not an ISL28022 measurement wrapper.
