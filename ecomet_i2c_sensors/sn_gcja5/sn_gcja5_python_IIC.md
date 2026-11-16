# SN-GCJA5 Python I2C API

The SN-GCJA5 driver reads particulate-matter concentrations, particle counts,
and sensor status.

## Files and initialization

`sn_gcja5.py` contains `SN_GCJA5`; register and status definitions are in
`sn_gcja5_constant.py`.

```python
from ecomet_i2c_sensors.sn_gcja5 import sn_gcja5

sensor = sn_gcja5.SN_GCJA5(busnum=1)
pm25, status = sensor.read_register("PM2_5")
```

## Python API

| Function | Description and result |
|---|---|
| `self_test()` | Check the state register; returns `0` for the expected state, `1` on read failure, or `2` for a non-zero state. |
| `read_register(register)` | Read one supported name: `PM1_0`, `PM2_5`, `PM10`, `P0_5`, `P1`, `P2_5`, `P5`, `P7_5`, `P10`, or `STATE`. Returns `(value, status)`. |
| `conf_register_list()` | Read the available measurements and return grouped `MASS`, `PARTICLE`, `PART_PERC`, and `STATUS` dictionaries. |

Mass readings are assembled from four bytes and divided by 1000 in the
driver; particle-count readings are assembled from two bytes. See
`sn_gcja5_constant.py` for register mapping and status bits.

## Example

```python
measurements = sn_gcja5.conf_register_list()
print(measurements["MASS"]["PM2_5"])
```

Example script: `python_test_scripts/sn_gcja5/sn_gcja5_i2c_test.py`.
