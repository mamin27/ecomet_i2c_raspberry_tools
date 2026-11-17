import logging
import math
import os
import time

import yaml

from ecomet_i2c_sensors.chirp import chirp_constant


_DEFAULT_REGISTER_READ_DELAY = 0.02
_DEFAULT_LIGHT_MEASUREMENT_DELAY = 9.0

_READ_REGISTERS = {
    "MOISTURE": chirp_constant.MOISTURE,
    "LIGHT": chirp_constant.LIGHT,
    "TEMPERATURE": chirp_constant.TEMPERATURE,
}


def _load_delays():
    config_path = os.path.expanduser("~/.comet/config.yaml")
    if not os.path.isfile(config_path):
        return {}

    with open(config_path, encoding="utf-8") as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML in {}".format(config_path)) from exc

    if not isinstance(config, dict):
        raise ValueError("config.yaml must contain a YAML mapping")
    chirp_config = config.get("chirp", {})
    if not isinstance(chirp_config, dict):
        raise ValueError("chirp config must be a YAML mapping")
    return chirp_config


def _validate_delay(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("{} must be a non-negative number".format(name))
    if not math.isfinite(value) or value < 0:
        raise ValueError("{} must be a non-negative number".format(name))
    return float(value)


class Chirp:
    """Read raw moisture, light, and temperature values from a Chirp sensor."""

    def __init__(
        self,
        address=chirp_constant.CHIRP_ADDRESS,
        busnum=None,
        i2c=None,
        register_read_delay=None,
        light_measurement_delay=None,
        **kwargs
    ):
        config = _load_delays()
        if register_read_delay is None:
            register_read_delay = config.get(
                "register_read_delay", _DEFAULT_REGISTER_READ_DELAY
            )
        if light_measurement_delay is None:
            light_measurement_delay = config.get(
                "light_measurement_delay", _DEFAULT_LIGHT_MEASUREMENT_DELAY
            )
        register_read_delay = _validate_delay(
            "register_read_delay", register_read_delay
        )
        light_measurement_delay = _validate_delay(
            "light_measurement_delay", light_measurement_delay
        )

        if i2c is None:
            import ecomet_i2c_sensors.i2c as i2c

        self._logger = logging.getLogger(__name__)
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self.register_read_delay = register_read_delay
        self.light_measurement_delay = light_measurement_delay

    def close(self):
        """Close the underlying I2C bus."""
        self._device.close()

    def read_register(self, register):
        """Read a 16-bit big-endian sensor register by name or register number."""
        if isinstance(register, str):
            try:
                register = _READ_REGISTERS[register.upper()]
            except KeyError as exc:
                raise ValueError("unsupported Chirp register: {}".format(register)) from exc
        elif register not in _READ_REGISTERS.values():
            raise ValueError("unsupported Chirp register: {}".format(register))

        self._device.writeRaw8(register)
        time.sleep(self.register_read_delay)
        data = self._device.readRawBytes(2)
        if len(data) != 2:
            raise IOError("Chirp register 0x{:02x} returned {} bytes, expected 2".format(
                register, len(data)
            ))
        value = (data[0] << 8) | data[1]
        self._logger.debug("Read Chirp register 0x%02x: %d", register, value)
        return value

    def read_moisture(self):
        """Return the raw 16-bit capacitive moisture reading."""
        return self.read_register("MOISTURE")

    def read_temperature(self):
        """Return the raw 16-bit temperature reading (not converted to degrees)."""
        return self.read_register("TEMPERATURE")

    def read_light(self):
        """Request a light measurement and return its raw 16-bit reading."""
        self._device.writeRaw8(chirp_constant.REQUEST_LIGHT_MEASUREMENT)
        time.sleep(self.light_measurement_delay)
        return self.read_register("LIGHT")

    def reset(self):
        """Send the sensor reset command."""
        self._device.writeRaw8(chirp_constant.RESET)
