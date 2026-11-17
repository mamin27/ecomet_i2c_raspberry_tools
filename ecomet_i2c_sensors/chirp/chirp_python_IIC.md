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
| `read_moisture()` | Return a valid raw capacitive moisture reading (`0–1023`), retrying transient I2C errors or out-of-range data up to three times. Raises `IOError` if all attempts fail. |
| `read_moisture_percent()` | Return relative moisture from the configured dry/wet calibration, clamped to `0–100 %`. This is not volumetric water content. |
| `moisture_to_percent(raw)` | Convert an already-read raw moisture value using the configured calibration. |
| `read_temperature()` | Return the raw temperature register value. The driver does not convert it to degrees; not all firmware implements this register. |
| `read_light()` | Request a light measurement, wait for it to complete, and return the raw light reading. |
| `read_light_duration_ms()` | Return the LED discharge time in milliseconds, or `None` if the light timer overflowed. This is not illuminance in lux. |
| `reset()` | Send the Chirp reset command. |
| `set_address(address)` | Store a new I2C address in EEPROM (`0x20–0x29`). The sensor listens at it after reset or power cycle. |
| `get_stored_address()` | Read the I2C address byte stored in EEPROM. |
| `close()` | Close the underlying I2C bus. |

The timing and calibration values are configured in
`~/.comet/config.yaml` under `i2c.sensor.chirp`, alongside other sensor
configuration:

```yaml
i2c:
  sensor:
    chirp:
      register_read_delay: 0.02
      light_measurement_delay: 15.0
      moisture_dry_raw: 244
      moisture_wet_raw: 534
```

The delays are in seconds. The moisture calibration values are raw counts
measured at the dry and wet endpoints. A top-level `chirp` section is also
accepted for compatibility, but `i2c.sensor.chirp` takes precedence. If both
sections are absent, the driver defaults to 20 ms, 9 seconds, and the
calibration above. All four values can be overridden when constructing
`Chirp(...)`. Calibration must use two different integer readings in the
`0–1023` range. The resulting percentage is a relative scale for this sensor
and setup, not an absolute soil-water percentage. Unsupported register names
or numbers raise `ValueError`; I2C errors are propagated to the caller.

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

To assign an address, connect only one sensor at its current address and run:

```shell
python3 python_test_scripts/chirp/chirp_set_address.py 0x21 --current-address 0x20
```

The script writes and verifies the address EEPROM byte, then asks you to
power-cycle the sensor. It does not erase or initialize the rest of EEPROM;
the firmware's light-threshold initialization remains unchanged. The ten
supported address slots are `0x20` through `0x29`.

See [chirp_i2c_protocol.md](chirp_i2c_protocol.md) for register numbers,
commands, and read timing.
