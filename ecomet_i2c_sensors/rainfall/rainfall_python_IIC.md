# SEN0575 rainfall sensor Python I2C API

The driver reads cumulative and period rainfall, raw tipping-bucket counts,
sensor identity, firmware version, and working time.

## Files and initialization

`rainfall.py` contains `RainfallSensor`; `rainfall_constant.py` defines
registers and measurement scales. Catchment-area selection is configured in
`~/.comet/config.yaml`; see [collector-adapter-design.md](collector-adapter-design.md).

```python
from ecomet_i2c_sensors.rainfall import RainfallSensor

sensor = RainfallSensor()
if sensor.begin():
    print(sensor.get_rainfall(), "mm")
```

## Python API

| Function | Description and result |
|---|---|
| `begin()` | Verify the connected device PID/VID; returns `True` on success. |
| `close()` | Close the I2C device. |
| `get_pid_vid()` | Return `(PID, VID)` and save them on the instance. |
| `get_firmware_version()` | Return the firmware version as a dotted string. |
| `get_sensor_working_time()` | Return operating time in hours. |
| `get_rainfall()` | Return cumulative rainfall in mm, corrected for configured collector area. |
| `get_rainfall_time(hour)` | Return rainfall over the preceding 1–24 hours in mm. |
| `get_raw_data()` | Return the raw tipping-bucket count without area correction. |
| `set_rain_accumulated_value(value)` | Set the baseline in mm; validates the device register range and converts to native scale. |

`collector` may also be supplied to `RainfallSensor` as `"original"` or
`"attachment"` to override the YAML selection. The direct register helpers
`_read_register` and `_write_register` are private.

## Example

```python
sensor = RainfallSensor(collector="attachment")
rainfall_mm = sensor.get_rainfall()
hourly_mm = sensor.get_rainfall_time(1)
raw_count = sensor.get_raw_data()
```

Example script: `python_test_scripts/rainfall/rainfall_i2c_test.py`.
