# Chirp Python I2C API

The Chirp is a capacitive soil-moisture sensor with an I2C slave interface.
This package provides the `Chirp` driver, register constants, and a hardware
test script.

## Files and initialization

`chirp.py` contains the `Chirp` class; `chirp_constant.py` defines the I2C
address, commands, registers, and default protocol delays. The default 7-bit
I2C address is `0x20`.

```python
from ecomet_i2c_sensors.chirp import Chirp

sensor = Chirp()
try:
    moisture = sensor.read_moisture()
    moisture_percent = sensor.moisture_to_percent(moisture)
    light_duration_ms = sensor.read_light_duration_ms()
finally:
    sensor.close()
```

The device begins in its normal alarm mode after reset. Receiving I2C
communication switches it into sensor mode, where it responds to reads and
does not chirp.

## Python API

| Function | Description and result |
|---|---|
| `Chirp(address=0x20, busnum=None, i2c=None, ...)` | Initialize the sensor interface. Supports the common I2C driver options. |
| `read_register(register)` | Return an unsigned 16-bit, big-endian value. `register` can be `MOISTURE`, `LIGHT`, `TEMPERATURE`, or the corresponding register number. |
| `read_moisture()` | Return the raw capacitive moisture reading. |
| `read_moisture_percent()` | Return relative moisture from the configured dry/wet calibration, clamped to `0–100 %`. This is not volumetric water content. |
| `moisture_to_percent(raw)` | Convert an already-read raw moisture value using the configured calibration. |
| `read_temperature()` | Return the raw temperature register value. The driver does not convert it to degrees; not all firmware implements this register. |
| `read_light()` | Request a light measurement, wait for it to complete, and return the raw light reading. |
| `read_light_duration_ms()` | Return the LED discharge time in milliseconds, or `None` if the light timer overflowed. This is not illuminance in lux. |
| `reset()` | Send the Chirp reset command. |
| `close()` | Close the underlying I2C bus. |

The timing values are configured in `~/.comet/config.yaml` under the top-level
`chirp` key (at the same level as `i2c`):

```yaml
chirp:
  register_read_delay: 0.02
  light_measurement_delay: 9.0
  moisture_dry_raw: 244
  moisture_wet_raw: 534
```

The delays are in seconds. The moisture calibration values are raw counts
measured at the dry and wet endpoints. If the file or `chirp` section is
absent, the driver defaults to 20 ms, 9 seconds, and the calibration above.
All four values can be overridden when constructing `Chirp(...)`. Calibration
must use two different integer readings in the `0–65535` range. The resulting
percentage is a relative scale for this sensor and setup, not an absolute
soil-water percentage. Unsupported register names or numbers raise
`ValueError`; I2C errors are propagated to the caller.

## Example

```python
from ecomet_i2c_sensors.chirp import Chirp

sensor = Chirp()
try:
    print("Moisture (relative):", sensor.read_moisture_percent(), "%")
    print("Light duration:", sensor.read_light_duration_ms(), "ms")
finally:
    sensor.close()
```

Hardware test script: `python_test_scripts/chirp/chirp_i2c_test.py`.
It accepts `--address` and `--bus`; use `--skip-light` to avoid the longer
light measurement.

See [chirp_i2c_protocol.md](chirp_i2c_protocol.md) for register numbers,
commands, and read timing.
