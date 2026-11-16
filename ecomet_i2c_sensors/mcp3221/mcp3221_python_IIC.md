# MCP3221 Python I2C API

The MCP3221 module reads the 12-bit ADC value and maps it to a direction.

## Files and initialization

`mcp3221.py` contains `MCP3221`; scale and direction calibration values are
in `mcp3221_constant.py`.

```python
from ecomet_i2c_sensors.mcp3221 import mcp3221

adc = mcp3221.MCP3221(busnum=1)
degrees, status = adc.to_max_const
direction, status = adc.degrees_to_cardinal_calibrated
```

The read methods below are properties: access them without parentheses.

## Python API

| Property | Description and result |
|---|---|
| `read_value` | Read the ADC and normalize its raw value; returns `(fraction, status)`. |
| `to_max_const` | Scale the normalized reading to the configured 0–360° range; returns `(degrees, status)`. |
| `degrees_to_cardinal` | Convert the angle into one of eight cardinal/intercardinal directions. |
| `degrees_to_cardinal_calibrated` | Convert using the calibrated direction thresholds in `mcp3221_constant.py`. |

Direction properties return `(direction, status)`; a conversion error is
reported as `"Error"` with a non-zero status.

## Example

```python
direction, status = adc.degrees_to_cardinal_calibrated
if status == 0:
    print(direction)
```

Example script: `python_test_scripts/mcp3221/mcp3221_i2c_test.py`.
