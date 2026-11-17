#!/usr/bin/env python3

import argparse
import logging
import time

from ecomet_i2c_sensors.chirp import Chirp
from ecomet_i2c_sensors.chirp import chirp_constant


def main():
    parser = argparse.ArgumentParser(description="Read values from a Chirp sensor")
    parser.add_argument("--address", type=lambda value: int(value, 0),
                        default=chirp_constant.CHIRP_ADDRESS,
                        help="7-bit I2C address (default: 0x20)")
    parser.add_argument("--bus", type=int, default=None, help="I2C bus number")
    parser.add_argument("--skip-light", action="store_true",
                        help="skip the light measurement, which can take 9 seconds")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    sensor = Chirp(address=args.address, busnum=args.bus)

    try:
        moisture = sensor.read_moisture()
        temperature = sensor.read_temperature()
        print("Moisture (raw): {}".format(moisture))
        print("Temperature (raw): {}".format(temperature))

        if not args.skip_light:
            print("Measuring light (may take up to 9 seconds)...")
            light = sensor.read_light()
            print("Light (raw): {}".format(light))
    finally:
        sensor.close()


if __name__ == "__main__":
    main()
