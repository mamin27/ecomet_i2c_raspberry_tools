# SGP40 Python I2C API

The SGP40 measures raw gas-resistance signal and derives a VOC index with the
included Sensirion VOC algorithm.

## Files and initialization

`sgp40.py` contains `SGP40`; `sgp40_algorithm.py` implements the VOC index
algorithm and `sgp40_constant.py` defines sensor commands.

```python
from ecomet_i2c_sensors.sgp40 import sgp40

sensor = sgp40.SGP40(busnum=1, relative_humidity=50, temperature_c=25)
status = sensor.begin(duration=10)
```

## Python API

| Function | Description and result |
|---|---|
| `set_envparams(relative_humidity, temperature_c)` | Set compensation inputs in %RH and °C. |
| `begin(duration=10)` | Initialize the VOC algorithm, warm up for `duration` seconds, and run a sensor self-test; returns `0` on success, `1` on failure. |
| `measure_raw()` | Return raw VOC signal, or `-1` when reading/CRC validation fails. |
| `get_voc_index()` | Return the compensated VOC index (0–500), or `-1` on read failure. |
| `index_to_explanation(index)` | Map an index to `excelent`, `normal`, `warning`, `major`, or `critical` (the first label is spelled this way in the current implementation). |
| `read_register(register, byte=None)` | Read a supported response register; returns `(bytes, status)`. |
| `write_register(register, data)` | Send a supported command; returns status. |

The reading methods use the most recently supplied environmental parameters.
Private reset, CRC, and sensor-test helpers are implementation details.

## Example

```python
sensor.set_envparams(relative_humidity=45, temperature_c=22)
index = sensor.get_voc_index()
print(index, sensor.index_to_explanation(index))
```

Examples: `python_test_scripts/sgp40/sgp40_raw_value.py` and
`python_test_scripts/sgp40/sgp40_voc_index.py`.
