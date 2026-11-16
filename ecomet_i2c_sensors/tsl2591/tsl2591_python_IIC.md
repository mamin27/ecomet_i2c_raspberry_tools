# TSL2591 Python I2C API

The TSL2591 driver measures full-spectrum, infrared, visible light, and
calculated illuminance.

## Files and initialization

`tsl2591.py` contains `TSL2591`; `tsl2591_constant.py` defines registers,
gains, integration times, and lux coefficients. Initialization verifies the
device ID and configures the sensor.

```python
from ecomet_i2c_sensors.tsl2591 import tsl2591

sensor = tsl2591.TSL2591(busnum=1)
lux, gain, integration = sensor.Lux()
```

## Python API

| Function or property | Description and result |
|---|---|
| `self_test()` | Check the device ID; returns `0` on success and non-zero on failure. |
| `enable_ic`, `disable_ic`, `reset_ic` | Properties that enable, disable, or reset the sensor. |
| `get_gain`, `get_IntegralTime` | Properties that read current gain and integration-time settings. |
| `set_gain(data)` | Set one of `GAIN_LOW`, `GAIN_MED`, `GAIN_HIGH`, `GAIN_MAX`. |
| `set_IntegralTime(data)` | Set integration time from 100 to 600 ms. |
| `set_persistent(data)` | Set the interrupt persistence filter. |
| `Read_FullSpectrum(calibrate=None)` | Return both channels combined with gain and integration-time labels. |
| `Read_Infrared(calibrate=None)` | Return IR channel data with gain and integration-time labels. |
| `Read_Visible(calibrate=None)` | Return visible channel data with gain and integration-time labels. |
| `Lux()` | Calculate lux; returns `(lux, gain, integration_time)` or `-1` for invalid/saturated readings. |
| `append_lux()` | Append the current lux result to the internal sample list. |
| `SelfCalibrate()` | Run multi-setting lux calibration and return its average. |
| `SelfCalibrate_perChannel(chan)` | Calibrate a selected channel; returns `(channel_value, status)`. |
| `read_register(register)` | Read a named register; returns `(value, status)`. |
| `write_register(register, data)` | Write a named register; returns status. |
| `SpecialFunction(funct)` | Send a supported interrupt command. |
| `SET_InterruptThreshold(HIGH, LOW)` | Set raw channel-count interrupt thresholds. |
| `TSL2591_SET_LuxInterrupt(SET_LOW, SET_HIGH)` | Convert lux thresholds to raw counts and configure the interrupt. |
| `conf_register_list()` | Return decoded sensor configuration, status, thresholds, and channel readings. |

Property accessors are used without parentheses. Measurement results include
the active gain and integration-time names so readings can be interpreted
with their acquisition settings.

## Example

```python
sensor.enable_ic
visible, gain, integration = sensor.Read_Visible()
lux, gain, integration = sensor.Lux()
```

Example script: `python_test_scripts/tsl2591/tsl2591_i2c_test.py`.
