# AXP805 Python I2C API

This package contains a power-management controller driver with the same
register-access API as the AXP209 package.

## Files and initialization

The implementation is `axp805.py`; it currently imports the AXP209 constants
and exposes a class named `AXP209`. Although `axp805_constant.py` is present,
the implementation does not use it.

## Python API

| Function or property | Description and result |
|---|---|
| `close()` | Close the I2C device. |
| `gpio2_output` | Write-only property; assign a truthy value to enable GPIO2 output, or a false value to disable it. |
| `adc_enable1`, `adc_enable2` | Read or write ADC enable flags. |
| `vbus_current_limit` | Read or set the VBUS current-limit setting. |
| `power_input_status`, `power_operating_mode` | Return decoded input and operating status flags. |
| `battery_current_direction`, `battery_exists`, `battery_charging` | Properties returning battery direction, presence, and charging state. |
| `battery_current_adc_enable`, `acin_voltage_adc_enable`, `acin_current_adc_enable` | Read ADC-enable flags. |
| `vbus_voltage_adc_enable`, `vbus_current_adc_enable`, `aps_voltage_adc_enable` | Read ADC-enable flags. |
| `ts_pin_adc_function_enable`, `apx209_internal_temperature_monitoring_adc_enable` | Read TS-pin and internal-temperature ADC flags. |
| `gpio0_adc_function_enable`, `gpio1_adc_function_enable` | Read GPIO ADC-function flags. |
| `battery_voltage`, `battery_charge_current`, `battery_discharge_current` | Properties returning voltage in mV and current in mA. |
| `internal_temperature` | Property returning PMIC temperature in °C. |
| `battery_gauge` | Property returning battery gauge percentage, or `-1` when unavailable. |
| `read_register(register)` | Read a named register; returns `(value, status)`. |
| `write_register(register, data)` | Write a named register; returns status. |

ADC, status, and battery accessors are properties; read them without
parentheses. Verify that this package's class and register definitions match
the AXP805 hardware before using it: the current implementation reuses AXP209
register constants and naming. Its `gpio2_output` setter also references an
unqualified flag class and may fail with `NameError`.

## Example

```python
from ecomet_i2c_sensors.axp805 import axp805

pmu = axp805.AXP209(busnum=1)
print(pmu.battery_voltage)
```
