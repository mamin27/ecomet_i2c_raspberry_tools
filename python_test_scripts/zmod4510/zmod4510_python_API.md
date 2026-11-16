# ZMOD4510 Python API notes

The repository contains a test script for the external `zmod4510` Python
package, but does not include that package's implementation. This page
documents only the API calls and data fields used by
`zmod4510_i2c_test.py`; constructor options and other methods are not
verified against the library source.

## Initialization and lifecycle

```python
from zmod4510 import zmod4510, ZMODStatus

sensor = zmod4510.ZMOD4510(logger=logger)
if not sensor.start():
    raise RuntimeError("Failed to start sensor.")
```

`start()` starts the sensor and should be checked for a false result. The
test script calls `stop()` in a `finally` block to stop the sensor on normal
exit, interruption, or error.

## Reading data

`get_data()` returns an object with a `status` and, for an `OK` result,
`o3_ppb`, `no2_ppb`, `fast_aqi`, and `epa_aqi` fields. The script handles
these `ZMODStatus` members:

| Status | Meaning in the test script |
|---|---|
| `STABILIZATION` | Sensor is warming up. |
| `OK` | Log ozone and nitrogen-dioxide values and both AQI values. |
| `DAMAGE` | Report a damaged sensor. |
| Other values | Report an unknown status. |

Example:

```python
data = sensor.get_data()
if data.status == ZMODStatus.OK:
    print(data.o3_ppb, data.no2_ppb, data.fast_aqi, data.epa_aqi)
```

The accompanying test repeatedly reads data until interrupted with
Ctrl+C, then calls `stop()`. It writes logs to `zmod4510.log`.
