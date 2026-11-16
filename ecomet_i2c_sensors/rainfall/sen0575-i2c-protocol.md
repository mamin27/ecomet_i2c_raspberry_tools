# SEN0575 I2C protocol

This note covers the I2C register interface used by the Python rainfall
sensor driver. The sensor uses 7-bit address `0x1D`; multi-byte values are
little-endian.

| Register | Meaning | Size |
|---|---|---:|
| `0x00` | PID and VID | 4 bytes |
| `0x0A` | Firmware version | 2 bytes |
| `0x0C` | Rainfall in selected period | 4 bytes |
| `0x10` | Cumulative rainfall | 4 bytes |
| `0x14` | Raw tipping-bucket count | 4 bytes |
| `0x18` | Sensor working time in minutes | 2 bytes |
| `0x26` | Selected rainfall period in hours (write) | 1 byte |
| `0x28` | Accumulated rainfall baseline (write) | 2 bytes |

Rainfall register values use units of `1/10000 mm`; working time uses
minutes. Initialization expects PID `0x100C0` and VID `0x3343`. Valid
selected-hour values are 1 through 24. The baseline register stores rainfall
in `1/10000 mm` in a 16-bit value.

The Python driver uses `rainfall.collector` in `~/.comet/config.yaml` to
select the catchment area: `original` uses `50 × 110 mm` and `attachment`
uses the `200 cm²` inlet. With the attachment selected, rainfall readings
are corrected by `55/200`; baseline writes are converted back to the sensor's
native scale.
