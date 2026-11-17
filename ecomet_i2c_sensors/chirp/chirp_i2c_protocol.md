# Chirp I2C protocol

The Chirp plant-watering sensor acts as an I2C slave at 7-bit address
`0x20` by default. The I2C header is also available for programming and
serial communication. The protocol and register map below follow the
manufacturer's [Chirp documentation](https://wemakethings.net/chirp/).

## Commands and registers

| Value | Name | Operation |
|---:|---|---|
| `0x00` | Moisture | Read two bytes of capacitive moisture data. |
| `0x03` | Request light measurement | Write this command to start a light measurement. |
| `0x04` | Light | Read two bytes of light data after requesting a measurement. |
| `0x05` | Temperature | Read two bytes of temperature data. |
| `0x06` | Reset | Write this command to reset the sensor. |

The moisture, light, and temperature readings are unsigned 16-bit values
transmitted most-significant byte first. The published interface describes
these as sensor readings but does not specify a conversion scale or
temperature unit; the Python driver therefore returns raw values.

## Read sequence and timing

To read a register, write its register number to the device, wait for the
register-read interval, then read two bytes. The Arduino examples use 20 ms
for this interval in standalone sensor mode and 1100 ms in the alarm firmware
example.

To read light, first write `0x03`, wait for the measurement, then read
register `0x04`. The firmware example allows up to 9 seconds for this
measurement. The Python driver defaults to 9 seconds plus the 20 ms register
read interval; both delays are configurable in `~/.comet/config.yaml` under
`chirp.register_read_delay` and `chirp.light_measurement_delay`, or at
initialization.

```yaml
chirp:
  register_read_delay: 0.02
  light_measurement_delay: 9.0
```

Both settings are in seconds. If either setting is omitted, its default value
is used.

The sensor may take 1 to 9 seconds to complete its initial moisture and light
measurements after reset. Any I2C communication during this startup period
switches the device into sensor mode. In sensor mode it responds to I2C
requests without making alarm sounds.

## Python usage

```python
from ecomet_i2c_sensors.chirp import Chirp

sensor = Chirp()
try:
    moisture = sensor.read_register(0x00)
    temperature = sensor.read_register("TEMPERATURE")
    light = sensor.read_light()
finally:
    sensor.close()
```

`chirp_constant.py` defines the address, register numbers, command values,
and default timing values used by the driver.
