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
temperature unit; the Python driver therefore returns raw values. The linked
firmware source does not implement a temperature-register read in sensor
mode, so only use that register if the installed firmware explicitly supports
it.

## Read sequence and timing

To read a register, write its register number to the device, wait for the
register-read interval, then read two bytes. The Arduino examples use 20 ms
for this interval in standalone sensor mode and 1100 ms in the alarm firmware
example.

To read light, first write `0x03`, wait for the measurement, then read
register `0x04`. The firmware example allows up to 9 seconds for this
measurement. The Python driver defaults to 9 seconds plus the 20 ms register
read interval; both delays are configurable in `~/.comet/config.yaml` under
`i2c.sensor.chirp`, or at initialization.

```yaml
i2c:
  sensor:
    chirp:
      register_read_delay: 0.02
      light_measurement_delay: 15.0
```

Both settings are in seconds. If either setting is omitted, its default value
is used.

The sensor may take 1 to 9 seconds to complete its initial moisture and light
measurements after reset. Any I2C communication during this startup period
switches the device into sensor mode. In sensor mode it responds to I2C
requests without making alarm sounds.

## Engineering units and calibration

The moisture register reports a device-specific raw capacitive reading, not
water content in `m³/m³` or percent by volume. The driver can map two measured
endpoints to a relative `0–100 %` scale. The default endpoints below are
calibration values supplied for one sensor:

```yaml
chirp:
  moisture_dry_raw: 244
  moisture_wet_raw: 534
```

In this relative scale, `244` maps to `0 %` and `534` to `100 %`. Values
outside the calibrated range are clamped. The wet endpoint should be measured
in the intended wet reference condition; immersion in water is not a
volumetric soil-moisture calibration.

The light register reports a timer count, not lux. For the published
firmware's 250 kHz clock and 1:256 timer prescaler, one count is `1.024 ms`;
`0xFFFF` indicates timer overflow and is reported as no valid duration.
Converting this duration to lux requires calibration against a light meter
and depends on the LED and firmware. During measurement, firmware briefly
forward-biases the LED to discharge its junction capacitance, then immediately
reverse-biases it and measures the discharge time. This pulse is not intended
to be a visible status blink, so absence of a visible flash is expected.

## Python usage

```python
from ecomet_i2c_sensors.chirp import Chirp

sensor = Chirp()
try:
    moisture_percent = sensor.read_moisture_percent()
    light_duration_ms = sensor.read_light_duration_ms()
finally:
    sensor.close()
```

`chirp_constant.py` defines the address, register numbers, command values,
and default timing values used by the driver.
