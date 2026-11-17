#!/usr/bin/env python3

import argparse
import logging
import sys

from ecomet_i2c_sensors.chirp import Chirp
from ecomet_i2c_sensors.chirp import chirp_constant


def main():
    parser = argparse.ArgumentParser(
        description="Read measurements from a Chirp soil moisture sensor"
    )
    parser.add_argument("--address", type=lambda value: int(value, 0),
                        default=chirp_constant.CHIRP_ADDRESS,
                        help="7-bit I2C address (default: 0x20)")
    parser.add_argument("--bus", type=int, default=None, help="I2C bus number")
    parser.add_argument("--skip-light", action="store_true",
                        help="skip the light measurement")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    sensor = Chirp(address=args.address, busnum=args.bus)

    try:
        print("Chirp soil moisture sensor:")
        try:
            moisture = sensor.read_moisture()
        except OSError as exc:
            logging.error("No valid moisture reading: %s", exc)
            return 1
        moisture_percent = sensor.moisture_to_percent(moisture)
        print("Soil moisture (relative): {:.1f} %".format(moisture_percent))
        print("Soil moisture (raw): {}".format(moisture))

        if not args.skip_light:
            print(
                "Measuring ambient light with the LED sensor "
                "(waiting {:.1f} seconds)...".format(
                    sensor.light_measurement_delay
                )
            )
            print("No visible LED blink is expected during this measurement.")
            light_duration = sensor.read_light_duration_ms()
            if light_duration is None:
                print("Ambient light: timer overflow (too dark or no valid reading)")
            else:
                print(
                    "LED light-sensor discharge time: {:.3f} ms".format(
                        light_duration
                    )
                )
    finally:
        sensor.close()


if __name__ == "__main__":
    sys.exit(main())
