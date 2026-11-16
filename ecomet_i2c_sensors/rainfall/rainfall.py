import logging
import math
import os
import time

import yaml

from ecomet_i2c_sensors.rainfall import rainfall_constant as constant


class RainfallSensor:
    """I2C driver for the DFRobot SEN0575 rainfall sensor."""

    def __init__(self, address=constant.RAINFALL_ADDRESS, busnum=None,
                 i2c=None, collector=None, **kwargs):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as i2c

        if collector is None:
            config_path = os.path.expanduser("~/.comet/config.yaml")
            collector = "original"
            if os.path.isfile(config_path):
                with open(config_path, encoding="utf-8") as config_file:
                    try:
                        config = yaml.safe_load(config_file)
                    except yaml.YAMLError as exc:
                        raise ValueError(
                            "Invalid YAML in {}".format(config_path)
                        ) from exc
                if not isinstance(config, dict):
                    raise ValueError("config.yaml must contain a YAML mapping")
                rainfall_config = config.get("rainfall", {})
                if not isinstance(rainfall_config, dict):
                    raise ValueError("rainfall config must be a YAML mapping")
                collector = rainfall_config.get("collector", "original")

        if collector not in constant.COLLECTOR_AREAS_MM2:
            raise ValueError(
                "collector must be one of: {}".format(
                    ", ".join(constant.COLLECTOR_AREAS_MM2)
                )
            )

        self.collector = collector
        self._rainfall_factor = (
            constant.ORIGINAL_COLLECTOR_AREA_MM2 /
            constant.COLLECTOR_AREAS_MM2[collector]
        )
        self._logger = logging.getLogger(__name__)
        self._device = i2c.get_i2c_device(address, busnum=busnum, **kwargs)
        self.pid = None
        self.vid = None

    def close(self):
        self._device.close()

    def _read_register(self, register, length):
        data = self._device.readList(register, length)
        if len(data) != length:
            raise IOError(
                "Short read from rainfall sensor register 0x{:02X}".format(
                    register
                )
            )
        return bytes(data)

    def _write_register(self, register, data):
        self._device.writeList(register, list(data))
        time.sleep(0.1)

    def get_pid_vid(self):
        data = self._read_register(constant.REG_PID_VID, 4)
        pid = data[0] | (data[1] << 8) | ((data[3] & 0xC0) << 10)
        vid = data[2] | ((data[3] & 0x3F) << 8)
        self.pid = pid
        self.vid = vid
        return pid, vid

    def begin(self):
        """Check that the connected device is a supported SEN0575."""
        pid, vid = self.get_pid_vid()
        if pid != constant.EXPECTED_PID or vid != constant.EXPECTED_VID:
            self._logger.error(
                "Unexpected rainfall sensor identity: PID=0x%X VID=0x%X",
                pid, vid
            )
            return False
        return True

    def get_firmware_version(self):
        version = int.from_bytes(
            self._read_register(constant.REG_FIRMWARE_VERSION, 2), "little"
        )
        return "{}.{}.{}.{}".format(
            (version >> 12) & 0xF,
            (version >> 8) & 0xF,
            (version >> 4) & 0xF,
            version & 0xF
        )

    def get_sensor_working_time(self):
        minutes = int.from_bytes(
            self._read_register(constant.REG_WORKING_TIME, 2), "little"
        )
        return minutes / 60.0

    def get_rainfall(self):
        """Return cumulative rainfall in millimeters."""
        value = int.from_bytes(
            self._read_register(constant.REG_CUMULATIVE_RAINFALL, 4),
            "little"
        )
        return value / constant.RAINFALL_SCALE * self._rainfall_factor

    def get_rainfall_time(self, hour):
        """Return rainfall for the preceding 1-24 hours, in millimeters."""
        if isinstance(hour, bool) or not isinstance(hour, int) or not (
            constant.MIN_PERIOD_HOURS <= hour <= constant.MAX_PERIOD_HOURS
        ):
            raise ValueError("hour must be an integer from 1 to 24")

        self._write_register(
            constant.REG_RAINFALL_PERIOD_HOURS, [hour]
        )
        value = int.from_bytes(
            self._read_register(constant.REG_PERIOD_RAINFALL, 4), "little"
        )
        return value / constant.RAINFALL_SCALE * self._rainfall_factor

    def get_raw_data(self):
        """Return the raw tipping-bucket count."""
        return int.from_bytes(
            self._read_register(constant.REG_RAW_COUNT, 4), "little"
        )

    def set_rain_accumulated_value(self, value):
        """Set the accumulated-rainfall baseline in millimeters."""
        max_baseline = constant.MAX_BASELINE_MM * self._rainfall_factor
        if (not math.isfinite(value) or value < 0 or
                value > max_baseline):
            raise ValueError(
                "value must be between 0 and {:.4f} mm".format(
                    max_baseline
                )
            )

        raw_value = int(
            value / self._rainfall_factor * constant.RAINFALL_SCALE
        )
        self._write_register(
            constant.REG_ACCUMULATED_BASELINE,
            raw_value.to_bytes(2, "little")
        )
